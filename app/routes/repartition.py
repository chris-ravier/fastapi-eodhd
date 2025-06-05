from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/repartition")
def get_repartition(amount: float = Query(..., description="Montant à investir en euros")):
    # Répartition simple (équilibrée)
    etf = round(amount * 0.6, 2)
    dividendes = round(amount * 0.3, 2)
    cash = round(amount * 0.1, 2)

    return {
        "montant": amount,
        "répartition": {
            "ETF Monde": etf,
            "Actions à dividendes": dividendes,
            "Cash": cash
        },
        "conseil": "Bonne diversification. Pense à rééquilibrer tous les 6 mois."
    }
