import httpx
import pandas as pd
import numpy as np
from fastapi import APIRouter, Query
import os
from ta.trend import MACD
from ta.volatility import BollingerBands
from app.routes.ml_model import predict_score

router = APIRouter()

EODHD_API_KEY = os.getenv("EODHD_API_KEY")
BASE_URL = "https://eodhd.com/api"

def calculate_rsi(data, period: int = 14):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

async def analyse_symbol(symbol: str):
    url = f"{BASE_URL}/eod/{symbol}.US?api_token={EODHD_API_KEY}&fmt=json&order=d"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date', ascending=True).reset_index(drop=True)
    df['close'] = df['close'].astype(float)
    df['sma_7'] = df['close'].rolling(window=7).mean()
    df['sma_30'] = df['close'].rolling(window=30).mean()
    df['rsi'] = calculate_rsi(df)

    macd = MACD(df['close']).macd()
    bb = BollingerBands(df['close'])
    bb_upper = bb.bollinger_hband()
    bb_lower = bb.bollinger_lband()

    df['macd'] = macd
    df['bb_upper'] = bb_upper
    df['bb_lower'] = bb_lower

    variation = ((df['close'].iloc[-1] - df['close'].iloc[-30]) / df['close'].iloc[-30]) * 100
    trend = "bullish" if df['sma_7'].iloc[-1] > df['sma_30'].iloc[-1] else "bearish"
    volatility = df['bb_upper'].iloc[-1] - df['bb_lower'].iloc[-1]

    score_ai, prediction = predict_score(
        df['rsi'].iloc[-1],
        df['macd'].iloc[-1],
        volatility,
        variation
    )

    return {
        "symbol": symbol.upper(),
        "variation_30d": round(variation, 2),
        "rsi": round(df['rsi'].iloc[-1], 2),
        "macd": round(df['macd'].iloc[-1], 4),
        "trend": trend,
        "score_ai": score_ai,
        "prediction": prediction
    }

@router.get("/compare")
async def compare_stocks(symbols: str = Query(..., description="Liste séparée par virgules (ex: AAPL,MSFT,GOOGL)")):
    symbol_list = symbols.split(",")[:5]  # Max 5 actions
    results = []
    for symbol in symbol_list:
        try:
            result = await analyse_symbol(symbol.strip())
            if result["score_ai"] >= 6.0:  # Filtrage par score
                results.append(result)
        except Exception as e:
            results.append({"symbol": symbol.upper(), "error": str(e)})

    sorted_results = sorted(results, key=lambda x: x.get("score_ai", 0), reverse=True)
    return sorted_results
