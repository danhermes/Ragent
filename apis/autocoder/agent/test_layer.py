import os
import json
import logging

logger = logging.getLogger(__name__)

class TestLayer:
    """
    Provides test-mode replacements for APIs, I/O, and external services.
    Acts as a backend harness for testing code without making real calls.
    """
    def __init__(self, baseline_path: str = "../baseline_test_data.json"):
        self.mock_data = {}
        self.enabled = False
        if baseline_path and os.path.exists(baseline_path):
            try:
                with open(baseline_path, 'r', encoding='utf-8') as f:
                    self.mock_data = json.load(f)
                self.enabled = True
                logger.info(f"TestLayer: Loaded baseline test data from {baseline_path}")
            except Exception as e:
                logger.error(f"TestLayer: Failed to load baseline: {str(e)}")

    def get(self, key: str):
        if self.enabled:
            return self.mock_data.get(key)
        return None

    def put(self, key: str, value):
        if self.enabled:
            self.mock_data[key] = value

    def chatgpt(self, prompt: str):
        if self.enabled:
            return self.mock_data.get("chatgpt_response", "[TestLayer] GPT reply.")
        raise RuntimeError("TestLayer not enabled")

    def file_read(self, file_key: str):
        if self.enabled:
            return self.mock_data.get("files", {}).get(file_key, "")
        raise RuntimeError("TestLayer not enabled")

    def file_write(self, file_key: str, content: str):
        if self.enabled:
            self.mock_data.setdefault("files", {})[file_key] = content

    def db_read(self, query: str):
        if self.enabled:
            return self.mock_data.get("db_results", {}).get(query, None)
        raise RuntimeError("TestLayer not enabled")

    def db_write(self, query: str, result):
        if self.enabled:
            self.mock_data.setdefault("db_results", {})[query] = result
