# RAgent (Robot Agent)

**RAgent (Robot Agent)** is a framework for creating and organizing agents and agentic workflows.

RAgent facilitates the construction of agents individually, in a team, as needed, or autonomously.

RAgents have tools(toys) at their disposal to allow them to write code (Autocoder), write books (LitLegos), proofread books (Proofer), and automate tasks (n8n).

## The RAgents So Far
1. The Ragers - an autonomous organization of agents, loosely configured in a hierarchy (director, manager, worker), that take a goal, discuss it, and develop it into a written deliverable such as a business strategy or a technical specification
2. Cliff - a PC-based web agent that listens to conversations ambiently and provides a browser-based HUD for technical terms employing a local STT (Whisper/Vosk) and ChatGPT
3. Nevil - a talking PiCar robot built using a Raspberry Pi (8GB RAM) and onboard SST and LLM (TinyLlama). Converses wittily, plays autonomously, and has a basic RAG function whereby it can stay abreast of your schedule and goals for the week.

## Human Interfaces
- Voice - mic/speaker w/ STT/TTS) - OpenAI Whisper API, Whisper local, and Vosk
- Text on web browser or mobile device
- Command line

## Brains: GPTs and LLMs
- ChatGPT
- Gemma2b, TinyLlama (for Raspberry Pi-driven robots)

## RAgents' Toys - Agentic APIs
- AutoCoder - codes (Python), tests (pytest), and debugs (in temp Docker containers) against a technical spec
- LitLegos - writes a book given a book title and Table of Contents
- Proofer - proofreads a manuscript
- n8n - for creating and uploading autonomous n8n workflows