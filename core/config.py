import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TRADE_INTERVAL = "1m"  # interval for bot operation
LEVERAGE = 5
TP_PERCENT = 2.5
SL_PERCENT = 1.5
CAPITAL_USDT = 200      # Total available capital (bot decides how to split)
TOP_TRADES = 3          # Max number of trades at once
MODEL_PATH = "data/model.json"
