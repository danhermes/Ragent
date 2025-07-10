import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const ListMicsAndPick = ({ onMicrophoneSelected }) => {
  const [availableMicrophones, setAvailableMicrophones] = useState([]);

  useEffect(() => {
    navigator.mediaDevices.enumerateDevices()
      .then(devices => {
        const mics = devices.filter(device => device.kind === 'audioinput');

        // Create a map to store unique microphone entries by deviceId
        const uniqueMics = new Map();
        mics.forEach(mic => {
          uniqueMics.set(mic.deviceId, mic);
        });

        // Convert the map back to an array
        setAvailableMicrophones(Array.from(uniqueMics.values()));
      })
      .catch(err => console.error("Error getting microphones:", err));
  }, []);


  const handleMicSelect = (deviceId) => {
    if (onMicrophoneSelected) {
      onMicrophoneSelected(deviceId);
    }
  };

  return (
    <div>
      <label htmlFor="microphoneSelect">Select Microphone:</label>
      <select
        id="microphoneSelect"
        onChange={e => handleMicSelect(e.target.value)}
      >
        {availableMicrophones.map(mic => (
          <option key={mic.deviceId} value={mic.deviceId}>
            {mic.label || `Microphone ${mic.deviceId}`}
          </option>
        ))}
      </select>
    </div>
  );
};


function App() {
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [statusText, setStatusText] = useState('');
  const [messages, setMessages] = useState([]);
  const audioContextRef = useRef(null);
  const mediaStreamRef = useRef(null);
  const processorNodeRef = useRef(null);
  const isListeningRef = useRef(false);
  const isProcessingRef = useRef(false);
  const recordedChunksRef = useRef([]);
  const micStreamRef = useRef(null);
  const workletNodeRef = useRef(null);
  const audioChunksRef = useRef([]);
  const messagesContainerRef = useRef(null);
  const [selectedMicrophoneId, setSelectedMicrophoneId] = useState(null);

  // Function to scroll to bottom of messages
  const scrollToBottom = () => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  };

  // Function to format GPT response with line-by-line styling
  const formatGPTResponse = (responseText) => {
    const lines = responseText.split('\n').filter(line => line.trim());
    
    if (lines.length === 0) return responseText;
    
    // Check if it's a Cliff-style response (title, definition, body)
    if (lines.length >= 3) {
      const title = lines[0];
      const definition = lines[1];
      const body = lines.slice(2).join('\n');
      
      return (
        <div className="message-content">
          <div className="response-title">{title}</div>
          <div className="response-definition">{definition}</div>
          <div className="response-body">{body}</div>
        </div>
      );
    }
    
    // Fallback to simple formatting
    return <div className="message-content">{responseText}</div>;
  };

  useEffect(() => {
    const checkBackendHealth = async () => {
      console.log("=== FRONTEND: Testing backend connection on app load ===");
      try {
        const response = await fetch('http://localhost:5000/api/health');
        console.log("Backend health check response:", response.status);
        if (response.ok) {
          const data = await response.json();
          console.log("=== FRONTEND: Backend connection successful ===");
          console.log("Backend status:", data);
        } else {
          console.error("Backend health check failed:", response.status);
        }
      } catch (error) {
        console.error("=== FRONTEND: Backend connection test failed ===");
        console.error("Connection error:", error);
      }
    };
    checkBackendHealth();
  }, []);

  const startRecording = async () => {
    console.log("Attempting to start recording with AudioWorklet...");
    try {
      const constraints = {
        audio: selectedMicrophoneId ? { deviceId: { exact: selectedMicrophoneId } } : true,
      };
      const stream = await navigator.mediaDevices.getUserMedia(constraints);

      // const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      console.log("🎤 Microphone access granted.");
      micStreamRef.current = stream;

      audioContextRef.current = new AudioContext({ sampleRate: 16000 });
      const workletPath = '/recorder-processor.js';
      await audioContextRef.current.audioWorklet.addModule(workletPath);

      console.log("Connecting microphone stream to worklet node...");
      const source = audioContextRef.current.createMediaStreamSource(stream);
      workletNodeRef.current = new AudioWorkletNode(audioContextRef.current, 'record-processor');

      workletNodeRef.current.port.onmessage = (event) => {
        const { type, data, chunkIndex, totalSamples } = event.data;
        if (type === 'chunk') {
          audioChunksRef.current.push(...data);
          console.log(`📦 Received chunk ${chunkIndex} with ${data.length} samples (total: ${totalSamples})`);
        } else if (type === 'speech') {
          console.log("🎤 Speech detected");
        } else if (type === 'silence-and-stop') {
          console.log("🔇 Silence detected");
          stopRecording();
        }
      };

      source.connect(workletNodeRef.current);
      workletNodeRef.current.connect(audioContextRef.current.destination);
      setIsListening(true);
      isListeningRef.current = true;
      setStatusText('Listening...');
      console.log("AudioWorklet recording started.");
    } catch (err) {
      console.error("Error initializing audio context or worklet:", err);
      setStatusText('Error accessing microphone');
    }
  };

  const stopRecording = async (isManualStop = false) => {
    console.log("🛑 Stopping recording...");
    setIsListening(false);
    isListeningRef.current = false;
    
    if (isManualStop) {
      setStatusText('Stopped');
      setIsProcessing(false);
      isProcessingRef.current = false;
      
      // Clean up audio resources without processing
      const audioContext = audioContextRef.current;
      const stream = micStreamRef.current;
      const processorNode = workletNodeRef.current;

      if (processorNode) processorNode.disconnect();
      if (stream) stream.getTracks().forEach(track => track.stop());
      if (audioContext) audioContext.close();
      
      audioChunksRef.current = [];
      return; // Exit early - don't process audio
    }
    
    setStatusText('Processing...');
    setIsProcessing(true);
    isProcessingRef.current = true;

    const audioContext = audioContextRef.current;
    const stream = micStreamRef.current;
    const processorNode = workletNodeRef.current;

    if (processorNode) processorNode.disconnect();
    if (stream) stream.getTracks().forEach(track => track.stop());
    if (audioContext) audioContext.close();

    const audioBuffer = audioChunksRef.current;
    audioChunksRef.current = [];

    const wavBlob = encodeWAV(audioBuffer, 16000);
    console.log("📤 Sending audio file to server...");
    sendAudioFile(wavBlob);
  };

  const encodeWAV = (samples, sampleRate) => {
    console.log("Encoding WAV with sample rate:", sampleRate);
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);
    const writeString = (view, offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + samples.length * 2, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeString(view, 36, 'data');
    view.setUint32(40, samples.length * 2, true);
    for (let i = 0; i < samples.length; i++) {
      view.setInt16(44 + i * 2, samples[i] * 0x7FFF, true);
    }
    return new Blob([view], { type: 'audio/wav' });
  };

  const sendAudioFile = async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');

    try {
      console.log("=== FRONTEND: Connecting to backend /api/transcribe ===");
      console.log("Backend URL: http://localhost:5000/api/transcribe");

      const response = await fetch('http://localhost:5000/api/transcribe', {
        method: 'POST',
        body: formData,
      });

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
      
      // Add transcribed message to the conversation
      if (transcribedText && transcribedText.trim()) {
        setMessages(prev => [...prev, {
          id: Date.now(),
          type: 'transcription',
          text: transcribedText,
          timestamp: new Date().toLocaleTimeString()
        }]);
        // Scroll to bottom after adding transcription
        setTimeout(scrollToBottom, 50);
      }
      
      sendToGPT(transcribedText);
    } catch (error) {
      console.error("=== FRONTEND: Chat request failed ===");
      console.error("Error details:", error);
      console.error("Error message:", error.message);
    }
  };

  const sendToGPT = async (message) => {
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
      
      // Add AI response to the conversation with formatted content
      if (data.response && data.response.trim()) {
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          type: 'ai',
          text: data.response,
          formattedContent: formatGPTResponse(data.response),
          timestamp: new Date().toLocaleTimeString()
        }]);
        
        // Scroll to bottom after adding GPT response
        setTimeout(scrollToBottom, 50);
        
        // Auto-restart listening immediately after GPT response is displayed
        setTimeout(() => {
          if (!isListeningRef.current) {
            startRecording();
          }
        }, 100); // Small delay to ensure the message is rendered
      }
    } catch (error) {
      console.error("=== FRONTEND: Chat request failed ===");
      console.error("Error details:", error);
      console.error("Error message:", error.message);
    } finally {
      setIsProcessing(false);
      isProcessingRef.current = false;
      
      // No auto-restart - user must manually start listening again
    }
  };

  return (
    <div className="cliff-app">
      <ListMicsAndPick onMicrophoneSelected={setSelectedMicrophoneId} />
      <div className="cliff-header">
        <h1>🎤 Cliff - AI Voice Assistant</h1>
        <div className="header-controls">
          <button 
            className="control-btn start" 
            onClick={startRecording} 
            disabled={isListening || isProcessing}
          >
            Start Listening
          </button>
          <button 
            className="control-btn stop" 
            onClick={() => stopRecording(true)} 
            disabled={!isListening}
          >
            Stop Listening
          </button>
        </div>
      </div>
      
      <div className="status-bar">
        <div className={`status-indicator ${isListening ? 'listening' : 'stopped'}`}>
          {isListening ? '🔴' : '⚫'}
        </div>
        <span className="status-text">{statusText}</span>
        {isProcessing && <span className="processing-spinner">⏳</span>}
      </div>
      
      <div className="messages-container" ref={messagesContainerRef}>
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type === 'transcription' ? 'transcription' : 'response'}`}>
            {message.type === 'ai' && message.formattedContent ? (
              message.formattedContent
            ) : (
              <div className="message-content">
                {message.text}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
