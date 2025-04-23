from config import *
from telegram import send_telegram
from profit_logger import log_trade
from trading_features import get_balance, place_market_order
from ai_model import predict
from gpt_brain import gpt_decide

def execute_ai_trade(exchange, symbol, features):
    try:
        # Local AI prediction (XGBoost)
        ai_signal = predict(features)  # 1 = BUY, 0 = HOLD
        ai_action = "BUY" if ai_signal == 1 else "HOLD"

        # GPT override or confirmation
        rsi, ema = features
        gpt_action = gpt_decide(symbol, rsi, ema, ai_action)

        if ai_action != "BUY" or gpt_action != "BUY":
            send_telegram(f"🤖 Skipped {symbol}: AI={ai_action}, GPT={gpt_action}")
            return

        balance = get_balance(exchange, "USDT")
        if balance < 5:
            send_telegram(f"💸 Not enough funds: ${balance}")
            return

        price = exchange.fetch_ticker(symbol)["last"]
        portion = balance / TOP_TRADES
        amount = round(portion / price, 3)

        exchange.set_leverage(LEVERAGE, symbol)
        order = place_market_order(exchange, symbol, "buy", amount, LEVERAGE)

        send_telegram(f"✅ [TRADE] {symbol} LONG @ {price:.2f} | Qty: {amount}\nAI: {ai_action} | GPT: {gpt_action}")
        profit = (price * LEVERAGE * TP_PERCENT / 100) * amount
        log_trade(symbol, "long", price, price * 1.02, amount, profit, "executed")

    except Exception as e:
        send_telegram(f"❌ AI Executor error: {str(e)}")
