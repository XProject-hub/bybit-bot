import ccxt
import time
from config import *
from ai_model import train_model
from ai_executor import execute_ai_trade
from telegram import send_telegram
from datetime import datetime

exchange = ccxt.bybit({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True,
    "options": {
        "defaultType": "future"  # if using futures
    }
})

send_telegram("🚀 ByBit Bot By X Project started.")
train_model()

while True:
    try:
        symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
        for symbol in symbols:
            ticker = exchange.fetch_ticker(symbol)
            price = ticker["last"]
            rsi = 50  # placeholder value
            ema = price  # placeholder value
            features = [rsi, ema]

            execute_ai_trade(exchange, symbol, features)

        time.sleep(60)
    except Exception as e:
        send_telegram(f"❌ Bot error: {str(e)}")
        time.sleep(60)
