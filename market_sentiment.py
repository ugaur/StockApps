import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def fetch_recent_news(symbol: str, company_name: str) -> str:
    # This is a mock; replace with a real news API if needed
    headlines = [
        f"{company_name} reported strong quarterly results.",
        f"{company_name} enters strategic partnership in AI.",
        f"Positive investor sentiment surrounds {company_name} amid global tech rally."
    ]
    return "\n".join(headlines)

def analyze_sentiment_with_llm(news_summary: str) -> str:
    import openai
    openai.api_key = GROQ_API_KEY
    openai.api_base = "https://api.groq.com/openai/v1"

    prompt = f"""
Analyze the following headlines and summarize market sentiment in 2-3 lines. Avoid outdated data:

{news_summary}
"""

    response = openai.ChatCompletion.create(
        model="llama3-70b-8192",
        temperature=0,
        messages=[
            {"role": "system", "content": "You summarize stock news sentiment for retail users."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
