from n8n_api_client import N8nApiClient
from config import N8nConfig
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_workflow():
    """Verify that the workflow was created successfully"""
    config = N8nConfig()
    client = N8nApiClient(config)
    
    try:
        # Get all workflows
        workflows = client.get_workflows()
        logger.info(f"Found {len(workflows.get('data', []))} workflows")
        
        # Get our specific workflow
        workflow = client.get_workflow("1")
        logger.info(f"Workflow details: {workflow}")
        
        # Check if it's active
        if workflow.get('active'):
            logger.info("Workflow is active!")
        else:
            logger.info("Workflow is not active")
            
    except Exception as e:
        logger.error(f"Error verifying workflow: {str(e)}")

if __name__ == "__main__":
    verify_workflow() 