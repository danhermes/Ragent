import streamlit as st
import numpy as np
import os
import time
import logging
from helpers.audio_handler import AudioHandler
from agents import DEFAULT_AGENT
from agents.base_agent import AgentType
import re

# Configure logging
logger = logging.getLogger("streamlit")
logger.setLevel(logging.DEBUG)
# Add console handler if not already present
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(console_handler)

class AgentView:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AgentView, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, agent=None):
        # Check if already initialized
        if hasattr(self, 'initialized'):
            logger.warning("AgentView already initialized, reusing existing instance")
            return
            
        logger.info("Initializing AgentView...")
        self.initialized = True
        
        # Initialize audio handler
        self.audio_handler = AudioHandler()
        
        # Initialize agent
        if agent is None:
            agent = DEFAULT_AGENT()
        
        self.agent = agent
        
        # Initialize session state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'timing_container' not in st.session_state:
            st.session_state.timing_container = st.empty()
        if 'chat_container' not in st.session_state:
            st.session_state.chat_container = st.container()
            st.session_state.container_refresh = st.session_state.chat_container.empty()
            
        # Initialize UI and start audio processing
        self.init_page()

    def init_page(self):
        """Initialize the page UI and start audio processing"""

        # Format agent name
        agent_name = "Agent " + self.agent.__class__.__name__.replace("Agent", "")
        
        # Create header once
        st.markdown("""
        <style>
        /* Remove default Streamlit padding */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Fixed header - reduced height */
        .header-container {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 30px;
            background: #ffffff;
            z-index: 1;
            padding: 0.25rem;
            border-bottom: 1px solid #eee;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .header-container h1 {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
            color: #000000;
        }
        
        /* Chat container positioning */
        .chat-container {
            position: fixed;
            top: 40px;
            left: 0;
            right: 0;
            bottom: 0;
            padding: 0.25rem;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            color: #000000;
            position: relative;
            z-index: 10;
            overflow-y: auto;
            max-height: calc(100vh - 40px);
        }
        
        .messages-wrapper {
            display: flex;
            flex-direction: column;
            gap: 10px;
            min-height: 100%;
            padding-bottom: 20px;
        }
               
        .chat-message {
            margin-bottom: 2rem;
            background: #ffffff;  /* Ensure messages have white background */
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .term {
            font-size: 23px;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #000000;
        }
        
        .first-sentence {
            font-size: 18px;
            margin-bottom: 0.15rem;
            color: #000000;
        }
        
        .remaining-text {
            font-size: 15px;
            color: #000000;
            margin-top: 0.15rem;
            line-height: 1.3;
        }

        /* Ensure Streamlit components don't overlap */
        .stApp {
            margin-top: 30px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Create main container with header
        st.markdown(f"""
        <div class="header-container">
            <h1>{agent_name}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Create chat container with explicit height
        chat_html = '''
        <div class="chat-container" id="chat-container">
            <div class="messages-wrapper">
            </div>
        </div>
        '''
        st.session_state.chat_container.markdown(chat_html, unsafe_allow_html=True)
        
        # Add scroll behavior
        # st.markdown("""
        #     <script>
        #         const container = document.getElementById('chat-container');
        #         function scrollToBottom() {
        #             container.scrollTop = container.scrollHeight;
        #             // Double-check scroll position after a short delay
        #             setTimeout(() => {
        #                 container.scrollTop = container.scrollHeight;
        #             }, 100);
        #         }
        #         // Initial scroll
        #         scrollToBottom();
        #         // Watch for changes
        #         const observer = new MutationObserver(scrollToBottom);
        #         observer.observe(container, { childList: true, subtree: true });
        #     </script>
        # """, unsafe_allow_html=True)
       
        def handle_response(response):
            """Handle response from audio processing"""
            if self.agent.agent_type == AgentType.TEXT:
                self.text_display_view(response)
            else:
                st.audio(response, format='audio/wav', start_time=0)
        
        # Start audio processing
        self.audio_handler.process_audio_stream(self.agent, handle_response)

    def text_display_view(self, text: str) -> None:
        """Display text responses in the chat interface"""
        # Guardrails: Skip ChatGPT apologies
        if "sorry" in text.lower() or "apologies" in text.lower():
            return
            
        # Add response to chat history
        st.session_state.chat_history.append(text)
        
        # Update the chat container content
        if 'chat_container' in st.session_state:
            logger.info("Updating UI with new message...")
            
            # # Build complete chat HTML
            # chat_html = '''
            # <div class="chat-container" id="chat-container">
            #     <div class="messages-wrapper">
            # '''
            # # Add all messages in order (newest first)
            # for message in st.session_state.chat_history:
            #     chat_html += self.format_message(message)
                
            # chat_html += '''
            #     </div>
            # </div>
            # '''
            
            text_html=self.format_message(text)

            # Update the entire container
            st.session_state.chat_container.markdown(text_html, unsafe_allow_html=True)

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'audio_handler'):
            # Set stop flag first
            self.audio_handler.should_stop = True
            # Then do cleanup
            self.audio_handler.cleanup()
        if 'audio_view_running' in st.session_state:
            st.session_state.audio_view_running = False

    def __del__(self):
        """Ensure cleanup on deletion"""
        self.cleanup() 
        
    def format_message(self, text):
        # Split the text into separate entries based on double newlines or ---
        entries = re.split(r'\n\s*---\s*\n|\n\s*\n\s*\n', text)
        
        formatted_entries = []
        for entry in entries:
            # Remove leading/trailing whitespace while preserving internal newlines
            entry = entry.strip()
            
            # Look for the term at the start (any text up to first newline)
            match = re.match(r'^([^\n]+)\n(.*)$', entry, re.DOTALL)
            if match:
                term, content = match.groups()
                # Clean up the term
                term = term.strip()
                term = re.sub(r'\*\*|\*|#\s*', '', term)  # Remove any markdown
                
                # Process the content
                content = content.strip()
                
                # Split into first sentence and remaining text
                sentence_match = re.match(r'^([^.!?]+[.!?])\s*(.*)$', content, re.DOTALL)
                if sentence_match:
                    first_sentence, remaining = sentence_match.groups()
                    remaining = remaining.strip()
                    formatted_entries.append(
                        f'<div class="chat-message">'
                        f'<div class="term">{term}</div>'
                        f'<div class="first-sentence">{first_sentence.strip()}</div>'
                        f'<div class="remaining-text">{remaining}</div>'
                        f'</div>'
                    )
                else:
                    # If no clear sentence break, treat all content as first sentence
                    formatted_entries.append(
                        f'<div class="chat-message">'
                        f'<div class="term">{term}</div>'
                        f'<div class="first-sentence">{content}</div>'
                        f'</div>'
                    )
            else:
                # If no clear term found, treat entire entry as content
                formatted_entries.append(
                    f'<div class="chat-message">'
                    f'<div class="first-sentence">{entry}</div>'
                    f'</div>'
                )
        
        return ''.join(formatted_entries) 