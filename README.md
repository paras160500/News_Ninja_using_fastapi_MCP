# News Ninja Fast API MCP

A personal news assistant that scrapes news and Reddit discussions, generates a broadcast-style summary using Mistral AI, and converts the final script into downloadable audio using ElevenLabs.

## Project Overview

This repository contains a FastAPI backend and a Streamlit frontend:

- `back-end/back_end_logic.py` - FastAPI app exposing `/generate-news-audio`
- `back-end/news_scraper.py` - news scraping and LLM summarization
- `back-end/reddit_scrapper.py` - Reddit discussion scraping and summarization
- `back-end/broadcast.py` - combines news and Reddit summaries into a broadcast-style script
- `back-end/text_to_speech.py` - converts generated text to audio using ElevenLabs
- `back-end/model.py` - request schema for the API
- `front-end/ui_front_end.py` - Streamlit UI to select topics and trigger audio generation

## Architecture

1. User enters one or more topics in the Streamlit UI.
2. Frontend sends a POST request to the backend at `http://localhost:1234/generate-news-audio`.
3. Backend scrapes news and/or Reddit using `TavilyClient`.
4. Backend generates summaries using Mistral AI and merges them into a broadcast-style script.
5. Generated script is converted into an MP3 audio file and returned to the frontend.

## Features

- Topic-based news scraping via Tavily
- Reddit discussion extraction for topic sentiment and community reaction
- LLM-powered news and Reddit summarization
- Broadcast-style summary generation
- ElevenLabs TTS audio export
- Streamlit web interface with audio playback and download

## Folder Structure

- `back-end/`
  - `back_end_logic.py`
  - `news_scraper.py`
  - `reddit_scrapper.py`
  - `broadcast.py`
  - `text_to_speech.py`
  - `model.py`
  - `utils_news_scrapper.py`
  - `utils_reddit.py`
- `front-end/`
  - `ui_front_end.py`
- `main.py` - placeholder entry point
- `pyproject.toml` - project metadata
- `README.md` - this file

## Requirements

This project targets Python 3.11 and depends on the following packages:

- `fastapi`
- `uvicorn`
- `streamlit`
- `python-dotenv`
- `pydantic`
- `requests`
- `aiolimiter`
- `tavily`
- `elevenlabs`
- `langchain-mistralai`
- `langchain-core`

> Note: The exact package names for Mistral integration may vary based on your environment. If you use a different package or version, adjust accordingly.

## Environment Variables

Create a `.env` file in the repository root with the following keys:

```env
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key
```

If any of these keys are missing, the backend will fail when attempting to call the respective API.

## Installation

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install fastapi uvicorn streamlit python-dotenv pydantic requests aiolimiter tavily elevenlabs langchain-mistralai langchain-core
```

## Running the App

### Start the backend

```powershell
python .\back-end\back_end_logic.py
```

The backend listens on `http://localhost:1234`.

### Start the frontend

```powershell
cd .\front-end
streamlit run ui_front_end.py
```

Open the Streamlit URL shown in the terminal to use the app.

## Usage

1. Enter one or more topics in the Streamlit UI.
2. Choose the data source: `both`, `news`, or `reddit`.
3. Click `Generate Summary`.
4. Listen to the generated audio or download it as `news-summary.mp3`.

## Troubleshooting

### API Error (500): list indices must be integers or slices, not str

This error usually indicates the backend received malformed data or a failed API response inside the summarization pipeline.

Check the following:

- `TAVILY_API_KEY`, `MISTRAL_API_KEY`, and `ELEVEN_API_KEY` are set correctly in `.env`
- Backend logs for exact exception details
- That the backend is running before you click the button in Streamlit
- The correct port and URL in `front-end/ui_front_end.py` (`BACKEND_URL = "http://localhost:1234"`)

### Common failure points

- Missing or invalid ElevenLabs API key causes text-to-speech conversion to fail.
- Tavily search may return empty results or unexpected data structure.
- LLM calls may raise exceptions when service limits are reached or keys are invalid.

## Notes

- `main.py` is a placeholder and not used by the actual app flow.
- `back-end/back_end_logic.py` is the primary FastAPI entrypoint.
- Audio files are saved to the `audio/` folder when generated.

## Future Improvements

- Add request validation and better error responses in the API.
- Improve retry handling for external API calls.
- Add caching for repeated topic requests.
- Support more voices or TTS providers.
- Add a dedicated frontend launch script.
