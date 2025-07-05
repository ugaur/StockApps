import streamlit as st
import requests
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import re
from fastapi import FastAPI
import uvicorn
# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="📈 Stock Advisor AI", layout="centered")

# Live stock ticker
live_tickers = [ticker + ".NS" for ticker in [
    "RELIANCE", "TCS", "INFY", "PNB", "HDFCBANK", "ICICIBANK", "HCLTECH", "SBIN",
    "BHARTIARTL", "LT", "ITC", "MARUTI", "AXISBANK", "KOTAKBANK", "ULTRACEMCO", "ADANIENT",
    "ADANIPORTS", "ASIANPAINT", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BPCL", "BRITANNIA",
    "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HINDALCO", "HINDUNILVR",
    "JSWSTEEL", "LTIM", "M&M", "NESTLEIND", "NTPC", "ONGC", "POWERGRID", "SBILIFE", "SUNPHARMA",
    "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM", "TITAN", "UPL", "WIPRO"]]
try:
    ticker_data = []
    for ticker in live_tickers:
        data = yf.Ticker(ticker).history(period="1d")
        last_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2] if len(data['Close']) > 1 else last_price
        trend_icon = "🔼" if last_price >= prev_close else "🔽"
        trend_color = "green" if last_price >= prev_close else "red"
        ticker_data.append(f"<span style='color:{trend_color};'>{ticker.replace('.NS','')} ₹{last_price:.2f} {trend_icon}</span>")
    live_ticker_str = " | ".join(ticker_data)
    st.markdown(f"""
    <marquee behavior='scroll' direction='left' style='font-size:16px; padding:4px; background-color:#e8f5e9; border-radius:5px;'>
        {live_ticker_str}
    </marquee>
    """, unsafe_allow_html=True)
except Exception as e:
    st.warning("Live ticker unavailable.")

# Title and description
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
st.markdown("<h2>📊 Smart Stock Advisor</h2>", unsafe_allow_html=True)
st.markdown("<p>Use AI to analyze NSE stocks using <b>fundamentals</b>, <b>technicals</b>, and <b>sentiment</b>.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- USER INPUT ----------
symbol = st.text_input("🔍 Enter NSE Symbol (e.g. TCS.NS)")
analyze_clicked = st.button("🚀 Analyze")

if analyze_clicked and symbol:
    selected_symbol = symbol.upper()

    with st.spinner("Analyzing stock using AI..."):
        try:
            response = requests.post("https://stockapps-t3xc.onrender.com/analyze", json={"symbol": selected_symbol})
            result = response.json()
        except Exception as e:
            st.error(f"❌ Failed to connect to backend: {e}")
            st.stop()

    if "latest_price" in result:
        st.metric("📌 Latest Price", f"₹{round(result['latest_price'], 2)}")

    if "recommendation" in result:
        st.markdown("### 📋 AI-Powered Stock Advice")

        rec_text = result["recommendation"]
        rec_html = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", rec_text)
        rec_html = re.sub(r"\*(.*?)\*", r"<i>\1</i>", rec_html)
        rec_html = re.sub(r"(🟢|✅|📈|🛑|🧠|⚠️)", r"<br><b>\1</b>", rec_html)

        st.markdown(f"""
        <div style="border:2px solid #4CAF50; border-radius:10px; padding:15px; background-color:#f0fff4; font-size:16px; line-height:1.6;">
            {rec_html}
        </div>
        """, unsafe_allow_html=True)

    if "technical" in result:
        support = result["technical"].get("Support_Level")
        resistance = result["technical"].get("Resistance_Level")

        st.markdown("### 🧱 Support & Resistance")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Support Level", f"₹{support}" if support else "N/A")
        with col2:
            st.metric("Resistance Level", f"₹{resistance}" if resistance else "N/A")

    try:
        df = yf.Ticker(selected_symbol).history(period="3mo")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
        fig.update_layout(
            title=f"{selected_symbol.upper()} Price Trend (Last 3 Months)",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            template="plotly_white"
        )
        st.markdown("### 📈 Price Trend (3 Months)")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Chart unavailable: {e}")

    if "sentiment" in result:
        st.markdown("### 📰 Market Sentiment")
        st.info(result["sentiment"])
    else:
        st.warning("⚠️ Sentiment data not found.")

    if "technical" in result:
        st.markdown("### 📊 Technical Indicators")
        tech_rows = []
        for key, value in result["technical"].items():
            if isinstance(value, (int, float)):
                trend = "📈" if value > 0 else "📉" if value < 0 else "➖"
                color = "green" if value > 0 else "red" if value < 0 else "gray"
                tech_rows.append(f"<tr><td>{key}</td><td style='color:{color};'>{value:,.2f}</td><td>{trend}</td></tr>")
            else:
                tech_rows.append(f"<tr><td>{key}</td><td>{value}</td><td>🔹</td></tr>")

        tech_html = f"""
        <table style='width:100%; border-collapse:collapse;'>
            <tr style='background-color:#e0f7fa;'>
                <th>Indicator</th><th>Value</th><th>Trend</th>
            </tr>
            {''.join(tech_rows)}
        </table>
        """
        st.markdown(tech_html, unsafe_allow_html=True)

    if "fundamentals" in result:
        st.markdown("### 📉 Company Fundamentals")
        fund_rows = []
        for key, value in result["fundamentals"].items():
            if isinstance(value, (int, float)):
                trend = "📈" if value > 0 else "📉" if value < 0 else "➖"
                color = "green" if value > 0 else "red" if value < 0 else "gray"
                fund_rows.append(f"<tr><td>{key}</td><td style='color:{color};'>{value:,.2f}</td><td>{trend}</td></tr>")
            else:
                fund_rows.append(f"<tr><td>{key}</td><td>{value}</td><td>🔹</td></tr>")

        fund_html = f"""
        <table style='width:100%; border-collapse:collapse;'>
            <tr style='background-color:#fbe9e7;'>
                <th>Metric</th><th>Value</th><th>Trend</th>
            </tr>
            {''.join(fund_rows)}
        </table>
        """
        st.markdown(fund_html, unsafe_allow_html=True)
