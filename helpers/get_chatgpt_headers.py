from call_ChatGPT import CallChatGPT
import logging
from datetime import datetime


# Configure logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/chatgpt_headers_{timestamp}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("Starting GetChatGPTHeaders")

class GetChatGPTHeaders:

    def __init__(self):
        self.call_chatgpt = CallChatGPT()
        self.response = self.call_chatgpt.get_openai_headers()
        logger.info("\n OpenAI Rate Limit Headers:")
        print("\n OpenAI Rate Limit Headers:")
        if self.response == None:
            logger.error("Empty response from OpenAI")
        for k, v in self.response.headers.items():
            if "ratelimit" in k.lower() or "retry" in k.lower():
                logger.info(f"{k}: {v}")
                print(f"{k}: {v}")


if __name__ == "__main__":
    GetChatGPTHeaders()