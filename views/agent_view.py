import streamlit as st
import numpy as np
import os
import time
import logging
from helpers.audio_handler import AudioHandler
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
            logger.info("Cliff interface already initialized")
            return
            
        logger.info("Setting up Cliff interface...")
        self.initialized = True
        
        # Initialize audio handler
        self.audio_handler = AudioHandler()
        
        # Initialize agent - agent must be provided
        if agent is None:
            raise ValueError("Agent must be provided to AgentView")
        
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

        # Format agent name - extract just the name part
        agent_name = self.agent.__class__.__name__.replace("Agent", "")
        
        # Create header CSS first
        st.markdown("""
        <style>
        /* Remove default Streamlit padding and margins */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Hide default Streamlit header */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Fixed header at very top */
        .header-container {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            z-index: 9999;
            padding: 0.75rem 1rem;
            border-bottom: 2px solid #4a5568;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .header-container h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        /* Chat container positioning - moved down to account for larger header */
        .chat-container {
            position: fixed;
            top: 60px;
            left: 0;
            right: 0;
            bottom: 0;
            padding: 1rem;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            color: #000000;
            position: relative;
            z-index: 10;
            overflow-y: auto;
            max-height: calc(100vh - 60px);
            background: #f8f9fa;
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
            background: #ffffff;
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

        /* Status message styling */
        .status-message {
            background: #f0f8ff;
            border-left: 4px solid #4CAF50;
            padding: 0.5rem;
            margin-bottom: 1rem;
            font-size: 14px;
            color: #2c5aa0;
        }
        
        .error-message {
            background: #fff5f5;
            border-left: 4px solid #F44336;
            padding: 0.5rem;
            margin-bottom: 1rem;
            font-size: 14px;
            color: #c53030;
        }
        
        .transcription-message {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 0.5rem;
            margin-bottom: 1rem;
            font-size: 14px;
            color: #1976d2;
        }

        /* Ensure Streamlit components don't overlap */
        .stApp {
            margin-top: 60px;
        }
        
        /* Auto-scroll to bottom */
        .auto-scroll {
            scroll-behavior: smooth;
        }
        </style>
        
        <script>
        // Auto-scroll to bottom when new content is added
        function scrollToBottom() {
            const chatContainer = document.querySelector('.chat-container');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
        
        // Scroll to bottom on page load
        window.addEventListener('load', scrollToBottom);
        
        // Create a MutationObserver to watch for new content
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    // Small delay to ensure content is rendered
                    setTimeout(scrollToBottom, 100);
                }
            });
        });
        
        // Start observing when the page loads
        window.addEventListener('load', function() {
            const chatContainer = document.querySelector('.chat-container');
            if (chatContainer) {
                observer.observe(chatContainer, {
                    childList: true,
                    subtree: true
                });
            }
        });
        </script>
        """, unsafe_allow_html=True)

        # Create main container with prominent header
        st.markdown(f"""
        <div class="header-container">
            <h1>🤖 {agent_name}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Create chat container with explicit height
        chat_html = f'''
        <div class="chat-container">
            <div class="messages-wrapper">
            </div>
        </div>
        '''
        st.session_state.chat_container.markdown(chat_html, unsafe_allow_html=True)
        
        # Show initial status
        self.show_status("listening", "🎧 Listening for speech...")
        
        # Create a single container for all messages that will auto-scroll
        self.messages_container = st.container()
        
        def handle_response(response):
            """Handle response from audio processing"""
            try:
                if self.agent.agent_type == AgentType.TEXT:
                    self.text_display_view(response)
                else:
                    st.audio(response, format='audio/wav', start_time=0)
            except Exception as e:
                logger.error(f"Error in response handler: {str(e)}")
                self.show_error(f"Response error: {str(e)}")
        
        def handle_status(status_type: str, message: str):
            """Handle status updates from audio processing"""
            try:
                self.show_status(status_type, message)
            except Exception as e:
                logger.error(f"Error in status handler: {str(e)}")
        
        def handle_transcription(text: str):
            """Handle transcription updates"""
            try:
                self.show_transcription(text)
            except Exception as e:
                logger.error(f"Error in transcription handler: {str(e)}")
        
        # Start audio processing with status callbacks and error handling
        try:
            logger.info("Starting audio processing...")
            self.audio_handler.process_audio_stream(self.agent, handle_response, handle_status, handle_transcription)
        except Exception as e:
            logger.error(f"Error starting audio processing: {str(e)}")
            self.show_error(f"Failed to start audio processing: {str(e)}")

    def show_status(self, status_type: str, message: str):
        """Show status message in the chat interface"""
        try:
            # Ensure session state exists
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Add status message to chat history
            st.session_state.chat_history.append(f"Status: {message}")
            
            # Display in the messages container (auto-scrolls)
            with self.messages_container:
                status_message = f'<div class="status-message">{message}</div>'
                st.markdown(status_message, unsafe_allow_html=True)
                    
        except Exception as e:
            logger.error(f"Error in show_status: {str(e)}")

    def show_transcription(self, text: str):
        """Show transcribed text in the chat interface"""
        try:
            # Always show the message, including "No speech detected"
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Add transcription message to chat history
            st.session_state.chat_history.append(f"Transcription: {text}")
            
            # Display in the messages container (auto-scrolls)
            with self.messages_container:
                if text == "No speech detected":
                    transcription_message = f'<div class="transcription-message">🔇 {text}</div>'
                else:
                    transcription_message = f'<div class="transcription-message">🎤 Heard: "{text}"</div>'
                st.markdown(transcription_message, unsafe_allow_html=True)
                    
        except Exception as e:
            logger.error(f"Error in show_transcription: {str(e)}")
    
    def show_error(self, error_message: str):
        """Show error message in the chat interface"""
        try:
            # Ensure session state exists
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Add error message to chat history
            st.session_state.chat_history.append(f"Error: {error_message}")
            
            # Display in the messages container (auto-scrolls)
            with self.messages_container:
                error_html = f'<div class="error-message">❌ Error: {error_message}</div>'
                st.markdown(error_html, unsafe_allow_html=True)
                
                # Reset to listening after 3 seconds
                time.sleep(3)
                self.show_status("listening", "🎧 Listening for speech...")
        except Exception as e:
            logger.error(f"Error in show_error: {str(e)}")

    def text_display_view(self, text: str) -> None:
        """Display text responses in the chat interface"""
        try:
            # Guardrails: Skip ChatGPT apologies
            if "sorry" in text.lower() or "could you" in text.lower() or "your message" in text.lower() or "please provide" in text.lower() or "apologies" in text.lower() or "I can assist you" in text.lower():
                return
                
            # Ensure session state exists
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Add response to chat history
            st.session_state.chat_history.append(text)
            
            # Display in the messages container (auto-scrolls)
            with self.messages_container:
                text_html = self.format_message(text)
                st.markdown(text_html, unsafe_allow_html=True)
                
                # Reset status to listening
                self.show_status("listening", "🎧 Listening for speech...")
        except Exception as e:
            logger.error(f"Error in text_display_view: {str(e)}")

    def cleanup(self):
        """Clean up resources when shutting down"""
        try:
            if hasattr(self, 'audio_handler') and self.audio_handler:
                logger.info("Stopping audio handler...")
                self.audio_handler.should_stop = True
                if hasattr(self.audio_handler, 'stream') and self.audio_handler.stream:
                    try:
                        self.audio_handler.stream.stop()
                        self.audio_handler.stream.close()
                    except:
                        pass
                self.audio_handler = None
            logger.info("AgentView cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
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