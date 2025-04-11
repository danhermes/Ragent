import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional, Dict

# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class N8nConfig:
    """Configuration for n8n API"""
    
    def __init__(self):
        self.api_url = os.getenv("N8N_BASE_URL", "http://localhost:5678")
        self.api_key = os.getenv("N8N_API_KEY", "")
        
    def __str__(self) -> str:
        return f"N8nConfig(api_url={self.api_url}, api_key=***)"
        
    def __repr__(self) -> str:
        return self.__str__()

    def get_headers(self):
        return {
            'X-N8N-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        } 