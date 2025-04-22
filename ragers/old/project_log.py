from datetime import datetime

class ProjectLog:
    def log_interaction(self, prompt: str, response: str) -> None:
        """Log ChatGPT interaction"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"\n[{timestamp}]\nPrompt: {prompt}\nResponse: {response}\n"
            
            with open(self.interactions_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
            self.logger.info(f"Logged ChatGPT interaction at {timestamp}")
        except Exception as e:
            self.logger.error(f"Failed to log ChatGPT interaction: {str(e)}") 