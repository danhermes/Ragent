from typing import Dict, Optional
from pathlib import Path
import logging
from ...proof.proof_API_client import ProofAPIClient, ProofService
from datetime import datetime

class ProofAdapter:
    """Adapter that bridges ragers proofing requirements with proof API"""
    
    def __init__(self, logger=None):
        self.client = ProofAPIClient()
        self.logger = logger or logging.getLogger("proof_adapter")
        
    def proof_text(self, text: str, requirements: Dict) -> Optional[Path]:
        """Proof text using proof API based on ragers requirements"""
        try:
            # Create proofing request
            request = {
                "text": text,
                "requirements": requirements # TODO: Add requirements to proofing request with ChatGPT
            }
            
            # Get proofed text from API
            result = self.client.check_text(text)
            
            self.logger.info(f"Proofing result: {result}")
            
            if not result:
                self.logger.error("Proof API failed to process text")
                return None
                
            # Apply corrections to get proofed text
            proof_service = ProofService(self.client)
            proofed_text = proof_service.apply_corrections(text, result)
                
            # Save proofed text to file in deliverables directory
            deliverables_dir = Path("deliverables")
            deliverables_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            proof_file = deliverables_dir / f"proofed_{timestamp}.txt"
            
            with open(proof_file, 'w', encoding='utf-8') as f:
                f.write(proofed_text)
                
            # Log and print the proofed text
            self.logger.info(f"Proofed text saved to: {proof_file}")
            self.logger.info("Proofed text content:")
            self.logger.info("-" * 80)
            self.logger.info(proofed_text)
            self.logger.info("-" * 80)
            
            print(f"\nProofed text saved to: {proof_file}")
            print("Proofed text content:")
            print("-" * 80)
            print(proofed_text)
            print("-" * 80)
                
            return proof_file
            
        except Exception as e:
            self.logger.error(f"Error proofing text: {str(e)}")
            return None 