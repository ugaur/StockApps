import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

def get_recommendation(symbol: str, fundamentals: dict, technicals: dict, sentiment: str) -> str:
    prompt = f"""
You are a stock advisor for beginners.

Use only the following **real-time data** to recommend:
- BUY RANGE: Based on technical **Support levels**
- SELL TARGET: Based on **Resistance**
- STOP LOSS: 5–8% below the support level
- Add a one-line reasoning and one caution/risk.

📌 Stock Symbol: {symbol}

📊 Technical Indicators:
{technicals}

📉 Fundamental Snapshot:
{fundamentals}

📰 Market Sentiment:
{sentiment}

👉 Give your advice in **this format**, markdown supported:

**🟢 Recommendation**: Buy / Sell / Hold  
**✅ Buy Range**: ₹xxx – ₹xxx *(based on support)*  
**📈 Target Sell Price**: ₹xxx *(near resistance)*  
**🛑 Stop Loss**: ₹xxx  
**🧠 Why**: <1-line simple reason>  
**⚠️ Risk**: <1-line risk>

🎯 Keep it short, clear, and data-driven. No historical info or guessing.
"""

    try:
        response = openai.ChatCompletion.create(
            model="llama3-70b-8192",
            temperature=0,
            messages=[
                {"role": "system", "content": "You provide data-based, updated, beginner-friendly stock advice."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("LLM Error:", e)
        return "❌ Recommendation could not be generated."
