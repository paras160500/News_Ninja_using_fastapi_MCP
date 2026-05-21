from tavily import TavilyClient
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage , HumanMessage
import os
load_dotenv()
TAVILY_KEY = os.getenv('TAVILY_API_KEY')
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_news(query):
    client = TavilyClient(api_key=TAVILY_KEY)

    response = client.search(
        query=query,
        search_depth="advanced",   # better results + content
        include_raw_content=True,  # tries to fetch full page text
        max_results=3
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "content": (item.get("content") or "")[:1000]
        })

    return results

def fetch_head_lines(results):
    titles = [item['title'] for item in results if item.get("title")]
    return "\n\n".join(titles)


def summarised_with_llm(headlines : str):
    system_prompt = """
        You are my personal news editor and scriptwriter for a news podcast. Your job is to turn raw headlines into a clean, professional, and TTS-friendly news script.

            The final output will be read aloud by a news anchor or text-to-speech engine. So:
            - Do not include any special characters, emojis, formatting symbols, or markdown.
            - Do not add any preamble or framing like "Here's your summary" or "Let me explain".
            - Write in full, clear, spoken-language paragraphs.
            - Keep the tone formal, professional, and broadcast-style — just like a real TV news script.
            - Focus on the most important headlines and turn them into short, informative news segments that sound natural when spoken.
            - Start right away with the actual script, using transitions between topics if needed.

            Remember: Your only output should be a clean script that is ready to be read out loud.
            """
    
    try:
        llm = ChatMistralAI(
            model = "mistral-small-2506",
            temperature=0.3,
            max_tokens=1000
        )
        response = llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=headlines)
            ]
        )
        return response.content

    except Exception as e:
        print(f"Error :-- {str(e)}")




if __name__ == "__main__":
    topic = input("Enter topic: ")

    news = get_news(topic)

    for item in news:
        print("\n" + "=" * 60)
        print("TITLE:", item["title"])
        print("URL:", item["url"])
        print("\nCONTENT:\n", item["content"])