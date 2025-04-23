import xgboost as xgb
import pandas as pd
import pickle
import os

def train_model(symbol="BTC/USDT"):
    df = pd.DataFrame({
        "rsi": [30, 40, 50, 60, 70],
        "ema": [100, 102, 104, 106, 108],
        "target": [1, 1, 0, 0, 0]
    })
    X = df[["rsi", "ema"]]
    y = df["target"]

    model = xgb.XGBClassifier()
    model.fit(X, y)

    os.makedirs("data", exist_ok=True)
    with open("data/model.json", "wb") as f:
        pickle.dump(model, f)

def predict(features):
    with open("data/model.json", "rb") as f:
        model = pickle.load(f)
    return model.predict([features])[0]
