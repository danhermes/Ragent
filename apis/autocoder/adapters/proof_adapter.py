from typing import Dict, Optional
from pathlib import Path
from ...proof.proof_API_client import ProofAPIClient

class ProofAdapter:
    """Adapter that bridges ragers proofing requirements with proof API"""
    
    def __init__(self):
        self.client = ProofAPIClient()
        
    def proof_text(self, text: str, requirements: Dict) -> Optional[Path]:
        """Proof text using proof API based on ragers requirements"""
        try:
            # Create proofing request
            request = {
                "text": text,
                "requirements": requirements
            }
            
            # Get proofed text from API
            result = self.client.proof_text(request)
            
            if not result or "proofed_text" not in result:
                self.logger.error("Proof API failed to process text")
                return None
                
            # Save proofed text to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            proof_file = Path(f"proofed_{timestamp}.txt")
            
            with open(proof_file, 'w', encoding='utf-8') as f:
                f.write(result["proofed_text"])
                
            return proof_file
            
        except Exception as e:
            self.logger.error(f"Error proofing text: {str(e)}")
            return None 