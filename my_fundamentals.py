def get_fundamental_data(info: dict) -> dict:
    return {
        "Company Name": info.get("longName"),
        "Sector": info.get("sector"),
        "Industry": info.get("industry"),
        "Market Cap": info.get("marketCap"),
        "PE Ratio (TTM)": info.get("trailingPE"),
        "EPS (TTM)": info.get("trailingEps"),
        "Return on Equity": info.get("returnOnEquity"),
        "Profit Margins": info.get("profitMargins"),
        "Debt to Equity": info.get("debtToEquity"),
        "Revenue Growth": info.get("revenueGrowth"),
        "52-Week High": info.get("fiftyTwoWeekHigh"),
        "52-Week Low": info.get("fiftyTwoWeekLow"),
        "Dividend Yield": info.get("dividendYield"),
    }
