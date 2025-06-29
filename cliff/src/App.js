import React, { useState, useRef, useEffect } from 'react';
import './App.css';

const App = () => {
  console.log("=== CLIFFAPP LOADED ===");
  
  // --- Version Information ---
  const VERSION = "1.0.0"; // Added version number here

  // --- State and Refs ---
  const [isListening, setIsListening] = useState(false);
  const isListeningRef = useRef(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [statusText, setStatusText] = useState('Click "Start Listening" to begin');
  const [messages, setMessages] = useState([]);

  // Refs for the audio processing logic
  const audioContextRef = useRef(null);
  const mediaStreamRef = useRef(null);
  const processorRef = useRef(null);
  const audioBufferRef = useRef([]); // Stores audio chunks during speech
  const silenceTimeoutRef = useRef(null); // Ref to manage silence detection timeout
  const lastProcessTimeRef = useRef(0); // Track last processing time to prevent overlap
  const isRecordingRef = useRef(false); // Track if we're currently recording

  // Ref for scrolling messages
  const messagesEndRef = useRef(null);

  // Ref for preventing multiple processing calls
  const isProcessingRef = useRef(false);

  // --- Effects ---

  // Effect to scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Effect for cleanup on component unmount
  useEffect(() => {
    return () => {
      stopListening();
    };
  }, []);

  // Effect to test backend connection on app load
  useEffect(() => {
    const testBackendConnection = async () => {
      console.log("=== FRONTEND: Testing backend connection on app load ===");
      try {
        const response = await fetch('http://localhost:5000/api/health');
        console.log("Backend health check response:", response.status);
        if (response.ok) {
          const data = await response.json();
          console.log("=== FRONTEND: Backend connection successful ===");
          console.log("Backend status:", data);
          // addMessage('✅ Backend connected successfully', 'status'); // Commented out - status only in status bar
        } else {
          console.error("Backend health check failed:", response.status);
          // addMessage('❌ Backend connection failed', 'error'); // Commented out - status only in status bar
        }
      } catch (error) {
        console.error("=== FRONTEND: Backend connection test failed ===");
        console.error("Connection error:", error);
        // addMessage('❌ Cannot connect to backend - check if Flask is running', 'error'); // Commented out - status only in status bar
      }
    };

    testBackendConnection();
  }, []);

  // --- Helper Functions ---

  // Function to add a new message to the display
  const addMessage = (text, type = 'user') => {
    // Only add transcriptions and responses to the messages container
    if (type === 'transcription' || type === 'response') {
      // Format response messages for better readability
      let formattedContent = text;
      if (type === 'response') {
        formattedContent = formatResponse(text);
      }
      
      const newMessage = {
        content: formattedContent,
        type,
        time: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, newMessage]);
    }
    // Status messages are handled by the status bar only
  };

  // Format response content for better readability
  const formatResponse = (text) => {
    // First apply the punctuation spacing fix
    let formatted = formatGPTResponse(text);
    
    // Split into lines and format each line
    const lines = formatted.split('\n').filter(line => line.trim());
    
    if (lines.length === 0) return text;
    
    // Format the first line as a title (bold, all caps)
    let result = `<div class="response-title">${lines[0]}</div>`;
    
    // Format the second line as a definition (bold, regular capitalization)
    if (lines.length > 1) {
      result += `<div class="response-definition">${lines[1]}</div>`;
    }
    
    // Add the rest of the lines as normal text with proper spacing
    if (lines.length > 2) {
      const remainingText = lines.slice(2).join('\n');
      result += `<div class="response-body">${remainingText}</div>`;
    }
    
    console.log("=== FORMATTING DEBUG ===");
    console.log("Original text:", text);
    console.log("Formatted HTML:", result);
    console.log("Lines:", lines);
    
    return result;
  };

  // Converts raw audio float data to a WAV file Blob
  const audioToWav = (audioData, sampleRate) => {
    const buffer = new ArrayBuffer(44 + audioData.length * 2);
    const view = new DataView(buffer);

    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    // RIFF header
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + audioData.length * 2, true);
    writeString(8, 'WAVE');
    // fmt sub-chunk
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true); // Sub-chunk size
    view.setUint16(20, 1, true); // Audio format (1 for PCM)
    view.setUint16(22, 1, true); // Number of channels
    view.setUint32(24, sampleRate, true); // Sample rate
    view.setUint32(28, sampleRate * 2, true); // Byte rate
    view.setUint16(32, 2, true); // Block align
    view.setUint16(34, 16, true); // Bits per sample
    // data sub-chunk
    writeString(36, 'data');
    view.setUint32(40, audioData.length * 2, true);

    // Write the PCM audio data
    let offset = 44;
    for (let i = 0; i < audioData.length; i++) {
      const sample = Math.max(-1, Math.min(1, audioData[i]));
      view.setInt16(offset, sample * 0x7FFF, true);
      offset += 2;
    }

    return new Blob([buffer], { type: 'audio/wav' });
  };

  // Helper to update both state and ref
  const setListening = (val) => {
    setIsListening(val);
    isListeningRef.current = val;
  };

  // --- Audio Processing Logic ---

  const startListening = async () => {
    console.log("[AUDIO] startListening called");
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.error("[AUDIO] Audio recording is not supported by your browser.");
      addMessage('Error: Audio recording is not supported by your browser.', 'error');
      return;
    }

    // Reset processing state for new session
    isProcessingRef.current = false;
    audioBufferRef.current = [];
    isRecordingRef.current = false; // Reset recording state
    if (silenceTimeoutRef.current) {
        clearTimeout(silenceTimeoutRef.current);
        silenceTimeoutRef.current = null;
    }

    try {
      console.log("[AUDIO] Requesting microphone access...");
      // Get microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
          audio: { sampleRate: 16000, channelCount: 1, echoCancellation: true, noiseSuppression: true }
      });
      console.log("[AUDIO] Microphone access granted.");
      mediaStreamRef.current = stream;

      console.log("[AUDIO] Creating AudioContext...");
      const context = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
      audioContextRef.current = context;

      console.log("[AUDIO] Creating MediaStreamSource...");
      const source = context.createMediaStreamSource(stream);

      console.log("[AUDIO] Creating ScriptProcessorNode...");
      const processor = context.createScriptProcessor(16384, 1, 1); // Maximum allowed: 16384 (1 second at 16kHz)
      processorRef.current = processor;

      console.log("[AUDIO] Setting onaudioprocess handler...");
      processor.onaudioprocess = (event) => {
        console.log("[AUDIO] isListening value:", isListeningRef.current);
        if (!isListeningRef.current || isProcessingRef.current) return;
        const inputData = event.inputBuffer.getChannelData(0);

        // Simple voice activity detection (VAD)
        const rms = Math.sqrt(inputData.reduce((sum, val) => sum + val * val, 0) / inputData.length);
        console.log(`[AUDIO] Audio chunk processed. RMS: ${rms}`);
        if (rms > 0.01) { // Threshold for speech detection
          // If speech is detected, clear any existing silence timeout
          if (silenceTimeoutRef.current) {
            clearTimeout(silenceTimeoutRef.current);
            silenceTimeoutRef.current = null;
            console.log("[AUDIO] Speech detected, cleared silence timeout.");
          }
          setStatusText('Speaking...');
          audioBufferRef.current.push(new Float32Array(inputData));
          console.log("[AUDIO] Speech detected, audio chunk added to buffer.");
        } else if (audioBufferRef.current.length > 0 && !silenceTimeoutRef.current) {
            // If there's recorded audio and now there's silence, start a timeout.
            silenceTimeoutRef.current = setTimeout(() => {
                console.log("[AUDIO] Silence detected, processing captured audio.");
                processCapturedAudio();
                silenceTimeoutRef.current = null;
            }, 2000); // 2 seconds of silence triggers processing
            console.log("[AUDIO] Silence detected, started silence timeout.");
        }
      };

      console.log("[AUDIO] Connecting source to processor...");
      source.connect(processor);

      console.log("[AUDIO] Connecting processor to context.destination...");
      processor.connect(context.destination);

      console.log("[AUDIO] Audio pipeline fully connected.");

      setListening(true);
      setStatusText('Listening...'); // Microphone access granted. 
      // addMessage('Listening for speech...', 'status'); // Commented out - status only in status bar
      console.log("[AUDIO] Listening started.");

    } catch (err) {
      console.error(`[AUDIO] Error accessing microphone: ${err.message}`);
      // addMessage(`Error accessing microphone: ${err.message}. Please grant permission.`, 'error'); // Commented out - status only in status bar
    }
  };

  const processCapturedAudio = () => {
      console.log("[AUDIO] processCapturedAudio called. Buffer length:", audioBufferRef.current.length, "Processing:", isProcessingRef.current);
      
      if (isProcessingRef.current) {
          console.log("[AUDIO] Already processing, ignoring duplicate call.");
          return;
      }
      
      if (audioBufferRef.current.length === 0) {
          console.log("[AUDIO] No audio buffer to process.");
          return;
      }
      
      // Calculate total audio length to ensure minimum duration
      const totalSamples = audioBufferRef.current.reduce((acc, buffer) => acc + buffer.length, 0);
      const audioDuration = totalSamples / 16000; // 16kHz sample rate
      console.log(`[AUDIO] Total audio duration: ${audioDuration.toFixed(2)} seconds`);
      
      // Require minimum 0.5 seconds of audio to prevent tiny fragments
      if (audioDuration < 0.5) {
          console.log("[AUDIO] Audio too short, discarding.");
          audioBufferRef.current = [];
          isProcessingRef.current = false;
          setListening(true);
          setStatusText('Listening...');
          return;
      }
      
      // Immediately set processing flag to prevent multiple calls
      isProcessingRef.current = true;
      setListening(false); // Automatically stop listening when processing audio
      // addMessage('Processing audio...', 'status'); // Commented out - status only in status bar
      setIsProcessing(true);
      setStatusText('Processing audio...');
      console.log("[AUDIO] Processing captured audio buffer.");

      // Clear any pending silence timeout
      if (silenceTimeoutRef.current) {
          clearTimeout(silenceTimeoutRef.current);
          silenceTimeoutRef.current = null;
      }

      // Combine all audio chunks into one array
      const combined = new Float32Array(audioBufferRef.current.reduce((acc, val) => acc + val.length, 0));
      let offset = 0;
      for(const buffer of audioBufferRef.current) {
          combined.set(buffer, offset);
          offset += buffer.length;
      }
      
      // Clear buffer immediately to prevent reprocessing
      audioBufferRef.current = [];

      // Convert to WAV and transcribe
      const wavBlob = audioToWav(combined, audioContextRef.current.sampleRate);
      console.log("[AUDIO] Audio buffer converted to WAV, sending to transcribeAudio.");
      transcribeAudio(wavBlob);
  }

  const stopListening = () => {
    console.log("[AUDIO] stopListening called");
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => track.stop());
      console.log("[AUDIO] Media stream tracks stopped.");
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      console.log("[AUDIO] AudioContext closed.");
    }
    if (processorRef.current) {
        processorRef.current.disconnect();
        console.log("[AUDIO] ScriptProcessorNode disconnected.");
    }
    if(silenceTimeoutRef.current) {
        clearTimeout(silenceTimeoutRef.current);
        silenceTimeoutRef.current = null;
        console.log("[AUDIO] Cleared silence timeout.");
    }

    // Process any remaining audio
    if (audioBufferRef.current.length > 0 && !isProcessingRef.current) {
        processCapturedAudio();
    }

    setListening(false);
    if (!isProcessing) {
        setStatusText('Click "Start Listening" to begin');
    }
    console.log("[AUDIO] Listening stopped.");
  };

  // --- API Communication ---

  const transcribeAudio = async (audioBlob) => {
    console.log("=== FRONTEND: Starting audio transcription ===");
    console.log("Audio blob size:", audioBlob.size, "bytes");
    
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');

    try {
      console.log("=== FRONTEND: Connecting to backend /api/transcribe ===");
      console.log("Backend URL: http://localhost:5000/api/transcribe");
      
      const response = await fetch('http://localhost:5000/api/transcribe', { method: 'POST', body: formData });
      
      console.log("=== FRONTEND: Backend response received ===");
      console.log("Response status:", response.status);
      console.log("Response headers:", Object.fromEntries(response.headers.entries()));
      
      if (!response.ok) {
        console.error("Backend error:", response.status, response.statusText);
        throw new Error(`Server error: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log("Backend response data:", data);
      
      if (data.error) {
        console.error("Backend returned error:", data.error);
        throw new Error(data.error);
      }

      const transcribedText = data.text;
      if (transcribedText) {
        console.log("=== FRONTEND: Transcription successful ===");
        console.log("Transcribed text:", transcribedText);
        addMessage(transcribedText, 'transcription');
        getChatResponse(transcribedText);
      } else {
        console.log("=== FRONTEND: No speech detected ===");
        // addMessage('No speech detected in the audio.', 'status'); // Commented out - status only in status bar
        setIsProcessing(false);
        isProcessingRef.current = false;
        setStatusText('Listening...');
      }

    } catch (error) {
      console.error("=== FRONTEND: Transcription failed ===");
      console.error("Error details:", error);
      console.error("Error message:", error.message);
      addMessage(`Transcription failed: ${error.message}`, 'error');
      setIsProcessing(false);
      isProcessingRef.current = false;
      setStatusText('Error during transcription. Please try again.');
    }
  };

  const getChatResponse = async (message) => {
    console.log("=== FRONTEND: Getting AI chat response ===");
    console.log("Message to send:", message);
    
    try {
        console.log("=== FRONTEND: Connecting to backend /api/chat ===");
        console.log("Backend URL: http://localhost:5000/api/chat");
        
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });
        
        console.log("=== FRONTEND: Chat response received ===");
        console.log("Response status:", response.status);
        
        if (!response.ok) {
          console.error("Backend chat error:", response.status, response.statusText);
          throw new Error(`Server error: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log("Backend chat response data:", data);
        
        if (data.error) {
          console.error("Backend chat returned error:", data.error);
          throw new Error(data.error);
        }
        
        console.log("=== FRONTEND: AI response successful ===");
        console.log("AI response:", data.response);
        addMessage(data.response, 'response');
        // Automatically restart listening if not already listening
        if (!isListeningRef.current) {
          startListening();
        }
    } catch (error) {
        console.error("=== FRONTEND: Chat request failed ===");
        console.error("Error details:", error);
        console.error("Error message:", error.message);
        addMessage(`Failed to get AI response: ${error.message}`, 'error');
    } finally {
        setIsProcessing(false);
        isProcessingRef.current = false;
        // After AI response, go back to listening state if the mic is still active
        if(isListening) {
             setStatusText('Listening...');
        }
    }
  };

  const formatGPTResponse = (text) => {
    // Add spaces after periods, commas, and other punctuation that might be missing
    let formatted = text
      .replace(/\.([A-Z])/g, '. $1')  // Add space after period before capital letter
      .replace(/\.([a-z])/g, '. $1')  // Add space after period before lowercase letter
      .replace(/,([A-Z])/g, ', $1')   // Add space after comma before capital letter
      .replace(/!([A-Z])/g, '! $1')   // Add space after exclamation before capital letter
      .replace(/\?([A-Z])/g, '? $1')  // Add space after question mark before capital letter
      .replace(/;([A-Z])/g, '; $1');  // Add space after semicolon before capital letter
    
    return formatted;
  };

  // --- Render Method ---

  return (
    <div className="cliff-app">
      <header className="cliff-header">
        <h1>Cliff <span className="version-number">v{VERSION}</span></h1> {/* Display version */}
        <div className="header-controls">
          <button onClick={startListening} className="control-btn start" disabled={isListening || isProcessing}>
            Start Listening
          </button>
          <button onClick={stopListening} className="control-btn stop" disabled={!isListening}>
            Stop Listening
          </button>
        </div>
      </header>

      <div className="status-bar">
        <span className={`status-indicator ${isListening ? 'listening' : 'stopped'}`}>●</span>
        <span className="status-text">{statusText}</span>
        {isProcessing && <span className="processing-spinner">⚙️</span>}
      </div>

      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div 
              className="message-content"
              dangerouslySetInnerHTML={{ __html: msg.content }}
            />
            <p className="message-time">{msg.time}</p>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default App;