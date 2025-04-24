import ccxt
import time
import pandas as pd
from config import *
from ai_model import train_model, create_features
from ai_executor import execute_ai_trade
from telegram import send_telegram
from position_manager import monitor_positions
from datetime import datetime

exchange = ccxt.bybit({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True,
    "options": {
        "defaultType": "future"
    }
})

send_telegram("🚀 ByBit Bot By X Project started — ALL crypto pairs enabled")
train_model()

# 🔁 Load all tradable USDT pairs
markets = exchange.load_markets()
symbols = [s for s in markets if s.endswith("/USDT") and markets[s]["active"]]

while True:
    try:
        for symbol in symbols:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe="1m", limit=100)
                df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

                features_df = create_features(df)
                if features_df.empty:
                    continue

                latest_features = features_df.iloc[-1]
                features = [
                    latest_features["rsi"],
                    latest_features["ema"],
                    latest_features["macd"],
                    latest_features["bb_width"]
                ]

                execute_ai_trade(exchange, symbol, features)

            except Exception as inner:
                print(f"[{symbol}] Skipped: {inner}")

        monitor_positions(exchange)
        time.sleep(60)

    except Exception as e:
        send_telegram(f"❌ Bot loop error: {str(e)}")
        time.sleep(60)
