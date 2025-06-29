from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'agent': 'Cliff'})

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """Mock transcription endpoint"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        # For now, just return a mock transcription
        return jsonify({'text': 'Hello, this is a test transcription'})
                
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Mock chat endpoint"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message']
        
        # Return a mock response
        return jsonify({'response': f'You said: "{message}". This is a test response from Cliff.'})
            
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': f'Chat failed: {str(e)}'}), 500

if __name__ == '__main__':
    logger.info("Starting Cliff Flask backend (test version)...")
    app.run(debug=True, host='0.0.0.0', port=5000) 