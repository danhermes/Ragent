# Ragents/main.py

import streamlit as st
import os
from view import AudioView
from dotenv import load_dotenv
from agents import DEFAULT_AGENT, AgentCliff, AgentNevil
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
st.set_page_config(initial_sidebar_state="collapsed")
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
        
        # Initialize AudioView only once using session state
        if 'audio_view' not in st.session_state:
            print("Initializing AudioView...")  # Immediate print to verify execution
            logger.debug("Initializing AudioView in session state...")
            
            # Add agent selection
            logger.debug("Setting up agent selection...")
            agent_type = st.sidebar.radio(
                "Choose your agent:",
                ("Cliff", "Nevil"),
                index=0  # Default to Cliff
            )
            
            # Initialize the appropriate agent
            logger.debug(f"Initializing {agent_type} agent...")
            agent = AgentCliff() if agent_type == "Cliff" else AgentNevil()
            logger.info(f"Agent initialized: {agent.__class__.__name__}")
            
            # Initialize AudioView with the selected agent
            logger.debug("Creating AudioView instance...")
            st.session_state.audio_view = AudioView(agent=agent)
            logger.info("AudioView instance created successfully")
        
        # Use the existing AudioView instance
        logger.debug("Starting audio view...")
        st.session_state.audio_view.audio_view()
        logger.info("Audio view started successfully")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")  # Immediate print to verify execution
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        raise
    finally:
        print("Main function finished")  # Immediate print to verify execution
        logger.info("Main application finished")

if __name__ == "__main__":
    print("Starting script...")  # Immediate print to verify execution
    main()
    print("Script finished")  # Immediate print to verify execution
