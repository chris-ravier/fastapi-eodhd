import requests
from fastapi import APIRouter
import json

router = APIRouter()
EODHD_API_KEY = "6840394cca4e74.25724982"

@router.get("/stock/{symbol}")
def stock_data(symbol: str):
    url = f"https://eodhd.com/api/real-time/{symbol}?api_token={EODHD_API_KEY}&fmt=json"
    return requests.get(url).json()

@router.get("/analyse/{symbol}")
def analyse_rsi(symbol: str):
    url = f"https://eodhd.com/api/technical/{symbol}?function=rsi&api_token={EODHD_API_KEY}&fmt=json"
    return requests.get(url).json()

@router.get("/analyse/macd/{symbol}")
def analyse_macd(symbol: str):
    url = f"https://eodhd.com/api/technical/{symbol}?function=macd&api_token={EODHD_API_KEY}&fmt=json"
    return requests.get(url).json()

@router.get("/prix/{symbol}")
def prix_actuel(symbol: str):
    url = f"https://eodhd.com/api/real-time/{symbol}?api_token={EODHD_API_KEY}&fmt=json"
    return requests.get(url).json()

@router.get("/plusvalue/{symbol}/{montant}")
def plus_value(symbol: str, montant: float):
    prix_url = f"https://eodhd.com/api/real-time/{symbol}?api_token={EODHD_API_KEY}&fmt=json"
    r = requests.get(prix_url)
    if r.status_code != 200:
        return {"error": "Erreur API"}
    data = r.json()
    if "close" in data:
        plusvalue = round(float(data["close"]) - float(montant), 2)
        return {
            "ticker": symbol,
            "investi": montant,
            "cours_actuel": data["close"],
            "plusvalue": plusvalue
        }
    else:
        return {"error": "Cours non dispo"}

@router.get("/portefeuille")
def portefeuille():
    with open("portefeuille.json", encoding="utf-8") as f:
        data = json.load(f)
    return data

# ROUTE D'EXEMPLE /COMPARE
@router.get("/compare")
def compare(symbols: str):
    # symbols = "MSFT.US,AAPL.US"
    tickers = symbols.split(",")
    resultats = []
    for ticker in tickers:
        url = f"https://eodhd.com/api/real-time/{ticker}?api_token={EODHD_API_KEY}&fmt=json"
        r = requests.get(url)
        if r.status_code == 200:
            resultats.append(r.json())
    return resultats

# ROUTE D'EXEMPLE /REPARTITION
@router.get("/repartition")
def repartition(amount: float):
    # Ex de répartition cible, adapte si tu veux (ici : 60/25/10/5)
    parts = [0.6, 0.25, 0.1, 0.05]
    categories = ["ETF Monde", "Actions Dividende", "ETF Thématique", "Opportunités"]
    result = [
        {"categorie": categories[i], "allocation_eur": round(amount * parts[i], 2)}
        for i in range(len(parts))
    ]
    return result
