# Ragents/main.py

import streamlit as st
from dotenv import load_dotenv
import os
from views.agent_view import AgentView
from agents.agent_cliff import AgentCliff
from agents.agent_nevil import AgentNevil
import logging
import sys

print("Script starting...")  # Immediate print to verify execution

#RUN: streamlit run main.py --logger.level=debug        
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('streamlit_debug.log')
    ]
)
logger = logging.getLogger("main")
logger.info("Logging Setup.")

print("Logging configured...")  # Immediate print to verify execution

# Configure Streamlit page
print("Configuring Streamlit...")  # Immediate print to verify execution
st.set_page_config(
    page_title="AI Agents",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)
print("Streamlit configured...")  # Immediate print to verify execution

# Get API key from environment variable
print("Checking API key...")  # Immediate print to verify execution
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("No API key found!")  # Immediate print to verify execution
    st.error("Please set OPENAI_API_KEY in your .env file")
    st.stop()

def main():
    print("Main function starting...")  # Immediate print to verify execution
    try:
        logger.info("Starting main application...")
        
        # Initialize AgentView if not already in session state
        if "agent_view" not in st.session_state:
            print("Initializing AgentView...")  # Immediate print to verify execution
            logger.debug("Initializing AgentView in session state...")
            
            # Add agent selection
            logger.debug("Setting up agent selection...")
            agent_type = st.sidebar.radio(
                "Choose your agent:",
                ["Cliff", "Nevil"],
                index=0,
                label_visibility="collapsed"
            )
            
            # Initialize the appropriate agent
            logger.debug(f"Initializing {agent_type} agent...")
            if agent_type == "Cliff":
                agent = AgentCliff()
            else:
                agent = AgentNevil()
            logger.info(f"Agent initialized: {agent.__class__.__name__}")
            
            # Initialize AgentView with the selected agent
            logger.debug("Creating AgentView instance...")
            st.session_state.agent_view = AgentView(agent)
            logger.info("AgentView instance created successfully")
        
        # Use the existing AgentView instance
        logger.debug("Starting agent view...")
        st.session_state.agent_view.agent_view()
        logger.info("Agent view started successfully")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")  # Immediate print to verify execution
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        raise
    finally:
        print("Main function finished")  # Immediate print to verify execution
        logger.info("Main application finished")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")
        if "agent_view" in st.session_state:
            st.session_state.agent_view.cleanup()
