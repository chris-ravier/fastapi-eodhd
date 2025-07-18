from fastapi import APIRouter
import requests
import os

router = APIRouter(prefix="/analyse", tags=["Suivi local"])

API_KEY = os.getenv("EODHD_API_KEY")

portefeuille = [
    {"nom": "Main Street Capital", "ticker": "MAIN", "montant_investi": 31.0, "devise": "USD"},
    {"nom": "Sanofi", "ticker": "SAN.PA", "montant_investi": 150.0, "devise": "EUR"},
    {"nom": "TotalEnergies", "ticker": "TTE.PA", "montant_investi": 150.0, "devise": "EUR"},
    {"nom": "C500 PEA", "ticker": "C500.PA", "montant_investi": 60.0, "devise": "EUR"},
    {"nom": "AI ETF", "ticker": "AIAI.MI", "montant_investi": 45.0, "devise": "EUR"},
]

def get_price(ticker):
    url = f"https://eodhd.com/api/real-time/{ticker}?api_token={API_KEY}&fmt=json"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("close")
    return None

@router.get("/portefeuille-local")
async def analyse_portefeuille_local():
    analyse = []

    for actif in portefeuille:
        prix = get_price(actif["ticker"])
        if prix is None:
            analyse.append({"nom": actif["nom"], "erreur": "Donnée indisponible"})
            continue

        plus_value = round(prix - actif["montant_investi"], 2)
        analyse.append({
            "nom": actif["nom"],
            "ticker": actif["ticker"],
            "investi": actif["montant_investi"],
            "prix_actuel": prix,
            "plus_value": plus_value,
            "devise": actif["devise"]
        })

    return {"analyse": analyse}


