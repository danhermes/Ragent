from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from agents.agent_cliff import AgentCliff
import tempfile
import wave
import numpy as np
from pathlib import Path
import datetime
import traceback

# Always load .env from the project root
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Configure logging with timestamps and detailed output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('cliff_backend.log')  # File output
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize Cliff agent
cliff_agent = None

def get_cliff_agent():
    """Get or create Cliff agent instance"""
    global cliff_agent
    if cliff_agent is None:
        cliff_agent = AgentCliff()
    return cliff_agent

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe uploaded audio file"""
    logger.info("=== FRONTEND CONNECTION RECEIVED: /api/transcribe ===")
    logger.info(f"Request from: {request.remote_addr}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    try:
        if 'audio' not in request.files:
            logger.error("No audio file in request")
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            logger.error("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Log file size before reading
        audio_file.seek(0, 2)  # Seek to end
        file_size = audio_file.tell()
        logger.info(f"Audio file received: {audio_file.filename}, size: {file_size} bytes")
        audio_file.seek(0)  # Reset file pointer
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            logger.info(f"Saving audio to temp file: {temp_file.name}")
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
        logger.info(f"Audio saved to temp file: {temp_path}")
        logger.info(f"Temp file exists after save: {os.path.exists(temp_path)}")
        logger.info(f"Temp file size: {os.path.getsize(temp_path)} bytes")
        
        try:
            # Get Cliff agent and transcribe
            logger.info("Starting transcription...")
            agent = get_cliff_agent()
            logger.info("OpenAI Whisper STT initialized successfully")
            logger.info(f"Transcribing file: {temp_path}")
            text = agent.transcribe_audio(temp_path)
            logger.info(f"Transcription result: {text}")
            
            if text and text.strip():
                logger.info(f"Transcription successful: '{text}'")
                return jsonify({'text': text.strip()})
            else:
                logger.info("No speech detected in audio")
                return jsonify({'text': ''})
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
                logger.info("Temp file cleaned up")
            except Exception as cleanup_err:
                logger.error(f"Temp file cleanup error: {cleanup_err}")
                logger.error(traceback.format_exc())
                pass
                
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Get AI response to transcribed text"""
    logger.info("=== FRONTEND CONNECTION RECEIVED: /api/chat ===")
    logger.info(f"Request from: {request.remote_addr}")
    
    try:
        data = request.get_json()
        logger.info(f"Received chat data: {data}")
        
        if not data or 'message' not in data:
            logger.error("No message in request data")
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message']
        if not message.strip():
            logger.error("Empty message")
            return jsonify({'error': 'Empty message'}), 400
        
        logger.info(f"Processing message: '{message}'")
        
        # Get Cliff agent and get response
        agent = get_cliff_agent()
        response = agent.get_chat_response(message)
        
        if response:
            logger.info(f"AI Response generated: {response[:100]}...")
            return jsonify({'response': response})
        else:
            logger.error("No response from AI")
            return jsonify({'error': 'No response from AI'}), 500
            
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': f'Chat failed: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info("=== HEALTH CHECK REQUEST ===")
    logger.info(f"Request from: {request.remote_addr}")
    return jsonify({'status': 'healthy', 'agent': 'Cliff'})

@app.route('/')
def index():
    """Serve the React app"""
    logger.info("=== ROOT PAGE REQUEST ===")
    logger.info(f"Request from: {request.remote_addr}")
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cliff - AI Speech Assistant</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            }
            #root {
                height: 100vh;
            }
        </style>
    </head>
    <body>
        <div id="root"></div>
        <script src="http://localhost:3000/static/js/bundle.js"></script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        exit(1)
    
    logger.info("=== CLIFF BACKEND STARTING ===")
    logger.info(f"Starting at: {datetime.datetime.now()}")
    logger.info("Backend will be available at: http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000) 