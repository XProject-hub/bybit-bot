import json
import os
import time
from config import *
from telegram import send_telegram
from profit_logger import log_trade
from trading_features import place_market_order

POSITIONS_FILE = "data/open_positions.json"

def load_positions():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_positions(data):
    with open(POSITIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_position(symbol, side, entry, qty, amount):
    tp = round(entry * (1 + TP_PERCENT / 100), 4)
    sl = round(entry * (1 - SL_PERCENT / 100), 4)
    positions = load_positions()
    positions[symbol] = {
        "side": side,
        "entry": entry,
        "qty": qty,
        "amount": amount,
        "tp": tp,
        "sl": sl,
        "trailing": sl,
        "timestamp": time.time()
    }
    save_positions(positions)

def monitor_positions(exchange):
    positions = load_positions()
    updated = False

    for symbol, pos in list(positions.items()):
        try:
            price = exchange.fetch_ticker(symbol)["last"]
            qty = pos["qty"]
            entry = pos["entry"]
            tp = pos["tp"]
            sl = pos["sl"]
            trailing = pos.get("trailing", sl)

            # Update trailing stop if price increases
            if price > entry and price * (1 - TRAIL_GAP / 100) > trailing:
                trailing = round(price * (1 - TRAIL_GAP / 100), 4)
                pos["trailing"] = trailing
                updated = True

            # Take Profit hit
            if price >= tp:
                place_market_order(exchange, symbol, "sell", qty, LEVERAGE)
                pnl = (tp - entry) * qty * LEVERAGE
                log_trade(symbol, "take-profit", entry, tp, qty, pnl, "TP hit")
                send_telegram(f"🎯 TP HIT: {symbol} sold @ {tp} | PnL: {pnl:.2f}")
                del positions[symbol]
                updated = True

            # Stop-Loss hit (trailing version)
            elif price <= trailing:
                place_market_order(exchange, symbol, "sell", qty, LEVERAGE)
                pnl = (price - entry) * qty * LEVERAGE
                log_trade(symbol, "stop-loss", entry, price, qty, pnl, "SL hit")
                send_telegram(f"⚠️ SL HIT: {symbol} sold @ {price} | PnL: {pnl:.2f}")
                del positions[symbol]
                updated = True

        except Exception as e:
            send_telegram(f"❌ Monitor error ({symbol}): {e}")

    if updated:
        save_positions(positions)
