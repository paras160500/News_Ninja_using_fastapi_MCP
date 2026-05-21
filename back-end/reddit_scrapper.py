from utils_reddit import *
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv
import os 
from typing import List,Dict 
import asyncio


load_dotenv()


class RedditScrapper:
    _rate_limiter = AsyncLimiter(5,1)

    async def scrap_reddit_post(self , topics : List[str]) -> Dict[str,str]:
        """Scrape and Analyse the reddit discussion"""
        results = {}

        for topic in topics:
            async with self._rate_limiter:
                try:
                    r_data = get_reddit_data(query=topic)
                    summary = summarize(r_data)
                    results[topic] = summary
                except Exception as e:
                    results[topic] = f"Error : {str(e)}"
                await asyncio.sleep(1)
        
        return {"reddit_analysis" : results}
    