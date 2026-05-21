from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

def generate_broadcast(news_data , reddit_data , topics):
    system_prompt = """
    You are broadcast_news_writer, a professional virtual news reporter. Generate natural, TTS-ready news reports using available sources:

    For each topic, STRUCTURE BASED ON AVAILABLE DATA:
    1. If news exists: "According to official reports..." + summary
    2. If Reddit exists: "Online discussions on Reddit reveal..." + summary
    3. If both exist: Present news first, then Reddit reactions
    4. If neither exists: Skip the topic (shouldn't happen)

    Formatting rules:
    - ALWAYS start directly with the content, NO INTRODUCTIONS
    - Keep audio length 60-120 seconds per topic
    - Use natural speech transitions like "Meanwhile, online discussions..." 
    - Incorporate 1-2 short quotes from Reddit when available
    - Maintain neutral tone but highlight key sentiments
    - End with "To wrap up this segment..." summary

    Write in full paragraphs optimized for speech synthesis. Avoid markdown.
    """

    try:
        topic_blocks = []
        for topic in topics:
            news_content = news_data['news_analysis'].get(topic) if news_data else ''
            reddit_content = reddit_data['reddit_analysis'].get(topic) if reddit_data else ''
            context = []
            if news_content:
                context.append(f'Offical News Content ----- \n{news_content}')
            if reddit_content:
                context.append(f'Reddit discussion Content ----- \n{reddit_content}')
            
            if context:
                topic_blocks.append(
                    f"Topic : {topic}\n\n" + "\n\n".join(context)
                )
        
        user_prompt = (
            "Create Broadcast segments for this topics using availale resources:\n\n" + 
            "\n\n ---- New Topic ----- \n\n".join(topic_blocks)
        )

        llm = ChatMistralAI(
            model = 'mistral-small-2506',
            temperature=0.3,
            max_tokens=4000
        )

        response = llm.invoke([
            SystemMessage(content = system_prompt),
            HumanMessage(content=user_prompt)
        ])

        return response.content 
    
    except Exception as e:
        raise e 