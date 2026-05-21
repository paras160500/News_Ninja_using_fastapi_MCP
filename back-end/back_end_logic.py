from fastapi import FastAPI,HTTPException,File,Response
from dotenv import load_dotenv
from model import NewsRequest
from news_scraper import NewsScraper
from reddit_scrapper import RedditScrapper
from broadcast import *
from text_to_speech import text_to_audio_elevenlabs_sdk
import uvicorn

load_dotenv()
app = FastAPI()

@app.post("/generate-news-audio")
async def generate_news_audio(request : NewsRequest):
    try:
        results = {}

        if request.source_type in ['news' , 'both']:
            news_scrapper = NewsScraper()
            results['news'] = await news_scrapper.scrap_news(topics=request.topics)

        if request.source_type in ['both' , 'reddit']:
            reddit_scrapper = RedditScrapper()
            results['reddit'] = await reddit_scrapper.scrap_reddit_post(topics=request.topics)
        
        news_data = results.get("news",{})
        reddit_data = results.get("reddit" , {})
        
        
        # Setup LLM Summariser
        news_summary = generate_broadcast(news_data , reddit_data,topics=request.topics)

        # Convert summary to Audio
        audio_path = text_to_audio_elevenlabs_sdk(
                text = news_summary,
                voice_id = "JBFqnCBsd6RMkjVDRZzb",
                model_id = "eleven_multilingual_v2",
                output_format = "mp3_44100_128",
                output_dir = "audio"
            )

        if audio_path:
            with open(audio_path , "rb") as f:
                audio_bytes = f.read()

            return Response(
                content = audio_bytes , 
                media_type = "audio/mpeg" , 
                headers = {"Content-Disposition": "attachment; filename=news-summary.mp3"}
            )
    
    except Exception as e:
        raise HTTPException(status_code=500 , detail = str(e))

if __name__ == "__main__":
    uvicorn.run(
        "back_end_logic:app",
        host="0.0.0.0",
        port=1234,
        reload=True
    )