# Ragents/main.py

import streamlit as st
from dotenv import load_dotenv
import os
from views.agent_view import AgentView
from agents.agent_cliff import AgentCliff
from agents.agent_nevil import AgentNevil

#RUN: streamlit run main.py --logger.level=debug        

def main():
    # Load environment variables
    load_dotenv()
    
    # Configure page
    st.set_page_config(
        page_title="AI Agents",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Please set your OpenAI API key in the .env file")
        return
    
    # Sidebar for agent selection
    with st.sidebar:
        st.title("Select Agent")
        agent_type = st.radio(
            "Choose your agent:",
            ["Cliff", "Nevil"],
            index=0,
            label_visibility="collapsed"
        )
    
    # Initialize AgentView if not already in session state
    if "agent_view" not in st.session_state:
        # Create appropriate agent based on selection
        if agent_type == "Cliff":
            agent = AgentCliff()
        else:
            agent = AgentNevil()
            
        # Initialize AgentView with the selected agent
        st.session_state.agent_view = AgentView(agent)

if __name__ == "__main__":
    main()
