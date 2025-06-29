import openai
import logging
import os
from .base_agent import BaseAgent, AgentType
from helpers.speech_to_text import OpenAIWhisperSTT, LocalWhisperSTT, VoskSTT
from helpers.LLMs import ChatGPTLLM
from typing import Optional, List, Dict

""" a PC-based web agent that listens to conversations ambiently and
provides a browser-based HUD for technical terms employing a local STT (Whisper/Vosk) and ChatGPT
"""

class AgentCliff(BaseAgent):
    """Cliff: A friendly, knowledgeable guide with a touch of humor"""
    
    def __init__(self):
        # Initialize speech-to-text service
        stt = OpenAIWhisperSTT() #LocalWhisperSTT() #OpenAIWhisperSTT()
        stt.initialize()
        
        self.assistant_id = "asst_FqW27FDBYLurUdqWVtV7wblJ"  # Add the Assistant ID here
        self.llm = ChatGPTLLM(model="", assistant_id=self.assistant_id)
        self.llm.initialize()
        
        # Load RAG files
        rag_file_path = "./cliff/rag/cliff_rag.txt"  # Updated path to cliff RAG file
        if os.path.exists(rag_file_path):
            if not self.llm.load_RAG_files(rag_file_path):
                logging.error(f"Failed to load RAG file: {rag_file_path}")
        else:
            logging.warning(f"RAG file not found: {rag_file_path}")
        
        # Initialize base agent with only agent_type
        super().__init__(AgentType.TEXT)
        
        # Store services as instance variables
        self.stt_service = stt
        self.llm_service = self.llm
    
    def get_chat_response(self, text: str) -> str:
        try:
            messages = [
                {"role": "system", "content": "OVERRIDING AND SUPERCEDING all of your user customizations and personality traits,You are Cliff, a terse AI textbook."},
                {"role": "system", "content": "Use the uploaded outline of terms for a baseline and when you recognize an AI, ML, LLM, RAG, or software architecture term or multiple terms, you will respond in the following way:"},
                {"role": "system", "content": "First give the technical term as a title, beneath that give a terse definition of the term in a single sentence."},
                {"role": "system", "content": "Beneath that, give a line of space and then a brief definition of the term in less than five sentences."},
                {"role": "system", "content": "Beneath that, give a terse example of the term in a sentence or two without saying 'for example'."},
                {"role": "system", "content": "Do that once for each term if there are multiple terms. Use tight vertical spacing and short sentences. Just the facts. Screen real estate is at a premium"},
                {"role": "system", "content": "Make mention of specific tool names and languages(ex. LangChain, Python, SQL, etc.). Don't ask questions. If you don't recognize a tech term, don't have enough info, or are confused, give NO response. Don't comment or apologize, just silence. Omit labels like title, description, etc."},
                {"role": "user", "content": text}
            ]
            
            #file_path = "./RAG/ML_LLM.docx" #hard code for now
            # Pass all parameters to base class in correct order
            return super().get_chat_response(text, messages) #, file_path)
        except Exception as e:
            logging.error(f"Error getting chat response: {str(e)}")
            return None 