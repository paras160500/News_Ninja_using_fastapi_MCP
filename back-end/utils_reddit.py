from tavily import TavilyClient
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage

import os

# Load API keys
load_dotenv()

TAVILY_KEY = os.getenv("TAVILY_API_KEY")


# =========================
# GET REDDIT DISCUSSIONS
# =========================

def get_reddit_data(query):

    client = TavilyClient(api_key=TAVILY_KEY)

    response = client.search(

        query=f"{query} site:reddit.com/r/",

        topic="news",   # gets recent data

        days=3,         # last 3 days

        max_results=3,

        search_depth="advanced",

        include_raw_content=True
    )

    results = []

    for item in response["results"]:

        results.append({

            "title": item["title"],

            "url": item["url"],

            "content": (
                item.get("raw_content")
                or item.get("content")
                or ""
            )[:2000]

        })

    return results


# =========================
# SUMMARIZE WITH MISTRAL
# =========================

def summarize(data):

    text = ""

    for item in data:

        text += f"""

Title: {item['title']}

Content:
{item['content']}

"""

    system_prompt =  """
You are an expert Reddit discussion analyst and news scriptwriter.

Your task is to analyze recent Reddit discussions and turn them into a clean, professional, and natural-sounding news summary.

Focus on:
- the main topic people are discussing
- overall public sentiment
- repeated opinions and reactions
- major concerns, criticism, or excitement
- important insights and trends

Ignore:
- memes
- spam
- jokes
- low quality comments
- unrelated discussions

Write like a professional news anchor or podcast narrator. The final output should sound smooth and natural when read aloud by a text-to-speech engine.

Rules:
- No markdown
- No bullet points
- No emojis
- No special characters
- No introductory lines like "Here is the summary"
- Start directly with the actual narration

Keep the tone professional, clear, and conversational.
"""

    llm = ChatMistralAI(
        model="mistral-small-2506",
        temperature=0.3
    )

    response = llm.invoke([

        SystemMessage(content=system_prompt),

        HumanMessage(content=text)

    ])

    return response.content



# =========================
# MAIN
# =========================

if __name__ == "__main__":

    topic = input("Enter topic: ")

    reddit_data = get_reddit_data(topic)

    print("\nLATEST REDDIT POSTS\n")

    for item in reddit_data:

        print("=" * 50)

        print("TITLE:", item["title"])

        print("URL:", item["url"])

    print("\nGenerating summary...\n")

    final_output = summarize(reddit_data)

    print(final_output)