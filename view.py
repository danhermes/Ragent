import streamlit as st
import sounddevice as sd
import numpy as np
import os
import soundfile as sf
from commands import CommandAgent

class AudioView:
    def __init__(self):
        self.command_agent = CommandAgent()

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

    def audio_view(self):

        # Upload audio file
        # uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

        # if uploaded_file is not None:
        #     # Save the uploaded file temporarily
        #     input_file = "uploaded_audio.wav"
        #     with open(input_file, "wb") as f:
        #         f.write(uploaded_file.getbuffer())
        #     st.success("File uploaded successfully!")

        #     # Send to ChatGPT button
        #     if st.button("Send to ChatGPT"):
        #         response_file = self.command_agent.process_audio_command("chat", input_file)
        #         if response_file:
        #             st.success("Received response from ChatGPT!")
        #             self.play_audio(response_file)
        #         else:
        #             st.error("Failed to get response from ChatGPT")

        # Record audio button
        if st.button("Record"):
            record_file = "recorded_audio.wav"
            self.record_audio(record_file)
            #st.success("Audio recorded successfully!")

            # Automatically send to ChatGPT
            response_file = self.command_agent.process_audio_command("chat", record_file)
            if response_file:
                #st.success("Received response from ChatGPT!")
                st.audio(response_file, format='audio/wav', start_time=0, autoplay=True)
            else:
                st.error("Failed to get response from ChatGPT") 