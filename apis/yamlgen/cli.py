import argparse
import sys
from pathlib import Path
from typing import Optional
import yaml
import os
from datetime import datetime

from yaml_parser import YamlParser
from yaml_generator import YAMLGenerator

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate tool-specific YAML files from structured templates"
    )
    parser.add_argument(
        "--input-file",
        required=True,
        help="Path to input template file (YAML/JSON)"
    )
    parser.add_argument(
        "--tool",
        required=True,
        choices=["autocoder", "litlegos", "n8n", "proof"],
        help="Target tool for YAML generation"
    )
    parser.add_argument(
        "--output",
        help="Path to save output YAML (default: stdout)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed parsing and generation steps"
    )
    return parser.parse_args()

def create_project_structure(project_name: str) -> Path:
    """Create project directory structure and return the project path."""
    base_path = Path("projects") / project_name
    dirs = [
        base_path / "specs",
        base_path / "yaml",
        base_path / "logs"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return base_path

def generate_yaml(
    input_file: str,
    tool: str,
    output: Optional[str] = None,
    verbose: bool = False
) -> None:
    """Generate YAML for specified tool from input template."""
    try:
        # Parse input file
        if verbose:
            print(f"Parsing input file: {input_file}")
        parser = YamlParser(input_file)
        spec = parser.load()
        unified_spec = parser.to_unified_spec()

        # Get project name from spec
        project_name = unified_spec.get("project", "untitled_project")
        project_path = create_project_structure(project_name)

        # Generate tool-specific YAML
        if verbose:
            print(f"Generating {tool} YAML...")
        generator = YAMLGenerator(unified_spec)
        
        # Get the appropriate generation method
        generate_method = getattr(generator, f"generate_{tool}_yaml")
        yaml_content = generate_method()

        # Save input spec
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        spec_path = project_path / "specs" / f"input_spec_{timestamp}.yaml"
        with open(spec_path, "w") as f:
            yaml.dump(spec, f, sort_keys=False)
        if verbose:
            print(f"Input spec saved to: {spec_path}")

        # Save unified spec
        unified_spec_path = project_path / "specs" / f"unified_spec_{timestamp}.yaml"
        with open(unified_spec_path, "w") as f:
            yaml.dump(unified_spec, f, sort_keys=False)
        if verbose:
            print(f"Unified spec saved to: {unified_spec_path}")

        # Output the result
        if output:
            output_path = Path(output)
        else:
            output_path = project_path / "yaml" / f"{tool}_{timestamp}.yaml"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            yaml.dump(yaml_content, f, sort_keys=False)
        if verbose:
            print(f"YAML saved to: {output_path}")

        # Create log entry
        log_path = project_path / "logs" / f"generation_{timestamp}.log"
        with open(log_path, "w") as f:
            f.write(f"Generated {tool} YAML at {timestamp}\n")
            f.write(f"Input file: {input_file}\n")
            f.write(f"Output file: {output_path}\n")
            if verbose:
                f.write("Verbose mode enabled\n")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point."""
    args = parse_args()
    generate_yaml(
        input_file=args.input_file,
        tool=args.tool,
        output=args.output,
        verbose=args.verbose
    )

if __name__ == "__main__":
    main() 