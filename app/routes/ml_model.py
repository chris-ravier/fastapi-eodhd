import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Exemple très simplifié : modèle IA entraîné à la volée
# À remplacer par un vrai entraînement sur données réelles

def get_model():
    # Données simulées : RSI, MACD, Volatilité, Variation 30j
    X_train = np.array([
        [45, 0.2, 2.5, 3.1],
        [70, 0.6, 1.2, 10.4],
        [30, -0.3, 4.1, -5.8],
        [55, 0.1, 3.0, 0.4],
        [80, 1.0, 0.8, 14.2],
        [25, -0.4, 5.2, -10.1]
    ])
    y_train = [1, 1, 0, 1, 1, 0]  # 1 = Acheter / 0 = Éviter

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    return model

model = get_model()

def predict_score(rsi, macd, volatility, variation):
    X = np.array([[rsi, macd, volatility, variation]])
    proba = model.predict_proba(X)[0][1]
    prediction = "Acheter" if proba > 0.6 else "Conserver" if proba > 0.4 else "Éviter"
    return round(proba * 10, 2), prediction
