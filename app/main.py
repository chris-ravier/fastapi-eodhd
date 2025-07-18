from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Allocation(BaseModel):
    asset: str
    pourcentage: float
    montant: float

class RepartitionResult(BaseModel):
    profil: str
    capital: float
    allocations: List[Allocation]

@router.get("/repartition", response_model=RepartitionResult)
def calcul_repartition(
    capital: float = Query(..., description="Capital à investir"),
    profil: str = Query(..., description="Profil investisseur: prudent, équilibré, dynamique")
):
    profils = {
        "prudent": [("Obligations", 0.7), ("ETF Monde", 0.2), ("Actions dividende", 0.1)],
        "équilibré": [("Obligations", 0.4), ("ETF Monde", 0.4), ("Actions dividende", 0.2)],
        "dynamique": [("Obligations", 0.1), ("ETF Monde", 0.4), ("Actions dividende", 0.5)]
    }

    if profil not in profils:
        raise ValueError(f"Profil inconnu: {profil}")

    structure = profils[profil]
    allocations = [
        Allocation(asset=nom, pourcentage=pct, montant=round(pct * capital, 2))
        for nom, pct in structure
    ]

    return RepartitionResult(profil=profil, capital=capital, allocations=allocations)


