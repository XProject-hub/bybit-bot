import ccxt
import matplotlib.pyplot as plt
import io
import base64

def get_sparkline(symbol: str, timeframe="1m", limit=30):
    try:
        exchange = ccxt.bybit()
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        closes = [c[4] for c in ohlcv]

        fig, ax = plt.subplots(figsize=(2, 0.8))
        ax.plot(closes, linewidth=1.2, color="#3ff073")
        ax.set_axis_off()
        plt.tight_layout(pad=0)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, transparent=True)
        plt.close()
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
        return ""
