from utils_news_scrapper import *
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv
import os 
from typing import List,Dict 
import asyncio


load_dotenv()


class NewsScraper:
    _rate_limiter = AsyncLimiter(5,1)

    async def scrap_news(self , topics : List[str]) -> Dict[str,str]:
        """Scrape and Analyse the news topic"""
        results = {}

        for topic in topics:
            async with self._rate_limiter:
                try:
                    results = get_news(query=topic)
                    headlines = fetch_head_lines(results=results)
                    summary = summarised_with_llm(headlines=headlines)
                    results[topic] = summary
                except Exception as e:
                    results[topic] = f"Error : {str(e)}"
                await asyncio.sleep(1)
        
        return {"news_analysis" : results}