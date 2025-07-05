import pandas as pd
import ta

def get_technical_signals(df: pd.DataFrame) -> dict:
    signals = {}
    close = df['Close']

    # SMA
    df['SMA_20'] = close.rolling(window=20).mean()
    df['SMA_50'] = close.rolling(window=50).mean()
    signals['SMA_Crossover'] = 'Bullish' if df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1] else 'Bearish'

    # RSI
    rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi()
    signals['RSI'] = round(rsi.iloc[-1], 2)
    signals['RSI_Signal'] = 'Overbought' if rsi.iloc[-1] > 70 else 'Oversold' if rsi.iloc[-1] < 30 else 'Neutral'

    # MACD
    macd_diff = ta.trend.MACD(close=close).macd_diff().iloc[-1]
    signals['MACD_Signal'] = 'Bullish' if macd_diff > 0 else 'Bearish'

    # Support/Resistance (Basic min/max over 30 periods)
    recent = close[-30:]
    support = recent.min()
    resistance = recent.max()
    signals['Support_Level'] = round(support, 2)
    signals['Resistance_Level'] = round(resistance, 2)

    return signals
