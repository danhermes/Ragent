import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class N8nConfig:
    """Configuration for n8n integration"""
    
    def __init__(self):
        self.base_url = os.getenv('N8N_BASE_URL', 'http://localhost:5678').rstrip('/')
        self.api_key = os.getenv('N8N_API_KEY')
        
        if not self.api_key:
            raise ValueError("n8n API key not found. Please set N8N_API_KEY in .env file.")
            
        self.headers = {
            'X-N8N-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        } 