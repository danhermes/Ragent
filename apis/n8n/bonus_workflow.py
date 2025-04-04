from n8n_workflow_helper import N8nWorkflowHelper
from config import N8nConfig
import logging
import json
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bonus_workflow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_bonus_workflow() -> None:
    """Create a bonus workflow that demonstrates advanced features
    
    This workflow:
    1. Runs daily at 9 AM
    2. Extracts data from a Dropbox Excel file
    3. Filters the data based on conditions
    4. Uses OpenAI to analyze the filtered data
    5. Sends an email report with the analysis
    6. Uploads the results back to Dropbox
    """
    logger.info("Starting bonus workflow creation")
    
    # Create config at the application level
    config = N8nConfig()
    logger.info("Created N8nConfig instance")
    
    # Pass config to workflow helper
    helper = N8nWorkflowHelper(config)
    logger.info("Initialized N8nWorkflowHelper")
    
    # Create nodes
    nodes = []
    
    # 1. Schedule Trigger (runs daily at 9 AM)
    logger.info("Creating Schedule Trigger node")
    schedule_node = helper.create_schedule_trigger(
        name="Daily Schedule",
        trigger_at_hour=9,
        interval="days"
    )
    schedule_node["position"] = [100, 100]  # Starting position
    nodes.append(schedule_node)
    
    # 2. Dropbox List Folder (to get the latest Excel file)
    logger.info("Creating Dropbox List Folder node")
    list_folder_node = helper.create_dropbox_list_folder(
        name="List Excel Files",
        folder_path="/Reports"
    )
    list_folder_node["position"] = [300, 100]  # Right of Schedule
    nodes.append(list_folder_node)
    
    # 3. Filter node to get the latest Excel file
    logger.info("Creating Filter node for latest Excel")
    filter_node = helper.create_filter(
        name="Get Latest Excel",
        conditions=[
            {
                "value1": "={{$json['name']}}",
                "value2": ".xlsx",
                "operation": "contains"
            }
        ],
        combinator="and"
    )
    filter_node["position"] = [500, 100]  # Right of List Folder
    nodes.append(filter_node)
    
    # 4. Extract from XLSX
    logger.info("Creating Extract XLSX node")
    extract_node = helper.create_extract_xlsx(
        name="Extract Data",
        sheet_name="Sheet1",
        range="A1:D100"
    )
    extract_node["position"] = [700, 100]  # Right of Filter
    nodes.append(extract_node)
    
    # 5. Filter data based on conditions
    logger.info("Creating Data Filter node")
    data_filter_node = helper.create_filter(
        name="Filter Data",
        conditions=[
            {
                "value1": "={{$json['status']}}",
                "value2": "pending",
                "operation": "equal"
            }
        ],
        combinator="and"
    )
    data_filter_node["position"] = [900, 100]  # Right of Extract
    nodes.append(data_filter_node)
    
    # 6. OpenAI Analysis
    logger.info("Creating OpenAI Analysis node")
    openai_node = helper.create_openai_message(
        name="Analyze Data",
        model="gpt-4",
        prompt="Analyze the following data and provide insights:\n{{$json}}"
    )
    openai_node["position"] = [1100, 100]  # Right of Data Filter
    nodes.append(openai_node)
    
    # 7. Edit Fields to format email content
    logger.info("Creating Edit Fields node")
    edit_fields_node = helper.create_edit_fields(
        name="Format Email",
        fields={
            "subject": "Daily Data Analysis Report",
            "body": "={{$json['choices'][0]['message']['content']}}"
        }
    )
    edit_fields_node["position"] = [1300, 100]  # Right of OpenAI
    nodes.append(edit_fields_node)
    
    # 8. Send Email
    logger.info("Creating Send Email node")
    email_node = helper.create_send_email(
        name="Send Report",
        to_email="team@example.com",
        subject="={{$json['subject']}}",
        body="={{$json['body']}}"
    )
    email_node["position"] = [1500, 0]  # Below Edit Fields
    nodes.append(email_node)
    
    # 9. Convert to XLSX for storage
    logger.info("Creating Convert to XLSX node")
    convert_node = helper.create_convert_to_xlsx(
        name="Convert Results",
        sheet_name="Analysis Results"
    )
    convert_node["position"] = [1500, 200]  # Below Edit Fields, right of Send Email
    nodes.append(convert_node)
    
    # 10. Upload to Dropbox
    logger.info("Creating Dropbox Upload node")
    upload_node = helper.create_dropbox_upload(
        name="Upload Results",
        folder_path="/Analysis Results",
        file_name="daily_analysis_{{Date.now()}}.xlsx"
    )
    upload_node["position"] = [1700, 200]  # Right of Convert
    nodes.append(upload_node)
    
    # Create connections between nodes
    connections = {}
    
    # Connect nodes in sequence
    logger.info("Creating node connections")
    
    # Connect Schedule to List Folder
    connections["Daily Schedule"] = {
        "main": [[{"node": "List Excel Files", "type": "main"}]]
    }
    
    # Connect List Folder to Filter
    connections["List Excel Files"] = {
        "main": [[{"node": "Get Latest Excel", "type": "main"}]]
    }
    
    # Connect Filter to Extract
    connections["Get Latest Excel"] = {
        "main": [[{"node": "Extract Data", "type": "main"}]]
    }
    
    # Connect Extract to Data Filter
    connections["Extract Data"] = {
        "main": [[{"node": "Filter Data", "type": "main"}]]
    }
    
    # Connect Data Filter to OpenAI
    connections["Filter Data"] = {
        "main": [[{"node": "Analyze Data", "type": "main"}]]
    }
    
    # Connect OpenAI to Edit Fields
    connections["Analyze Data"] = {
        "main": [[{"node": "Format Email", "type": "main"}]]
    }
    
    # Connect Edit Fields to Send Email
    connections["Format Email"] = {
        "main": [[{"node": "Send Report", "type": "main"}]]
    }
    
    # Connect Edit Fields to Convert (parallel path)
    connections["Format Email"]["main"].append([{"node": "Convert Results", "type": "main"}])
    
    # Connect Convert to Upload
    connections["Convert Results"] = {
        "main": [[{"node": "Upload Results", "type": "main"}]]
    }
    
    # Create the workflow in n8n
    logger.info("Submitting workflow to n8n")
    workflow = helper.create_workflow(
        name="Daily Data Analysis Workflow",
        nodes=nodes,
        connections=connections
    )
    
    # Save workflow JSON to file for reference
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    workflow_file = f"logs/workflow_{timestamp}.json"
    logger.info(f"Saving workflow JSON to {workflow_file}")
    
    with open(workflow_file, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    logger.info(f"Successfully created bonus workflow with ID: {workflow.get('id')}")
    logger.info("Workflow creation completed")

if __name__ == "__main__":
    create_bonus_workflow() 