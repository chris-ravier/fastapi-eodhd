from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/repartition")
def calcul_repartition(capital: float, profil: str = Query(..., enum=["prudent", "equilibré", "dynamique"])):
    suggestions = {
        "prudent": [
            {"symbol": "VOO", "poids": 0.5},
            {"symbol": "CASH", "poids": 0.5}
        ],
        "equilibré": [
            {"symbol": "AAPL", "poids": 0.25},
            {"symbol": "MSFT", "poids": 0.25},
            {"symbol": "VOO", "poids": 0.3},
            {"symbol": "CASH", "poids": 0.2}
        ],
        "dynamique": [
            {"symbol": "TSLA", "poids": 0.4},
            {"symbol": "NVDA", "poids": 0.3},
            {"symbol": "QQQ", "poids": 0.3}
        ]
    }

    allocation = []
    for ligne in suggestions[profil]:
        investi = round(ligne["poids"] * capital, 2)
        allocation.append({
            "symbol": ligne["symbol"],
            "poids": ligne["poids"],
            "investi": investi
        })

    return {
        "capital": capital,
        "profil": profil,
        "allocation": allocation
    }
