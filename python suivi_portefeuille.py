# 🔍 Suivi personnalisé du portefeuille utilisateur

import requests

# Liste des actifs avec leur ticker EODHD
portefeuille = [
    {"nom": "Main Street Capital", "ticker": "MAIN", "type": "Action dividende", "montant_investi": 31.0, "compte": "CTO", "devise": "USD", "dividende": True, "rendement_cible": 6.0},
    {"nom": "Sanofi", "ticker": "SAN.PA", "type": "Action dividende", "montant_investi": 150.0, "compte": "CTO", "devise": "EUR", "dividende": True, "rendement_cible": 6.0},
    {"nom": "TotalEnergies", "ticker": "TTE.PA", "type": "Action dividende", "montant_investi": 150.0, "compte": "CTO", "devise": "EUR", "dividende": True, "rendement_cible": 6.0},
    {"nom": "PEA S&P 500 EUR (Acc)", "ticker": "C500.PA", "type": "ETF capitalisant", "montant_investi": 60.0, "compte": "PEA", "devise": "EUR", "dividende": False, "rendement_cible": 8.0},
    {"nom": "Artificial Intelligence USD (Acc)", "ticker": "AIAI.MI", "type": "ETF capitalisant", "montant_investi": 45.0, "compte": "CTO", "devise": "EUR", "dividende": False, "rendement_cible": 8.0},
]

API_KEY = "6840394cca4e74.25724982"

def get_stock_data(ticker):
    url = f"https://eodhd.com/api/real-time/{ticker}?api_token={API_KEY}&fmt=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur API ({response.status_code}) pour {ticker}")
            return None
    except Exception as e:
        print(f"❌ Exception API pour {ticker} :", e)
        return None

def analyse_portefeuille():
    print("📊 Analyse du portefeuille :\n")
    for actif in portefeuille:
        data = get_stock_data(actif['ticker'])
        if data:
            try:
                prix_actuel = float(data.get("close"))
                montant_investi = actif['montant_investi']
                actif['prix_actuel'] = prix_actuel
                actif['plus_value_estimee'] = round((prix_actuel - montant_investi), 2)
                print(f"✔️ {actif['nom']} - Actuel: {prix_actuel} | Investi: {montant_investi} | P/L: {actif['plus_value_estimee']} {actif['devise']}")
            except (TypeError, ValueError):
                print(f"⚠️ {actif['nom']} - Donnée indisponible ('NA')")
        else:
            print(f"⚠️ Aucune donnée pour {actif['nom']}")

# Lancer l’analyse uniquement si le script est exécuté en tant que programme principal
if __name__ == "__main__":
    analyse_portefeuille()

    print("\n🔎 Test API individuel :")
    test_data = get_stock_data("TTE.PA")  # TotalEnergies
    print(test_data)
