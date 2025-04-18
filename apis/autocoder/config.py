import os
from dotenv import load_dotenv
load_dotenv()

DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
