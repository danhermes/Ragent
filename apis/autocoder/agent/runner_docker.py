import logging
import subprocess
import os
from typing import Tuple

logger = logging.getLogger(__name__)

def cleanup_docker_container():
    """Remove the Docker container if it exists"""
    try:
        logger.debug("Removing Docker container")
        subprocess.run(
            ["docker", "rm", "autocoder_agent_sandbox"],
            check=True,
            capture_output=True
        )
        logger.debug("Docker container removed successfully")
    except subprocess.CalledProcessError as e:
        if "No such container" in str(e.stderr):
            logger.debug("Docker container already removed")
        else:
            logger.error(f"Error removing Docker container: {str(e)}", exc_info=True)
            raise

def run_code_in_docker(code_path: str, cleanup: bool = False, env_var: str = None) -> Tuple[str, str]:
    """Run code in a Docker container
    
    Args:
        code_path: Path to the code file to run
        cleanup: Whether to remove the Docker container after running
        env_var: Environment variable to pass to the container in format "KEY=VALUE"
        
    Returns:
        Tuple of (stdout, stderr) from the container
    """
    logger.info(f"Running code in Docker: {code_path}")
    
    # Get absolute paths
    code_path = os.path.abspath(code_path)
    host_dir = os.path.dirname(code_path)
    container_path = f"/sandbox/{os.path.basename(code_path)}"
    
    logger.debug(f"Host directory: {host_dir}")
    logger.debug(f"Container path: {container_path}")
    
    # Check if Docker image exists
    logger.debug("Checking if Docker image exists")
    try:
        subprocess.run(['docker', 'image', 'inspect', 'autocoder_agent_sandbox'], 
                      check=True, capture_output=True)
        logger.debug("Docker image exists")
    except subprocess.CalledProcessError:
        logger.debug("Docker image not found, building...")
        # Get the correct path to Dockerfile - it's in the sandbox directory
        dockerfile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sandbox', 'Dockerfile')
        logger.debug(f"Using Dockerfile at: {dockerfile_path}")
        
        if not os.path.exists(dockerfile_path):
            logger.error(f"Dockerfile not found at: {dockerfile_path}")
            raise FileNotFoundError(f"Dockerfile not found at: {dockerfile_path}")
            
        # Build Docker image
        logger.info("Building Docker image...")
        build_result = subprocess.run(
            ['docker', 'build', '-t', 'autocoder_agent_sandbox', '-f', dockerfile_path, os.path.dirname(dockerfile_path)],
            capture_output=True,
            text=True
        )
        
        if build_result.returncode != 0:
            logger.error(f"Docker build failed:\n{build_result.stderr}")
            raise subprocess.CalledProcessError(build_result.returncode, build_result.args, build_result.stdout, build_result.stderr)
            
        logger.debug("Docker image built successfully")
    
    try:
        # Run code in container
        logger.info("Running in Docker container...")
        # Convert Windows path to Docker-friendly format
        docker_host_dir = host_dir.replace('\\', '/').replace(':', '')
        if host_dir.startswith('N:'):
            docker_host_dir = '/n' + docker_host_dir[1:]
        cmd = ['docker', 'run', '--rm', '-v', f'{docker_host_dir}:/sandbox']
        if env_var:
            cmd.extend(['-e', env_var])
        cmd.extend(['autocoder_agent_sandbox', 'pytest', container_path])
        
        run_result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        # Always return the output, even if tests fail
        logger.debug("Docker container execution completed")
        return run_result.stdout, run_result.stderr
        
    finally:
        if cleanup:
            logger.info("Cleaning up Docker container...")
            cleanup_docker_container()
