import streamlit as st
import sounddevice as sd
import numpy as np
import os
import soundfile as sf
from commands import CommandAgent
from agents import DEFAULT_AGENT
from agents.base_agent import AgentType
from speech_to_text import LocalWhisperSTT, OpenAIWhisperSTT, VoskSTT
from llm import BaseLLM, ChatGPTLLM, TinyLlamaLLM
import re
import time
import torch
import logging

# Configure logging
logger = logging.getLogger("streamlit")
logger.setLevel(logging.DEBUG)
# Add console handler if not already present
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(console_handler)

class AudioView:
    def __init__(self, agent=None):
        # Check if already initialized
        if 'audio_view_instance' in st.session_state:
            print("⚠️ AudioView already initialized, reusing existing instance")
            return
            
        print("Initializing AudioView...")  # Debug print
        st.session_state.audio_view_instance = True
        
        self.agent = agent if agent else DEFAULT_AGENT()
        self.command_agent = CommandAgent(agent=self.agent)
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'timing_container' not in st.session_state:
            st.session_state.timing_container = st.empty()
        
        # Initialize audio stream
        self.stream = None
        self.should_stop = False

        # Initialize STT model only if not already in session state
        if 'stt_model' not in st.session_state:
            try:
                print("Initializing speech-to-text model...")
                stt = LocalWhisperSTT()  # Default to local Whisper
                stt.initialize()
                st.session_state.stt_model = stt
                print("Speech-to-text model initialized successfully")
            except Exception as e:
                print(f"Error initializing speech-to-text: {str(e)}")
                raise
        
        # Initialize LLM only if not already in session state
        if 'llm_model' not in st.session_state:
            try:
                print("Initializing language model...")
                llm = ChatGPTLLM()  # Default to ChatGPT
                llm.initialize()
                st.session_state.llm_model = llm
                print("Language model initialized successfully")
            except Exception as e:
                print(f"Error initializing language model: {str(e)}")
                raise
        
        self.stt = st.session_state.stt_model
        self.llm = st.session_state.llm_model
        self.is_speaking = False
        self.silence_frames = 0
        self.max_silence_frames = 20  # 1 second of silence (20 * 50ms)

    def record_audio(self, filename, duration=5):
        #st.write("Recording...")
        fs = 44100  # Sample rate
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        sf.write(filename, myrecording, fs)
        #st.write("Recording finished!")

    def play_audio(self, filename):
        if os.path.exists(filename):
            st.audio(filename)
        else:
            st.error("Audio file not found!")

    def format_message(self, text):
        # Split the text into separate entries based on double newlines or ---
        entries = re.split(r'\n\s*---\s*\n|\n\s*\n\s*\n', text)
        
        formatted_entries = []
        for entry in entries:
            # Remove leading/trailing whitespace while preserving internal newlines
            entry = entry.strip()
            
            # Look for the term at the start (any text up to first newline)
            match = re.match(r'^([^\n]+)\n(.*)$', entry, re.DOTALL)
            if match:
                term, content = match.groups()
                # Clean up the term
                term = term.strip()
                term = re.sub(r'\*\*|\*|#\s*', '', term)  # Remove any markdown
                
                # Process the content
                content = content.strip()
                
                # Split into first sentence and remaining text
                sentence_match = re.match(r'^([^.!?]+[.!?])\s*(.*)$', content, re.DOTALL)
                if sentence_match:
                    first_sentence, remaining = sentence_match.groups()
                    remaining = remaining.strip()
                    formatted_entries.append(
                        f'<div class="chat-message">'
                        f'<div class="term">{term}</div>'
                        f'<div class="first-sentence">{first_sentence.strip()}</div>'
                        f'<div class="remaining-text">{remaining}</div>'
                        f'</div>'
                    )
                else:
                    # If no clear sentence break, treat all content as first sentence
                    formatted_entries.append(
                        f'<div class="chat-message">'
                        f'<div class="term">{term}</div>'
                        f'<div class="first-sentence">{content}</div>'
                        f'</div>'
                    )
            else:
                # If no clear term found, treat entire entry as content
                formatted_entries.append(
                    f'<div class="chat-message">'
                    f'<div class="first-sentence">{entry}</div>'
                    f'</div>'
                )
        
        return ''.join(formatted_entries)

    def display_text_response(self, text):
        # Basic validation
        if not text or not text.strip():
            print("⚠️ Empty response received, skipping display")
            return
            
        print("\n📤 Adding response to chat history...")
        print("=" * 50)
        print(text)
        print("=" * 50)
            
        # Add response to chat history
        st.session_state.chat_history.insert(0, text)
        
        # Update the chat container content
        if 'chat_container' in st.session_state:
            print("🔄 Updating UI with new message...")
            
            # Build chat HTML
            chat_html = '<div class="chat-container">'
            for message in st.session_state.chat_history:
                chat_html += self.format_message(message)
            chat_html += '</div>'
            
            # Force UI update
            try:
                st.session_state.chat_container.markdown(chat_html, unsafe_allow_html=True)
                print("✅ UI update complete")
            except Exception as e:
                print(f"❌ Error updating UI: {str(e)}")
                import traceback
                print(traceback.format_exc())

    def is_speech(self, audio_chunk, threshold=0.005):  # Increased threshold further
        """Better voice activity detection"""
        try:
            # Safety check for invalid input
            if audio_chunk is None or len(audio_chunk) == 0:
                return False
                
            # Safer RMS calculation to avoid overflow
            audio_chunk = audio_chunk.astype(np.float64)  # Convert to double precision
            squared = np.clip(audio_chunk**2, 0, 1)  # Clip to avoid overflow
            rms = np.sqrt(np.mean(squared))
            
            # Update speech state
            if rms > threshold:
                self.silence_frames = 0
                if not self.is_speaking:
                    self.is_speaking = True
                    print(f"🎤 Speech started - RMS: {rms:.6f}")
                return True
            else:
                self.silence_frames += 1
                if self.silence_frames >= self.max_silence_frames:
                    if self.is_speaking:
                        print(f"🔇 Speech ended - Buffer size: {len(st.session_state.audio_buffer)}")
                        # Only end speech if we have enough audio
                        if len(st.session_state.audio_buffer) < 10:  # At least 0.5 seconds (10 * 50ms)
                            print("⚠️ Speech too short, continuing recording...")
                            self.silence_frames = 0
                            return True
                    # Don't set is_speaking to False here - let the main loop do it after processing
                return False
        except Exception as e:
            print(f"Error in speech detection: {e}")
            return False

    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up resources...")
        try:
            if self.stream:
                self.stream.abort()  # Force stop immediately
                self.stream.close()
                self.stream = None
            sd.stop()  # Stop all sounddevice streams
        except Exception as e:
            print(f"Error during cleanup: {e}")
        print("Cleanup complete")

    def record_audio_chunk(self, duration=0.05):  # 50ms chunks
        """Record a chunk of audio and return the numpy array and sample rate"""
        try:
            fs = 16000  # 16kHz for speech
            frames = int(duration * fs)
            # Use blocking=True since it's a short duration
            recording = sd.rec(frames, samplerate=fs, channels=1, dtype=np.float32, blocking=True)
            
            # Safety check for invalid audio data
            if recording is None or np.any(np.isnan(recording)) or np.any(np.isinf(recording)):
                print("⚠️ Invalid audio data detected in recording")
                return np.zeros((frames, 1), dtype=np.float32), fs
                
            # Ensure correct shape
            if recording.shape != (frames, 1):
                print(f"⚠️ Unexpected recording shape: {recording.shape}, reshaping...")
                recording = recording.reshape((frames, 1))
            
            # Clip to prevent overflow
            recording = np.clip(recording, -1.0, 1.0)
            
            return recording, fs
        except Exception as e:
            print(f"Error recording audio: {str(e)}")
            # Return silent audio instead of raising
            return np.zeros((frames, 1), dtype=np.float32), fs

    def process_audio_chunk(self, chunk, fs):
        """Process audio chunk using speech-to-text and LLM"""
        print(f"\n🔍 Starting processing of audio chunk: {len(chunk)/fs:.2f}s")
        
        # Safety check for invalid audio data
        try:
            max_amp = np.max(np.abs(chunk))
            mean_amp = np.mean(np.abs(chunk))
            if max_amp > 1.0 or np.isnan(max_amp) or np.isinf(max_amp):
                print("❌ Invalid audio data detected (amplitude out of bounds)")
                return None
                
            print(f"🔊 Audio stats - Max amplitude: {max_amp:.6f}, Mean: {mean_amp:.6f}")
            
            # Check if audio is long enough
            duration = len(chunk)/fs
            if duration < 0.5:  # Minimum 0.5 seconds
                print(f"❌ Audio too short ({duration:.2f}s < 0.5s)")
                return None
                
            # Save chunk to temporary file
            temp_file = "temp_chunk.wav"
            try:
                print("💾 About to save audio...")
                sf.write(temp_file, chunk, fs)
                print("💾 Saved audio to temp file")
                
                # Verify the file was written correctly
                if os.path.exists(temp_file):
                    file_size = os.path.getsize(temp_file)
                    print(f"📁 Temp file size: {file_size} bytes")
                    if file_size < 1000:  # File too small
                        print("❌ Audio file too small")
                        return None
                else:
                    print("❌ Temp file not created!")
                    return None
                
                # Start STT timing
                print("🎯 Starting speech-to-text transcription...")
                
                try:
                    # Transcribe audio
                    text, stt_time = self.stt.transcribe(temp_file)
                    print(f"✨ Transcription result: '{text}'")
                    
                    if text:  # Only process if there's actual text
                        # Start LLM timing
                        print("\n🤖 Starting LLM processing...")
                        print("=" * 50)
                        print("Sending prompt to LLM:")
                        print(f"Text: {text}")
                        print("=" * 50)
                        
                        try:
                            response, llm_time = self.llm.generate_response(text)
                            
                            print("\n💬 LLM Response:")
                            print("=" * 50)
                            print(response)
                            print("=" * 50)
                            
                            print(f"⏱️ TIMING - STT: {stt_time:.2f}s, LLM: {llm_time:.2f}s, Total: {(stt_time + llm_time):.2f}s")
                            
                            return response
                        except Exception as e:
                            print(f"❌ Error in LLM processing: {str(e)}")
                            return None
                    else:
                        print("❌ No text detected in audio")
                        return None
                        
                except Exception as e:
                    print(f"❌ Error in speech-to-text transcription: {str(e)}")
                    return None
                
            except Exception as e:
                print(f"❌ Error in audio file handling: {str(e)}")
                return None
            
        except Exception as e:
            print(f"❌ Error in audio processing: {str(e)}")
            return None
            
        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass

    def audio_view(self):
        # Check if audio view is already running
        if 'audio_view_running' in st.session_state and st.session_state.audio_view_running:
            print("⚠️ Audio view already running, skipping initialization")
            return
            
        print("\n🚀 Starting audio view - Press Ctrl+C to stop\n")
        st.session_state.audio_view_running = True
        
        try:
            # Initialize session state variables
            if 'audio_buffer' not in st.session_state:
                st.session_state.audio_buffer = []
            if 'chat_container' not in st.session_state:
                st.session_state.chat_container = st.container()
            if 'last_process_time' not in st.session_state:
                st.session_state.last_process_time = time.time()
            
            # Format agent name
            agent_name = "Agent " + self.agent.__class__.__name__.replace("Agent", "")
            
            # Create header once
            st.markdown("""
            <style>
            /* Remove default Streamlit padding */
            .block-container {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                margin-top: 0 !important;
            }
            
            /* Fixed header */
            .header-container {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                height: 60px;
                background: #ffffff;
                z-index: 1000;  /* Increased z-index */
                padding: 1rem;
                border-bottom: 1px solid #eee;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* Added shadow for visual separation */
            }
            
            .header-container h1 {
                margin: 0;
                font-size: 24px;
                font-weight: 600;
                color: #000000;
            }
            
            /* Chat container positioning */
            .chat-container {
                position: relative;
                margin-top: 80px !important;  /* Increased margin to ensure content starts below header */
                padding: 1rem;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                color: #000000;
                z-index: 1;  /* Lower z-index than header */
            }
            
            .chat-message {
                margin-bottom: 2rem;
                background: #ffffff;  /* Ensure messages have white background */
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            }
            
            .term {
                font-size: 28px;
                font-weight: 600;
                margin-bottom: 0.7rem;
                color: #000000;
            }
            
            .first-sentence {
                font-size: 18px;
                margin-bottom: 0.5rem;
                color: #000000;
            }
            
            .remaining-text {
                font-size: 16px;
                color: #000000;
                margin-top: 0.5rem;
                line-height: 1.4;
            }

            /* Ensure Streamlit components don't overlap */
            .stApp {
                margin-top: 60px;  /* Match header height */
            }
            </style>
            """, unsafe_allow_html=True)

            # Create main container with header
            st.markdown("""
            <div class="header-container">
                <h1>Agent Cliff</h1>
            </div>
            """, unsafe_allow_html=True)
            
            # Create chat container with explicit height
            if 'chat_container' not in st.session_state:
                st.session_state.chat_container = st.container()
            
            # Initialize chat container with current history
            chat_html = '<div class="chat-container">'
            # First pass: collect all terms
            terms_messages = []
            other_messages = []
            for message in st.session_state.chat_history:
                formatted = self.format_message(message)
                if '<div class="term">' in formatted:
                    terms_messages.append(formatted)
                else:
                    other_messages.append(formatted)
            
            # Combine terms first, then other messages
            chat_html += ''.join(terms_messages)
            chat_html += ''.join(other_messages)
            chat_html += '</div>'
            st.session_state.chat_container.markdown(chat_html, unsafe_allow_html=True)
            
            try:
                while True:
                    try:
                        # Record small chunk
                        chunk, fs = self.record_audio_chunk(duration=0.05)
                        
                        # Check for speech
                        if self.is_speech(chunk):
                            # Only print buffer size every 50 chunks
                            if len(st.session_state.audio_buffer) % 50 == 0:
                                print(f"📝 Recording... ({len(st.session_state.audio_buffer)} chunks)")
                            st.session_state.audio_buffer.append(chunk)
                        elif self.is_speaking and self.silence_frames >= self.max_silence_frames:
                            print(f"\n🔄 Processing speech - {len(st.session_state.audio_buffer)} chunks collected")
                            if st.session_state.audio_buffer:
                                try:
                                    print("⚡ Attempting to concatenate audio chunks...")
                                    # Debug buffer contents
                                    print(f"📈 First chunk shape: {st.session_state.audio_buffer[0].shape}")
                                    print(f"📈 Last chunk shape: {st.session_state.audio_buffer[-1].shape}")
                                    print(f"📈 Number of chunks: {len(st.session_state.audio_buffer)}")
                                    
                                    try:
                                        combined_audio = np.concatenate(st.session_state.audio_buffer)
                                        print(f"✅ Concatenation successful")
                                    except Exception as e:
                                        print(f"❌ Concatenation failed: {str(e)}")
                                        print(f"📈 Chunk shapes: {[chunk.shape for chunk in st.session_state.audio_buffer]}")
                                        raise
                                    
                                    duration = len(combined_audio)/fs
                                    print(f"📊 Audio length: {duration:.2f}s ({len(combined_audio)} samples)")
                                    print(f"📊 Combined shape: {combined_audio.shape}")
                                    
                                    print("🚀 About to call process_audio_chunk...")
                                    response = self.process_audio_chunk(combined_audio, fs)
                                    print("✅ process_audio_chunk completed")
                                    
                                    if response:
                                        print("📝 Got response, updating UI...")
                                        if self.agent.agent_type == AgentType.TEXT:
                                            self.display_text_response(response)
                                        else:
                                            st.audio(response, format='audio/wav', start_time=0)
                                except Exception as e:
                                    print(f"❌ Error during audio processing: {str(e)}")
                                    import traceback
                                    print(traceback.format_exc())
                                finally:
                                    # Clear buffer and reset state after processing
                                    st.session_state.audio_buffer = []
                                    st.session_state.last_process_time = time.time()
                                    self.is_speaking = False  # Set is_speaking to False here, after processing
                    except KeyboardInterrupt:
                        print("\n⛔ Stopping audio recording...")
                        break
                    except Exception as e:
                        print(f"Error in audio loop: {str(e)}")
                        continue
                    
            finally:
                sd.stop()
                st.session_state.audio_view_running = False
                print("Audio view stopped") 
        except Exception as e:
            print(f"Error in audio view: {str(e)}")
            raise  # Re-raise the exception after cleanup
        finally:
            sd.stop()
            st.session_state.audio_view_running = False
            print("Audio view stopped") 