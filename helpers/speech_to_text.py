from abc import ABC, abstractmethod
import torch
import os
import time
from typing import Optional, Tuple
import numpy as np
import re
import openai
import logging

logger = logging.getLogger("streamlit")

class SpeechToText(ABC):
    """Base class for speech-to-text implementations"""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the STT model"""
        pass
        
    @abstractmethod
    def transcribe(self, audio_file: str) -> Tuple[str, float]:
        """
        Transcribe audio file to text
        Returns: (transcribed_text, processing_time)
        """
        pass
        
    def cleanup(self) -> None:
        """Cleanup resources if needed"""
        pass

class LocalWhisperSTT(SpeechToText):
    """Local Whisper implementation using faster-whisper"""
    
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None
        
    def initialize(self) -> None:
        try:
            print("Loading Whisper model...")
            from faster_whisper import WhisperModel
            
            # Use CUDA if available, else CPU
            device = "cuda" if torch.cuda.is_available() else "cpu"
            compute_type = "float16" if device == "cuda" else "int8"
            print(f"Using device: {device}, compute_type: {compute_type}")
            
            self.model = WhisperModel(
                self.model_size,
                device=device,
                compute_type=compute_type
            )
            print("Whisper model loaded successfully")
            
        except ImportError as e:
            print(f"Error importing faster-whisper: {str(e)}")
            raise
        except Exception as e:
            print(f"Error loading Whisper model: {str(e)}")
            raise
            
    def transcribe(self, audio_file: str) -> Tuple[str, float]:
        if not self.model:
            raise RuntimeError("Model not initialized. Call initialize() first.")
            
        start_time = time.time()
        try:
            segments, info = self.model.transcribe(
                audio_file,
                beam_size=5,
                language="en",
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=100,
                    speech_pad_ms=200,
                    threshold=0.1
                ),
                condition_on_previous_text=True,
                compression_ratio_threshold=2.4,
                temperature=0.0,
                word_timestamps=True,
                no_speech_threshold=0.6,
                best_of=5,
                fp16=False,
                initial_prompt="The following is a clear, well-enunciated speech:"
            )
            
            text = " ".join([s.text for s in segments]).strip()
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
            text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
            
            process_time = time.time() - start_time
            return text, process_time
            
        except Exception as e:
            print(f"Error in Whisper transcription: {str(e)}")
            return "", time.time() - start_time

class OpenAIWhisperSTT(SpeechToText):
    """Speech-to-text using OpenAI's Whisper API"""
    
    def __init__(self):
        self.model = "whisper-1"
        self.initialized = False
        
    def initialize(self):
        """Initialize the STT service"""
        if not self.initialized:
            try:
                # Verify API key is set
                if not os.getenv("OPENAI_API_KEY"):
                    raise ValueError("OPENAI_API_KEY environment variable not set")
                    
                self.initialized = True
                logger.info("OpenAI Whisper STT initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing OpenAI Whisper STT: {str(e)}")
                raise
                
    def transcribe(self, audio_file: str) -> Tuple[str, float]:
        """Transcribe audio file using OpenAI's Whisper API"""
        if not self.initialized:
            self.initialize()
            
        start_time = time.time()
        try:
            with open(audio_file, "rb") as file:
                response = openai.audio.transcriptions.create(
                    model=self.model,
                    file=file,
                    language="en",
                    response_format="text"
                )
                process_time = time.time() - start_time
                return response, process_time
                
        except Exception as e:
            logger.error(f"Error in OpenAI Whisper transcription: {str(e)}")
            return "", time.time() - start_time

class VoskSTT(SpeechToText):
    """Vosk offline speech recognition implementation"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or "vosk-model-small-en-us"
        self.model = None
        self.recognizer = None
        
    def initialize(self) -> None:
        try:
            from vosk import Model, KaldiRecognizer
            import wave
            
            if not os.path.exists(self.model_path):
                raise ValueError(f"Vosk model not found at {self.model_path}")
                
            self.model = Model(self.model_path)
            print("Vosk model loaded successfully")
            
        except ImportError:
            raise ImportError("vosk package not installed. Run: pip install vosk")
            
    def transcribe(self, audio_file: str) -> Tuple[str, float]:
        from vosk import KaldiRecognizer
        import wave
        import json
        
        start_time = time.time()
        try:
            wf = wave.open(audio_file, "rb")
            # Create new recognizer for each file to avoid state issues
            recognizer = KaldiRecognizer(self.model, wf.getframerate())
            
            text = ""
            while True:
                data = wf.readframes(4000)  # Read in chunks
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text += " " + result.get("text", "")
                    
            # Get final bits of audio
            final_result = json.loads(recognizer.FinalResult())
            text += " " + final_result.get("text", "")
            text = text.strip()
            
            process_time = time.time() - start_time
            return text, process_time
            
        except Exception as e:
            print(f"Error in Vosk transcription: {str(e)}")
            return "", time.time() - start_time 