import yfinance as yf
from my_indicators import get_technical_signals
from my_fundamentals import get_fundamental_data
from market_sentiment import fetch_recent_news, analyze_sentiment_with_llm
from my_llm import get_recommendation

symbol_cache = {}

def analyze_stock(symbol):
    if symbol in symbol_cache:
        return symbol_cache[symbol]
    try:
        data = yf.Ticker(symbol)
        hist = data.history(period="1mo", interval="1d")

        tech_signals = get_technical_signals(hist)
        fundamentals = get_fundamental_data(data.info)

        try:
            news_summary = fetch_recent_news(symbol, data.info.get("shortName"))
            sentiment = analyze_sentiment_with_llm(news_summary)
        except Exception as e:
            sentiment = f"Sentiment unavailable: {e}"

        decision = get_recommendation(symbol, fundamentals, tech_signals, sentiment)
        latest_price = hist['Close'].iloc[-1]

        result = {
            "symbol": symbol,
            "latest_price": latest_price,
            "technical": tech_signals,
            "fundamentals": fundamentals,
            "sentiment": sentiment,
            "recommendation": decision
        }

        # ✅ Save result to cache
        symbol_cache[symbol] = result
        return result

    except Exception as e:
        return {"error": str(e)}
