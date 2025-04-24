from config import *
from telegram import send_telegram
from profit_logger import log_trade
from trading_features import get_balance, place_market_order
from ai_model import predict
from gpt_brain import gpt_reason
from position_manager import add_position
from rl_agent import RLAgent

rl = RLAgent()

def execute_ai_trade(exchange, symbol, features):
    try:
        rsi, ema, macd, bb_width = features
        action = rl.choose_action(rsi, macd, bb_width)

        if action != "BUY":
            send_telegram(f"🤖 RL skipped {symbol}: Action={action}")
            return

        balance = get_balance(exchange, "USDT")
        if balance < 5:
            send_telegram(f"💸 Not enough funds: ${balance:.2f}")
            return

        price = exchange.fetch_ticker(symbol)["last"]
        portion = balance / TOP_TRADES
        amount = round(portion / price, 3)

        exchange.set_leverage(LEVERAGE, symbol)
        place_market_order(exchange, symbol, "buy", amount, LEVERAGE)

        reason = gpt_reason(symbol, rsi, ema, macd, bb_width, "BUY")
        send_telegram(f"✅ RL TRADE {symbol} LONG @ {price:.2f} | {amount} units\n🧠 {reason}")
        profit = (price * LEVERAGE * TP_PERCENT / 100) * amount

        # Log and update RL reward
        log_trade(symbol, "long", price, price * 1.02, amount, profit, "executed", reason)
        rl.update(rsi, macd, bb_width, action, reward=profit)

        add_position(symbol, "long", price, amount, portion)

    except Exception as e:
        send_telegram(f"❌ RL Executor error: {str(e)}")
