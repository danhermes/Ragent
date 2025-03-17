# Ragents/main.py

import streamlit as st
import os
from view import AudioView
from dotenv import load_dotenv
from agents import DEFAULT_AGENT, AgentCliff, AgentNevil
import logging


#RUN: streamlit run main.py --logger.level=debug        
# Load environment variables
load_dotenv()

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

# Configure Streamlit page
st.set_page_config(initial_sidebar_state="collapsed")

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please set OPENAI_API_KEY in your .env file")
    st.stop()

def main():
    # Initialize AudioView only once using session state
    if 'audio_view' not in st.session_state:
        # Add agent selection
        agent_type = st.sidebar.radio(
            "Choose your agent:",
            ("Cliff", "Nevil"),
            index=0  # Default to Cliff
        )
        
        # Initialize the appropriate agent
        agent = AgentCliff() if agent_type == "Cliff" else AgentNevil()
        
        # Initialize AudioView with the selected agent
        st.session_state.audio_view = AudioView(agent=agent)
    
    # Use the existing AudioView instance
    st.session_state.audio_view.audio_view()

if __name__ == "__main__":
    main()
