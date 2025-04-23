from flask import Flask, render_template, redirect, url_for, request, session
import pandas as pd
import matplotlib.pyplot as plt
import io, base64, os
from datetime import datetime


app = Flask(__name__)
app.secret_key = "supersecretkey"

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
    total_profit = 0
    if os.path.exists("data/profits.csv"):
        df = pd.read_csv("data/profits.csv", names=["Time","Symbol","Side","Entry","Exit","Amount","Profit","Reason"])
        df["Time"] = pd.to_datetime(df["Time"])
        total_profit = df["Profit"].sum()
        df["Date"] = df["Time"].dt.date
        profit_per_day = df.groupby("Date")["Profit"].sum()
        fig, ax = plt.subplots()
        profit_per_day.plot(kind="bar", ax=ax)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        chart = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()
    return render_template("dashboard.html",
                       total_profit=round(total_profit, 2),
                       chart=chart,
                       year=datetime.now().year)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
