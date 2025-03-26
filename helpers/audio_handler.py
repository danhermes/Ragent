import sounddevice as sd
import numpy as np
import soundfile as sf
import os
import logging
import wave
from typing import Optional, Tuple
import time

logger = logging.getLogger("streamlit")
logger.setLevel(logging.DEBUG)

class AudioHandler:
    """Handles audio input/output operations"""
    
    def __init__(self):
        self.sample_rate = 16000
        self.channels = 1
        self.dtype = np.float32
        self.is_speaking = False
        self.silence_frames = 0
        self.max_silence_frames = 30  # 1.5 seconds of silence
        self.speech_threshold = 0.005  # Lowered from 0.01 to be more sensitive
        self.stream = None
        self.audio_buffer = []
        self.processing_lock = False
        self.last_process_time = 0
        self.initialize()
        
    def initialize(self):
        """Initialize audio stream"""
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                callback=self._audio_callback
            )
            self.stream.start()
            logger.info("Audio stream initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing audio stream: {str(e)}")
            raise
            
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        if status:
            logger.warning(f"Audio callback status: {status}")
            
    def record_audio(self, filename, duration=5):
        """Record audio for a specified duration"""
        fs = 44100  # Sample rate
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        sf.write(filename, myrecording, fs)
        
    def record_audio_chunk(self, duration: float = 0.05) -> Tuple[np.ndarray, int]:
        """Record a short audio chunk"""
        try:
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
            
    def process_audio(self, audio_data: np.ndarray, sample_rate: int, agent) -> Optional[str]:
        """Process audio data through STT and LLM"""
        logger.info(f"\nStarting processing of audio: {len(audio_data)/sample_rate:.2f}s")
        
        # Safety check for invalid audio data
        try:
            max_amp = np.max(np.abs(audio_data))
            mean_amp = np.mean(np.abs(audio_data))
            if max_amp > 1.0 or np.isnan(max_amp) or np.isinf(max_amp):
                logger.error("Invalid audio data detected (amplitude out of bounds)")
                return None
                
            logger.info(f"Audio stats - Max amplitude: {max_amp:.6f}, Mean: {mean_amp:.6f}")
            
            # Check if audio is long enough
            duration = len(audio_data)/sample_rate
            if duration < 0.1:  # Minimum 0.1 seconds
                logger.error(f"Audio too short ({duration:.2f}s < 0.1s)")
                return None
                
            # Save chunk to temporary file
            temp_file = "temp_chunk.wav"
            try:
                if not self.save_audio_chunk(audio_data, sample_rate, temp_file):
                    logger.error("Failed to save audio chunk")
                    return None
                
                # Verify file exists and has content
                if not os.path.exists(temp_file):
                    logger.error("Temporary file not created")
                    return None
                    
                file_size = os.path.getsize(temp_file)
                logger.info(f"Saved audio file size: {file_size} bytes")
                
                if file_size == 0:
                    logger.error("Saved audio file is empty")
                    return None
                
                # Transcribe audio
                logger.info("Starting speech-to-text transcription...")
                text = agent.transcribe_audio(temp_file)
                logger.info(f"Transcription result: '{text}'")
                
                if text:  # Only process if there's actual text
                    # Get LLM response
                    logger.info("\nStarting LLM processing...")
                    logger.info("=" * 50)
                    logger.info(f"Sending prompt to LLM: {text}")
                    logger.info("=" * 50)
                    
                    try:
                        response = agent.get_chat_response(text)
                        
                        logger.info("\nLLM Response:")
                        logger.info("=" * 50)
                        logger.info(response)
                        logger.info("=" * 50)
                        
                        return response
                    except Exception as e:
                        logger.error(f"Error in LLM processing: {str(e)}")
                        return None
                else:
                    logger.error("No text detected in audio")
                    return None
                    
            except Exception as e:
                logger.error(f"Error in speech-to-text transcription: {str(e)}")
                return None
            
        except Exception as e:
            logger.error(f"Error in audio processing: {str(e)}")
            return None
            
        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.info("Cleaned up temporary audio file")
            except Exception as e:
                logger.error(f"Error cleaning up temporary file: {str(e)}")
                
    def process_audio_stream(self, agent, on_response):
        """Process continuous audio stream and handle responses"""
        try:
            while True:
                try:
                    # Get audio chunk
                    chunk, fs = self.record_audio_chunk()
                    if chunk is None:
                        continue
                        
                    # Process audio
                    if self.is_speech(chunk):
                        if len(self.audio_buffer) % 50 == 0:
                            logger.info(f"Recording... ({len(self.audio_buffer)} chunks)")
                        self.audio_buffer.append(chunk)
                    elif self.is_speaking and self.silence_frames >= self.max_silence_frames:
                        # Check if we're already processing
                        if self.processing_lock:
                            logger.warning("Already processing audio, skipping...")
                            continue
                            
                        logger.info(f"\nProcessing speech - {len(self.audio_buffer)} chunks collected")
                        if self.audio_buffer:
                            try:
                                self.processing_lock = True
                                logger.info("Attempting to concatenate audio chunks...")
                                # Debug buffer contents
                                logger.info(f"First chunk shape: {self.audio_buffer[0].shape}")
                                logger.info(f"Last chunk shape: {self.audio_buffer[-1].shape}")
                                logger.info(f"Number of chunks: {len(self.audio_buffer)}")
                                
                                try:
                                    combined_audio = np.concatenate(self.audio_buffer)
                                    logger.info("Concatenation successful")
                                except Exception as e:
                                    logger.error(f"Concatenation failed: {str(e)}")
                                    logger.error(f"Chunk shapes: {[chunk.shape for chunk in self.audio_buffer]}")
                                    raise
                                
                                duration = len(combined_audio)/fs
                                logger.info(f"Audio length: {duration:.2f}s ({len(combined_audio)} samples)")
                                logger.info(f"Combined shape: {combined_audio.shape}")
                                
                                logger.info("About to call process_audio...")
                                response = self.process_audio(combined_audio, fs, agent)
                                logger.info("process_audio completed")
                                
                                if response:
                                    logger.info("Got response, calling callback...")
                                    on_response(response)
                                    
                            except Exception as e:
                                logger.error(f"Error during audio processing: {str(e)}")
                                import traceback
                                logger.error(traceback.format_exc())
                            finally:
                                # Clear buffer and reset state after processing
                                self.audio_buffer = []
                                self.last_process_time = time.time()
                                self.is_speaking = False
                                self.processing_lock = False
                except KeyboardInterrupt:
                    logger.info("\nStopping audio recording...")
                    break
                except Exception as e:
                    logger.error(f"Error in audio loop: {str(e)}")
                    continue
                
        finally:
            self.cleanup()
            logger.info("Audio processing stopped")
            
    def cleanup(self):
        """Clean up audio resources"""
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
                logger.info("Audio stream cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up audio resources: {str(e)}") 