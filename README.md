# RAgent (Robot Agent)

**RAgent (Robot Agent)** is for creating agents that can hold LLM-powered STT/TTS conversations, provide a web interface, and even be physically mobile. RAgent runs on a core audio loop where it listens for speech and records it, converts it to text, then sends it as a prompt to an LLM along with instructions. The resulting text output is either converted to speech or displayed in a web browser. 

## The RAgents So Far
1. Nevil - a talking PiCar robot built using a Raspberry Pi (8GB RAM) and onboard SST and LLM (TinyLlama)
2. Blake - a smart but slow agent that employs API calls for TTS (Whisper) and ChatGPT (Nevil may employ Blake for advanced questions and situations)
2. Cliff - a PC-based web agent that listens to conversations and provides a browser-based HUD for technical terms employing a local STT (Whisper/Vosk) and ChatGPT

## RAgent Options
- Interface: Speech(mic/speaker w/ STT/TTS), Text on web browser 
- Speech-to-Text: OpenAI Whisper API, Whisper local, and Vosk
- LLM: ChatGPT, TinyLlama (for Raspberry Pi-driven robots)
