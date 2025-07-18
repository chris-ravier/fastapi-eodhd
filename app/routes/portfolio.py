import os
import json
from fastapi import APIRouter, HTTPException, Request
from dotenv import load_dotenv

# Dans portfolio.py
from fastapi import APIRouter, HTTPException
import json

router = APIRouter()
PORTEFEUILLE_PATH = "chemin/vers/portefeuille.json"

@router.post("/portfolio/add")
def add_position(position: dict):
    with open(PORTEFEUILLE_PATH, "r") as f:
        portefeuille = json.load(f)
    portefeuille["positions"].append(position)
    with open(PORTEFEUILLE_PATH, "w") as f:
        json.dump(portefeuille, f, indent=2)
    return {"success": True, "message": "Ajouté !"}

router = APIRouter()
load_dotenv()
PORTFOLIO_PATH = "portefeuille.json"

def charger_portefeuille():
    with open(PORTFOLIO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_portefeuille(data):
    with open(PORTFOLIO_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@router.get("/analyse/portefeuille")
async def analyse_portefeuille():
    portefeuille = charger_portefeuille()
    total = sum(l.get("montant_investi", 0) for l in portefeuille)
    return {"nb_lignes": len(portefeuille), "montant_total": total, "lignes": portefeuille}

@router.post("/portefeuille/ajouter")
async def ajouter_ligne(request: Request):
    new_line = await request.json()
    portefeuille = charger_portefeuille()
    # Check si le titre existe déjà (par ticker)
    if any(l["ticker"] == new_line["ticker"] for l in portefeuille):
        raise HTTPException(status_code=400, detail="Titre déjà présent dans le portefeuille.")
    portefeuille.append(new_line)
    sauvegarder_portefeuille(portefeuille)
    return {"ok": True, "message": "Titre ajouté avec succès.", "nouveau_portefeuille": portefeuille}
