# Cliff - AI Speech Assistant

## Overview

Cliff is an AI-powered speech assistant that listens to conversations ambiently and provides real-time technical term explanations. Built with **React** (frontend) and **Flask** (backend), it uses OpenAI Whisper for speech-to-text transcription and ChatGPT for intelligent responses.

## Features

- **Real-time Speech Recognition**: Continuously listens for speech using OpenAI Whisper
- **Technical Term Detection**: Automatically identifies and explains AI, ML, LLM, RAG, and software architecture terms
- **Visual Feedback**: Real-time status updates showing listening, processing, and transcription states
- **Clean Interface**: Modern, responsive UI with clear status indicators
- **Comprehensive Logging**: Detailed logging in both frontend (browser console) and backend (terminal/file)
- **Error Handling**: Graceful error handling with user-friendly feedback

## Architecture

### Components

1. **React Frontend** (`cliff/src/App.js`): Modern React component handling audio processing and UI
2. **Flask Backend** (`cliff/flask_backend.py`): Flask API server handling transcription and AI responses
3. **AudioHandler** (`helpers/audio_handler.py`): Audio processing pipeline for real-time speech capture
4. **BaseAgent** (`agents/base_agent.py`): Base class providing common agent functionality

### Audio Processing Pipeline

```
Microphone Input → Audio Chunks → Speech Detection → Audio Buffer → 
Transcription (Whisper) → LLM Processing (ChatGPT) → Response Display
```

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key
- Microphone access

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Ragent
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r install/requirements.txt
   ```

3. **Install React dependencies**:
   ```bash
   cd cliff
   npm install
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Development Mode

1. **Start the Flask backend** (in one terminal):
   ```bash
   cd cliff
   python flask_backend.py
   ```
   The backend will be available at `http://localhost:5000`

2. **Start the React frontend** (in another terminal):
   ```bash
   cd cliff
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

3. **Access the application**:
   Open your browser and go to `http://localhost:3000`

### Using Cliff

1. **Initialization**: The app will show "🎧 Listening for speech..." when ready
2. **Speak**: Talk naturally - Cliff will detect speech and show "📊 Recording speech..."
3. **Processing**: When you stop speaking, Cliff will show "⚙️ Processing speech..."
4. **Transcription**: You'll see "🎤 Heard: '[your words]'" when speech is transcribed
5. **Response**: Cliff will provide technical term explanations in the chat interface

### Visual Feedback

- **🎧 Green status**: Listening for speech
- **📊 Blue status**: Recording speech chunks
- **⚙️ Orange status**: Processing speech
- **🎤 Blue box**: Shows transcribed text
- **❌ Red box**: Error messages
- **🤖 Header**: Shows "Cliff" agent name

## Configuration

### Audio Settings

Default audio settings in the React app:
- Sample rate: 16kHz
- Channels: 1 (mono)
- Speech threshold: 0.01 (sensitivity)
- Max silence frames: 30 (1.5 seconds)

### LLM Configuration

Cliff uses:
- **Model**: GPT-4o
- **Assistant ID**: `asst_FqW27FDBYLurUdqWVtV7wblJ`
- **Response Format**: Technical term explanations

## Testing

### Run All Tests
```bash
cd cliff
python tests/test_all.py
```

### Run Specific Tests
```bash
cd cliff
python tests/test_backend.py      # Backend API tests
python tests/test_integration.py  # Integration tests
python tests/test_frontend.py     # Frontend tests
```

### Test Documentation
See `cliff/tests/TESTING.md` for detailed testing information.

## Logging

### Frontend Logging
- **Location**: Browser console (F12 → Console tab)
- **Logs include**:
  - App initialization
  - Backend connection status
  - Audio processing events
  - API request/response details
  - Error messages

### Backend Logging
- **Location**: Terminal and `cliff/cliff_backend.log`
- **Logs include**:
  - Server startup
  - API request details
  - Transcription processing
  - Error handling

## Troubleshooting

### Common Issues

1. **"No API key found"**
   - Ensure your `.env` file contains `OPENAI_API_KEY=your_key`
   - Restart the backend after adding the key

2. **"Audio too short"**
   - Speak for at least 0.1 seconds
   - Check microphone permissions

3. **"Error in OpenAI Whisper transcription"**
   - Verify internet connection
   - Check OpenAI API key validity
   - Ensure microphone is working

4. **No audio detection**
   - Check microphone permissions in your OS
   - Verify microphone is not muted
   - Try increasing speech threshold in the React app

5. **Frontend not connecting to backend**
   - Ensure Flask backend is running on port 5000
   - Check browser console for connection errors
   - Verify CORS settings in Flask

### Debug Mode

Run with debug logging:
```bash
# Backend
cd cliff
python flask_backend.py

# Frontend
cd cliff
npm start
# Then check browser console (F12)
```

## Development

### Project Structure

```
cliff/
├── src/                    # React frontend
│   ├── App.js             # Main React component
│   ├── App.css            # Styles
│   └── index.js           # React entry point
├── public/                # React public files
├── tests/                 # Test files
│   ├── test_backend.py    # Backend tests
│   ├── test_integration.py # Integration tests
│   ├── test_frontend.py   # Frontend tests
│   ├── test_all.py        # All tests
│   └── TESTING.md         # Test documentation
├── old_frontend/          # Archived old files
├── flask_backend.py       # Flask API server
├── package.json           # React dependencies
├── cliff_backend.log      # Backend logs
└── README.md              # Documentation
```

### Adding New Features

1. **New Frontend Features**: Edit `cliff/src/App.js` and `cliff/src/App.css`
2. **New Backend Features**: Edit `cliff/flask_backend.py`
3. **New Tests**: Add to `cliff/tests/` directory
4. **New Audio Processing**: Extend `helpers/audio_handler.py`

### Testing

Run the application and test:
- Speech detection sensitivity
- Transcription accuracy
- Response quality
- Error handling
- Integration between frontend and backend

## API Reference

### Flask Backend Endpoints

```python
# Health check
GET /api/health
Response: {"status": "healthy", "agent": "Cliff"}

# Audio transcription
POST /api/transcribe
Body: FormData with 'audio' file
Response: {"text": "transcribed_text"}

# AI chat response
POST /api/chat
Body: {"message": "user_text"}
Response: {"response": "ai_response"}
```

### React Frontend

```javascript
// Main component
const App = () => {
  // State management
  const [isListening, setIsListening] = useState(false);
  const [messages, setMessages] = useState([]);
  
  // Audio processing
  const startListening = async () => { /* ... */ };
  const stopListening = () => { /* ... */ };
  
  // API communication
  const transcribeAudio = async (audioBlob) => { /* ... */ };
  const getChatResponse = async (message) => { /* ... */ };
};
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly using the test suite
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Check the troubleshooting section
- Review the logs in debug mode
- Check the test documentation
- Create an issue in the repository 