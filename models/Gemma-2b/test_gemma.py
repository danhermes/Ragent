from agents.GPT_agents.chat_agent import GemmaAgent
import logging

def main():
    # Configure logging to show INFO messages
    logging.basicConfig(level=logging.INFO, 
                      format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    # Create agent
    logger.info("Initializing Gemma model (this may take a few minutes to download and load)...")
    agent = GemmaAgent()
    logger.info("Model loaded successfully!")
    
    # Test prompt
    prompt = "Explain black holes in simple terms."
    logger.info(f"\nSending prompt: {prompt}")
    
    # Get response
    logger.info("Generating response...")
    response = agent.get_chat_response(prompt)
    logger.info(f"\nResponse: {response}")

if __name__ == "__main__":
    main() 