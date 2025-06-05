import httpx
from fastapi import APIRouter
import os

router = APIRouter()

EODHD_API_KEY = os.getenv("EODHD_API_KEY")
BASE_URL = "https://eodhd.com/api"

@router.get("/stock/{symbol}")
async def get_stock_data(symbol: str):
    url = f"{BASE_URL}/eod/{symbol}.US?api_token={EODHD_API_KEY}&fmt=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
