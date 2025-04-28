import argparse
import sys
import os
from datetime import datetime
import logging
from pathlib import Path
from apis.yamlgen.modules.yamlgen_dispatcher import YAMLgenDispatcher

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/cli_{timestamp}.log"

# Create handlers
file_handler = logging.FileHandler(log_file, encoding='utf-8')
console_handler = logging.StreamHandler()

# Set formatters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, console_handler]
)

# Configure specific loggers
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configure other loggers
logging.getLogger('openai').setLevel(logging.DEBUG)
logging.getLogger('httpcore').setLevel(logging.DEBUG)
logging.getLogger('httpx').setLevel(logging.DEBUG)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YAMLgen CLI - Generate YAMLs from Automation Tech Specs")
    parser.add_argument("--input-file", required=True, help="Path to input .md file")
    parser.add_argument("--tool", required=True, choices=["autocoder", "n8n", "proof", "litlegos"], help="Target tool")
    parser.add_argument("--enhance", action="store_true", help="Enhance spec using Elias (OpenAI)")
    parser.add_argument("--output", help="Optional path to save generated YAML")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()

def main():
    args = parse_args()
    dispatcher = YAMLgenDispatcher()

    # Set default output path if not provided
    output_path = args.output
    if output_path is None:
        output_dir = Path("./apis/yamlgen/generated_yamls")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{args.tool}.yaml"

    try:
        dispatcher.generate_yaml(
            input_path=args.input_file,
            tool=args.tool,
            enhance=args.enhance,
            output_path=str(output_path),
            verbose=args.verbose
        )
        logger.info("YAML generation complete.")
        logger.info(f"Output saved to: {output_path}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()