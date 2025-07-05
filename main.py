from fastapi import FastAPI
from pydantic import BaseModel
from stock_analysis import analyze_stock

app = FastAPI()

class StockRequest(BaseModel):
    symbol: str

@app.post("/analyze")
def get_analysis(req: StockRequest):
    try:
        result = analyze_stock(req.symbol)
        return result
    except Exception as e:
        return {"error": str(e)}
