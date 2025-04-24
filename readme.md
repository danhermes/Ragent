# RAgent (Robot Agent)

**RAgent (Robot Agent)** is an AI framework for creating and organizing agents and agentic workflows.

RAgent facilitates the construction of AI agents individually, in a team, as needed, or autonomously.
Directed by the user via HQ (Headquarters), RAgent's agents can build all kinds of stuff, such as:
    - technical specifications
    - automation workflows (implemented and running)
    - python modules and scripts
    - publications (post, article, book)

RAgents have tools(apis)) at their disposal to allow them to write code (Autocoder), write books (LitLegos), proofread books (Proofer), and automate tasks (n8n). YAMLgen is an adapter that can help translate between agents and tools.

## The Ragers
An autonomous organization of agents, loosely configured in a hierarchy (director, manager, worker, SME), that take a goal, discuss it, and develop it into a written deliverable such as a business strategy or a technical specification.

## HQ(Headquarters)
User interfaces into RAgent, from CLI, to web UI, to voice interface.  Creates and tracks agent tasks.
- Command Line Interface (CLI) and task dispatcher for RAgent
- Voice - mic/speaker w/ STT/TTS) - OpenAI Whisper API, Whisper local, and Vosk
- Text on web browser or mobile device

## RAgents Tools and Adapters: APIs
- AutoCoder - codes (Python), tests (pytest), and debugs (in temp Docker containers) against a technical spec
- LitLegos - writes a book given a book title and Table of Contents
- Proofer - proofreads a manuscript
- n8n - for creating and uploading autonomous n8n workflows

## The Vision:
    Idea -> Manifestation

    Goal -> Tech Specification -> Implementation -> Deliverable

    Goal -> Ragers -> Tools and Adapters: YAMLgen,  Autocoder, APIs, etc.  -> Deliverable

    Deliverables:
    - technical specifications
    - automation workflows (implemented and running)
    - python modules and scripts
    - publications (post, article, book)