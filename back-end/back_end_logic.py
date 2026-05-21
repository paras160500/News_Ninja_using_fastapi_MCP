from fastapi import FastAPI,HTTPException,File,Response
from dotenv import load_dotenv
from model import NewsRequest
from news_scraper import NewsScraper
from reddit_scrapper import RedditScrapper
from broadcast import *

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
        audio_path = convert_text_to_audio(news_summary)

        if audio_path:
            return response , header , etc 
    
    except Exception as e:
        raise HTTPException(status_code=500 , detail = str(e))

