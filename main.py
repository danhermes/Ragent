# Ragents/main.py

import streamlit as st
import os
from view import AudioView
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please set OPENAI_API_KEY in your .env file")
    st.stop()

def main():
    st.title("NEVIL")
    audio_view_instance = AudioView()
    audio_view_instance.audio_view()

if __name__ == "__main__":
    main()
