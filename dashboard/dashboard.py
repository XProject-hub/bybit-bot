from flask import Flask, render_template, redirect, request, session
import pandas as pd
import matplotlib.pyplot as plt
import io, base64, os, json
from datetime import datetime
import ccxt  # NEW
from utils.sparkline import get_sparkline
from utils.gpt_summary import generate_trade_summary


app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.template_filter("datetimeformat")
def datetimeformat(value):
    return datetime.fromtimestamp(float(value)).strftime('%Y-%m-%d %H:%M:%S')

@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect("/dashboard")
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "xproject2024":
            session["logged_in"] = True
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")

    chart = None
    symbol_chart = None
    total_profit = 0
    trades = []
    most_traded_list = []
    open_positions = []
    gpt_summary = generate_trade_summary()


    if os.path.exists("data/profits.csv"):
        df = pd.read_csv("data/profits.csv", names=["Time","Symbol","Side","Entry","Exit","Amount","Profit","Status","Reason"])
        df["Time"] = pd.to_datetime(df["Time"])
        total_profit = df["Profit"].sum()
        df["Date"] = df["Time"].dt.date

        profit_per_day = df.groupby("Date")["Profit"].sum()
        fig, ax = plt.subplots()
        profit_per_day.plot(kind="bar", ax=ax, color="skyblue")
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        chart = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()

        profit_per_symbol = df.groupby("Symbol")["Profit"].sum()
        top_profit_symbols = profit_per_symbol.sort_values(ascending=False).head(5)
        fig2, ax2 = plt.subplots()
        top_profit_symbols.plot(kind="bar", ax=ax2, color="limegreen")
        ax2.set_title("Top Profitable Symbols")
        buf2 = io.BytesIO()
        plt.savefig(buf2, format="png")
        buf2.seek(0)
        symbol_chart = base64.b64encode(buf2.read()).decode("utf-8")
        plt.close()

        most_traded_counts = df["Symbol"].value_counts().head(5).reset_index()
        most_traded_counts.columns = ["Symbol", "Trades"]
        most_traded_list = most_traded_counts.to_dict(orient="records")

        trades = df.sort_values("Time", ascending=False).head(10).to_dict(orient="records")

    if os.path.exists("data/open_positions.json"):
        with open("data/open_positions.json", "r") as f:
            open_positions = list(json.load(f).values())

        # Add live price and alert type
        exchange = ccxt.bybit()
        for pos in open_positions:
            try:
                symbol = pos.get("symbol")
                ticker = exchange.fetch_ticker(symbol)
                current = ticker["last"]
                pos["current"] = current
                pos["alert"] = "none"
                pos["sparkline"] = get_sparkline(symbol)

                if current >= pos["tp"] * 0.985:
                    pos["alert"] = "tp"
                elif current <= pos["trailing"] * 1.015:
                     pos["alert"] = "sl"

            except Exception:
                pos["current"] = 0
                pos["alert"] = "error"
                pos["sparkline"] = ""

    return render_template("dashboard.html",
    total_profit=round(total_profit, 2),
    chart=chart,
    symbol_chart=symbol_chart,
    trades=trades,
    most_traded=most_traded_list,
    open_positions=open_positions,
    gpt_summary=gpt_summary,
    year=datetime.now().year
)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
