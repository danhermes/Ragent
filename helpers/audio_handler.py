import sounddevice as sd
import numpy as np
import soundfile as sf
import os
import logging
import wave
from typing import Optional, Tuple
import time
import threading

# Suppress verbose debug logging from external libraries
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

logger = logging.getLogger("streamlit")
logger.setLevel(logging.INFO)  # Changed from DEBUG to INFO

class AudioHandler:
    """Handles audio input/output operations"""
    
    def __init__(self):
        self.sample_rate = 16000
        self.channels = 1
        self.dtype = np.float32
        self.is_speaking = False
        self.silence_frames = 0
        self.max_silence_frames = 30  # 1.5 seconds of silence
        self.speech_threshold = 0.001  # Lowered from 0.005 to be more sensitive
        self.stream = None
        self.audio_buffer = []
        self.processing_lock = False
        self.last_process_time = 0
        self.should_stop = False  # Add flag to control stream
        self.initialize()
        
    def initialize(self):
        """Initialize audio stream"""
        try:
            # Reset stop flag
            self.should_stop = False
            
            # Configure stream but don't start it yet
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                callback=self._audio_callback
            )
            logger.info("Audio stream initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing audio stream: {str(e)}")
            raise
            
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        if status:
            logger.warning(f"Audio callback status: {status}")
        if self.should_stop:
            raise sd.CallbackStop()
            
    def record_audio(self, filename, duration=5):
        """Record audio for a specified duration"""
        fs = 44100  # Sample rate
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        sf.write(filename, myrecording, fs)
        
    def record_audio_chunk(self, duration: float = 0.05) -> Tuple[np.ndarray, int]:
        """Record a short audio chunk"""
        try:
            if self.should_stop:
                return None, self.sample_rate
                
            frames = int(duration * self.sample_rate)
            audio_data = sd.rec(frames, samplerate=self.sample_rate, channels=self.channels, dtype=self.dtype)
            sd.wait()
            return audio_data, self.sample_rate
        except Exception as e:
            logger.error(f"Error recording audio chunk: {str(e)}")
            return None, self.sample_rate
            
    def is_speech(self, audio_data: np.ndarray) -> bool:
        """Detect if audio chunk contains speech"""
        try:
            # Normalize audio data before calculating RMS to prevent overflow
            if np.max(np.abs(audio_data)) > 1.0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Calculate RMS using a more numerically stable method
            rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float64))))
            
            # Debug: log audio levels occasionally
            if len(self.audio_buffer) % 100 == 0:  # Log every 100 chunks
                logger.info(f"Audio RMS: {rms:.6f}, Threshold: {self.speech_threshold:.6f}")
            
            if rms > self.speech_threshold:
                self.is_speaking = True
                self.silence_frames = 0
                return True
            else:
                if self.is_speaking:
                    self.silence_frames += 1
                return False
        except Exception as e:
            logger.error(f"Error detecting speech: {str(e)}")
            return False
            
    def save_audio_chunk(self, audio_data: np.ndarray, sample_rate: int, filename: str) -> bool:
        """Save audio chunk to WAV file"""
        try:
            # Ensure audio data is in the correct format
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
                
            # Normalize audio if needed
            max_val = np.max(np.abs(audio_data))
            if max_val > 1.0:
                audio_data = audio_data / max_val
                
            # Save to WAV file
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(sample_rate)
                wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
                
            # Verify file was created and has content
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                logger.error("Failed to save audio file or file is empty")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Error saving audio chunk: {str(e)}")
            return False
            
    def process_audio(self, audio_data: np.ndarray, sample_rate: int, agent, on_transcription=None) -> Optional[str]:
        """Process audio data through STT and LLM"""
        duration = len(audio_data)/sample_rate
        logger.info(f"Processing {duration:.1f}s of audio...")
        
        # Initialize temp_file at the start
        temp_file = "temp_chunk.wav"
        
        # Safety check for invalid audio data
        try:
            max_amp = np.max(np.abs(audio_data))
            mean_amp = np.mean(np.abs(audio_data))
            if max_amp > 1.0 or np.isnan(max_amp) or np.isinf(max_amp):
                logger.error("Invalid audio data detected")
                return None
                
            # Check if audio is long enough
            if duration < 0.1:  # Minimum 0.1 seconds
                logger.error(f"Audio too short ({duration:.2f}s < 0.1s)")
                return None
                
            # Save chunk to temporary file
            try:
                if not self.save_audio_chunk(audio_data, sample_rate, temp_file):
                    logger.error("Failed to save audio chunk")
                    return None
                
                # Verify file exists and has content
                if not os.path.exists(temp_file):
                    logger.error("Temporary file not created")
                    return None
                    
                file_size = os.path.getsize(temp_file)
                if file_size == 0:
                    logger.error("Saved audio file is empty")
                    return None
                
                # Transcribe audio
                logger.info("Transcribing speech...")
                text = agent.transcribe_audio(temp_file)
                
                if text:  # Only process if there's actual text
                    logger.info(f"Transcribed: '{text}'")
                    
                    # Call transcription callback
                    if on_transcription:
                        on_transcription(text)
                    
                    # Get LLM response
                    logger.info("Getting AI response...")
                    
                    try:
                        response = agent.get_chat_response(text)
                        
                        if response:
                            logger.info("Response received")
                            return response
                        else:
                            logger.error("No response from AI")
                            return None
                    except Exception as e:
                        logger.error(f"Error in LLM processing: {str(e)}")
                        return None
                else:
                    logger.info("No speech detected")
                    # Report no speech to UI
                    if on_transcription:
                        on_transcription("No speech detected")
                    return None
                    
            except Exception as e:
                logger.error(f"Error in transcription: {str(e)}")
                return None
            
        except Exception as e:
            logger.error(f"Error in audio processing: {str(e)}")
            return None
            
        finally:
            # Clean up temporary file with retry logic
            self._cleanup_temp_file(temp_file)
    
    def _cleanup_temp_file(self, temp_file: str):
        """Clean up temporary file with retry logic for Windows file locks"""
        if not os.path.exists(temp_file):
            return
            
        max_retries = 3
        for attempt in range(max_retries):
            try:
                os.remove(temp_file)
                break
            except PermissionError:
                if attempt < max_retries - 1:
                    time.sleep(0.1)  # Wait a bit before retrying
                    continue
                else:
                    logger.warning(f"Could not remove {temp_file} after {max_retries} attempts")
            except Exception as e:
                logger.warning(f"Error cleaning up {temp_file}: {str(e)}")
                break
            
    def process_audio_stream(self, agent, on_response, on_status=None, on_transcription=None):
        """Process continuous audio stream and handle responses"""
        try:
            if on_status:
                on_status("listening", "Listening for speech...")
            
            self.stream.start()
            
            while not self.should_stop:
                try:
                    # Check stop flag more frequently
                    if self.should_stop:
                        break
                        
                    # Get audio chunk
                    chunk, fs = self.record_audio_chunk(duration=0.05)
                    if chunk is None:
                        continue
                        
                    # Process audio
                    if self.is_speech(chunk):
                        if len(self.audio_buffer) % 50 == 0:
                            logger.info(f"Recording speech... ({len(self.audio_buffer)} chunks)")
                            if on_status:
                                on_status("listening", f"Recording speech... ({len(self.audio_buffer)} chunks)")
                        self.audio_buffer.append(chunk)
                    elif self.is_speaking and self.silence_frames >= self.max_silence_frames:
                        # Check if we're already processing
                        if self.processing_lock:
                            logger.warning("Already processing audio, skipping...")
                            continue
                            
                        # Check if processing has been locked for too long (safety check)
                        if hasattr(self, 'processing_start_time') and time.time() - self.processing_start_time > 20:
                            logger.warning("Processing lock timeout, resetting...")
                            self.processing_lock = False
                            
                        logger.info(f"Processing {len(self.audio_buffer)} chunks of speech...")
                        if on_status:
                            on_status("processing", "Processing speech...")
                            
                        if self.audio_buffer:
                            try:
                                self.processing_lock = True
                                self.processing_start_time = time.time()
                                combined_audio = np.concatenate(self.audio_buffer)
                                
                                # Add timeout to prevent hanging
                                response = None
                                processing_error = None
                                
                                def process_with_timeout():
                                    nonlocal response, processing_error
                                    try:
                                        response = self.process_audio(combined_audio, fs, agent, on_transcription)
                                    except Exception as e:
                                        processing_error = e
                                
                                # Start processing in a separate thread with timeout
                                processing_thread = threading.Thread(target=process_with_timeout)
                                processing_thread.daemon = True
                                processing_thread.start()
                                
                                # Wait for processing with timeout (15 seconds)
                                processing_thread.join(timeout=15)
                                
                                if processing_thread.is_alive():
                                    logger.error("Audio processing timed out - killing thread")
                                    if on_status:
                                        on_status("error", "Processing timed out")
                                    processing_error = Exception("Processing timed out")
                                    # Force stop the thread
                                    self.should_stop = True
                                
                                if processing_error:
                                    raise processing_error
                                    
                                if response:
                                    on_response(response)
                                    
                            except Exception as e:
                                logger.error(f"Error during audio processing: {str(e)}")
                                if on_status:
                                    on_status("error", f"Processing error: {str(e)}")
                            finally:
                                # Clear buffer and reset state after processing
                                self.audio_buffer = []
                                self.last_process_time = time.time()
                                self.is_speaking = False
                                self.processing_lock = False
                                # Reset stop flag
                                self.should_stop = False
                                
                except KeyboardInterrupt:
                    logger.info("Stopping audio recording...")
                    self.should_stop = True
                    break
                except Exception as e:
                    logger.error(f"Error in audio loop: {str(e)}")
                    if on_status:
                        on_status("error", f"Audio error: {str(e)}")
                    # Add small delay to prevent rapid error loops
                    time.sleep(1)
                    continue
                
        except Exception as e:
            logger.error(f"Fatal error in audio stream: {str(e)}")
            if on_status:
                on_status("error", f"Fatal audio error: {str(e)}")
        finally:
            # Force stop the stream
            self.should_stop = True
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except:
                    pass
                self.stream = None
            self.audio_buffer = []
            self.processing_lock = False
            self.is_speaking = False
            self.silence_frames = 0
            logger.info("Audio processing stopped") 