import httpx
import pandas as pd
import numpy as np
from fastapi import APIRouter
import os

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

@router.get("/analyse/{symbol}")
async def analyse_stock(symbol: str):
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

    variation = ((df['close'].iloc[-1] - df['close'].iloc[-30]) / df['close'].iloc[-30]) * 100
    trend = "bullish" if df['sma_7'].iloc[-1] > df['sma_30'].iloc[-1] else "bearish"
    score = round((variation / 10 + (50 - abs(df['rsi'].iloc[-1] - 50)) / 10), 2)

    conseil = "Renforcer" if score > 7 else "Conserver" if score > 5 else "Alléger"

    return {
        "symbol": symbol.upper(),
        "variation_30d": round(variation, 2),
        "rsi": round(df['rsi'].iloc[-1], 2),
        "sma_7": round(df['sma_7'].iloc[-1], 2),
        "sma_30": round(df['sma_30'].iloc[-1], 2),
        "trend": trend,
        "score": score,
        "conseil": conseil
    }
