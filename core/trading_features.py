from config import *
import time

def get_balance(exchange, asset="USDT"):
    balance = exchange.fetch_balance()
    return balance.get(asset, {}).get("free", 0)

def place_market_order(exchange, symbol, side, amount, leverage=1):
    exchange.set_leverage(leverage, symbol)
    if side == "buy":
        return exchange.create_market_buy_order(symbol, amount)
    elif side == "sell":
        return exchange.create_market_sell_order(symbol, amount)

def place_conditional_order(exchange, symbol, side, amount, stop_price, tp_price=None, sl_price=None):
    params = {
        "triggerDirection": 1 if side == "buy" else 2,
        "stopPrice": stop_price,
        "reduceOnly": False,
        "timeInForce": "GoodTillCancel",
        "positionIdx": 0
    }
    if tp_price:
        params["takeProfit"] = tp_price
    if sl_price:
        params["stopLoss"] = sl_price

    return exchange.create_order(
        symbol=symbol,
        type="market",
        side=side,
        amount=amount,
        price=None,
        params=params
    )

def place_trailing_stop(exchange, symbol, side, amount, trailing_percent):
    last_price = exchange.fetch_ticker(symbol)["last"]
    trailing_offset = last_price * trailing_percent / 100
    trigger_price = last_price + trailing_offset if side == "sell" else last_price - trailing_offset

    params = {
        "triggerPrice": trigger_price,
        "trailingStop": True,
        "trailingPercent": trailing_percent
    }

    return exchange.create_order(symbol, 'market', side, amount, None, params)
