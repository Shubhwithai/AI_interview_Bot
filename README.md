# Vapi Voice Assistant Streamlit App

This is a Streamlit application that integrates with the Vapi AI Python SDK to create a voice-to-voice assistant experience.

## Features

- Real-time voice interaction with AI assistants
- Customizable assistant parameters (model, voice, context)
- Option to use existing Vapi assistants or create custom ones
- Simple and intuitive UI

## Prerequisites

- Python 3.7+
- Vapi API Key (get it from [Vapi Dashboard](https://dashboard.vapi.ai/))
- Microphone access

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. On Mac, you might need to install PortAudio for PyAudio to work:

```bash
brew install portaudio
```

4. Create a `.env` file based on the `.env.example` file and add your Vapi API key:

```
VAPI_API_KEY=your-vapi-api-key
```

## Usage

1. Start the Streamlit app:

```bash
streamlit run app.py
```

2. Configure your assistant settings or use an existing assistant ID
3. Click "Start Call" to begin the voice conversation
4. Speak into your microphone to interact with the assistant
5. Click "Stop Call" when you're done

## Configuration Options

- **Assistant ID**: Optional ID of an existing Vapi assistant
- **First Message**: The initial message the assistant will say
- **Assistant Context**: Instructions for the AI assistant's behavior
- **Model**: AI model to use (GPT-3.5, GPT-4, Claude, etc.)
- **Voice**: Voice to use for the assistant's speech
- **Recording Enabled**: Whether to record the conversation
- **Interruptions Enabled**: Whether the assistant can be interrupted while speaking

## Troubleshooting

- Make sure your browser has permission to access your microphone
- If you encounter issues with PyAudio, try installing PortAudio first
- Check that your Vapi API key is correctly set in the `.env` file or entered in the app

## License

MIT License
