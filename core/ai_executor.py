from config import *
from telegram import send_telegram
from profit_logger import log_trade
from trading_features import get_balance, place_market_order
from ai_model import predict

def execute_ai_trade(exchange, symbol, features):
    prediction = predict(features)
    if prediction != 1:
        return

    try:
        # fetch real available USDT
        balance = get_balance(exchange, "USDT")
        if balance < 5:
            send_telegram(f"❌ Not enough USDT to trade: {balance}")
            return

        price = exchange.fetch_ticker(symbol)["last"]
        portion = balance / TOP_TRADES
        amount = round(portion / price, 3)

        exchange.set_leverage(LEVERAGE, symbol)
        order = place_market_order(exchange, symbol, "buy", amount, LEVERAGE)

        send_telegram(f"✅ LONG {symbol} @ {price:.2f} | Amount: {amount}")
        profit = (price * LEVERAGE * TP_PERCENT / 100) * amount
        log_trade(symbol, "long", price, price * 1.02, amount, profit, "executed")

    except Exception as e:
        send_telegram(f"❌ Error in execute_ai_trade: {e}")
