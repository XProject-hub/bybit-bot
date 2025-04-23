from config import *
from telegram import send_telegram
from profit_logger import log_trade
from ai_model import predict

def execute_ai_trade(exchange, symbol, features):
    prediction = predict(features)
    if prediction == 1:
        price = exchange.fetch_ticker(symbol)["last"]
        amount = CAPITAL_USDT / price
        order = exchange.create_market_buy_order(symbol, amount)
        send_telegram(f"[BUY] {symbol} at {price}")
        profit = (price * LEVERAGE * TP_PERCENT / 100) * amount
        log_trade(symbol, "long", price, price * 1.02, amount, profit, "executed")
