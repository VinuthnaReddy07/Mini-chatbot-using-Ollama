# MiniGPT

MiniGPT is a lightweight chat interface built with Streamlit and Ollama. It runs language models locally and streams their responses into a web-based chat UI.

## Features

- Chat with locally available Ollama models
- Stream responses as they are generated
- Keep multiple conversations and switch between them during a session
- Adjust temperature and top-p sampling settings
- Customize the assistant's system instructions
- Start a conversation from a set of example prompts
- View Ollama connection status and available models

## Requirements

- Python 3.11 or newer
- [Ollama](https://ollama.com/) installed and running
- The default model, `qwen2.5:1.5b`, downloaded in Ollama (or another model available locally)

## Setup

1. Clone this repository and open a terminal in the project directory.
2. Create and activate a virtual environment:

   **Windows (PowerShell):**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the Python dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start Ollama and download the default model:

   ```bash
   ollama pull qwen2.5:1.5b
   ```

   Ollama should be reachable at `http://localhost:11434`, which is the URL configured by the app.

5. Launch MiniGPT:

   ```bash
   streamlit run frontend/app.py
   ```

   Streamlit prints a local URL (usually `http://localhost:8501`) to open in your browser.

## Using another model

Download a model with Ollama, for example:

```bash
ollama pull llama3.2
```

When Ollama is running, MiniGPT lists the models it discovers in the **Language Model** selector. The default model can also be used as configured in `frontend/app.py`.

## Project structure

```text
.
├── frontend/
│   └── app.py          # Streamlit UI, conversation state, and Ollama client
├── requirements.txt    # Python dependencies
├── README.md
└── ARCHITECTURE.md
```

## Notes

- Conversation history and settings are held in Streamlit session state; they are not saved to a database or file and are not intended to persist between sessions.
- The app sends requests to the local Ollama service. Keep Ollama running while chatting.
- Model output quality and response speed depend on the selected model and the available hardware.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the application components and request flow.
