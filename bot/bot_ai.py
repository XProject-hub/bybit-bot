import ccxt
import time
from config import *
from ai_model import train_model
from ai_executor import execute_ai_trade
from telegram import send_telegram

exchange = ccxt.bybit({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True
})

send_telegram("🤖 Bot started")
train_model()

while True:
    try:
        symbols = ["BTC/USDT", "ETH/USDT"]
        for sym in symbols:
            ticker = exchange.fetch_ticker(sym)
            price = ticker["last"]
            rsi = 50  # placeholder
            ema = price  # placeholder
            features = [rsi, ema]
            execute_ai_trade(exchange, sym, features)
        time.sleep(60)
    except Exception as e:
        send_telegram(f"Error: {e}")
        time.sleep(60)
