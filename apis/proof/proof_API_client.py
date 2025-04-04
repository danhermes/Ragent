import requests
import json
import os
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from pathlib import Path

class ProofAPIClient:
    """Client for interacting with the LanguageTool API"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.logger = logging.getLogger("proof_api_client")
        self.logger.setLevel(logging.INFO)
        
        # Load environment variables
        env_path = Path(__file__).resolve().parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path, override=True)
        
        # Use provided base_url or get from env
        self.base_url = base_url or os.getenv('LANGUAGE_TOOL_API_URL')
        if not self.base_url:
            self.logger.error("LANGUAGE_TOOL_API_URL not found in environment variables")
            raise ValueError("LANGUAGE_TOOL_API_URL environment variable is required")
            
        # Ensure base_url ends with /v2
        if not self.base_url.endswith('/v2'):
            self.base_url = f"{self.base_url.rstrip('/')}/v2"
            
        self.logger.info(f"Initialized Proof API client with base URL: {self.base_url}")

    def _request(self, endpoint: str, method: str = "POST", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the LanguageTool API. Args: endpoint (str): API endpoint, method (str): HTTP method, data (Dict[str, Any]): Request data. Returns: Dict[str, Any]: API response."""
        url = f"{self.base_url}{endpoint}"
        self.logger.debug(f"Proofing now.")
        self.logger.debug(f"Making {method} request to {url}")
        if data:
            self.logger.debug(f"Request data: {json.dumps(data, indent=2)}")
        
        try:
            response = requests.request(method, url, data=data)
            response.raise_for_status()
            
            response_data = response.json()
            self.logger.debug(f"Response: {json.dumps(response_data, indent=2)}")
            self.logger.debug(f"Proofing complete.")
            
            return response_data
            
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error: {str(e)}")
            raise ConnectionError("Could not connect to LanguageTool API. Make sure the Docker container is running.")
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            if e.response.status_code == 400:
                raise ValueError(f"Invalid request to LanguageTool API: {e.response.text}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse response: {str(e)}")
            raise ValueError(f"Invalid response from LanguageTool API: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise

    def check_text(self, text: str, language: str = "en-US") -> Dict[str, Any]:
        """Check text for grammar, spelling, and style issues. Args: text (str): Text to check, language (str): Language code. Returns: Dict[str, Any]: API response with matches."""
        data = {
            "text": text,
            "language": language,
            "enabledOnly": "false"
        }
        self.logger.info(f"Checking text: {text[:50]}...")
        response = self._request("/check", data=data)
        self.logger.info(f"Found {len(response.get('matches', []))} issues")
        return response

class ProofService:
    """Service for text proofreading using LanguageTool"""
    
    def __init__(self, api_client: Optional[ProofAPIClient] = None):
        self.logger = logging.getLogger("proof_service")
        self.logger.setLevel(logging.INFO)
        self.api = api_client or ProofAPIClient()
        self.logger.info("Initialized Proof Service")

    def check_text(self, text: str) -> Dict[str, Any]:
        """Check text for issues. Args: text (str): Text to check. Returns: Dict[str, Any]: API response with matches."""
        return self.api.check_text(text)

    def apply_corrections(self, text: str, matches: Dict[str, Any]) -> str:
        """Apply corrections to text. Args: text (str): Original text, matches (Dict[str, Any]): API response with matches. Returns: str: Corrected text."""
        corrected_text = text
        issue_count = 0
        
        for match in reversed(matches.get("matches", [])):
            if match.get("replacements"):
                start = match["offset"]
                end = start + match["length"]
                replacement = match["replacements"][0]["value"]
                corrected_text = corrected_text[:start] + replacement + corrected_text[end:]
                issue_count += 1
        
        self.logger.info(f"Applied {issue_count} corrections")
        return corrected_text

if __name__ == "__main__":
    test_text = "This is a test text with some grammer mistakes and spelling erors."
    try:
        proof_service = ProofService()
        issues = proof_service.check_text(test_text)
        print("Found issues:", json.dumps(issues, indent=2))
        corrected = proof_service.apply_corrections(test_text, issues)
        print("Corrected text:", corrected)
    except ConnectionError as e:
        print(f"Error: {str(e)}")
        print("Run: docker run -d -p 8010:8010 --name languagetool erikvl87/languagetool")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}") 