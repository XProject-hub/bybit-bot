import xgboost as xgb
import pandas as pd
import pickle
import os
import ta  # Ensure 'ta' library is installed: pip install ta

MODEL_PATH = "data/model.json"

def create_features(df):
    df = df.copy()
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    df["ema"] = ta.trend.EMAIndicator(df["close"], window=14).ema_indicator()
    df["macd"] = ta.trend.MACD(df["close"]).macd_diff()
    bb = ta.volatility.BollingerBands(df["close"])
    df["bb_width"] = bb.bollinger_hband() - bb.bollinger_lband()

    df = df.dropna()
    return df[["rsi", "ema", "macd", "bb_width"]]

def train_model():
    # Simulated training set for testing (in real case: load historical OHLCV)
    df = pd.DataFrame({
        "close": [100, 102, 104, 103, 101, 99, 97, 96, 98, 100] * 10
    })

    features = create_features(df)
    features["target"] = [1, 0, 0, 1, 1] * 20  # Fake labels

    X = features[["rsi", "ema", "macd", "bb_width"]]
    y = features["target"]

    model = xgb.XGBClassifier()
    model.fit(X, y)

    os.makedirs("data", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

def predict(features):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model.predict([features])[0]
