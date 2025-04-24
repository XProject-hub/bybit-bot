import os
import openai
import pandas as pd
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_trade_summary(csv_path="data/profits.csv"):
    if not os.path.exists(csv_path):
        return "No trades recorded yet."

    try:
        df = pd.read_csv(csv_path, names=["Time","Symbol","Side","Entry","Exit","Amount","Profit","Status","Reason"])
        df["Time"] = pd.to_datetime(df["Time"])
        df = df[df["Time"].dt.date == datetime.utcnow().date()]

        if df.empty:
            return "No trades executed today."

        trades_txt = df.to_string(index=False)

        prompt = f"""
You are a smart trading assistant. Based on today's trades below, give a short summary:
- Total trades
- Winning vs losing trades
- Top 2 most profitable symbols
- Anything unusual or interesting

TRADES:
{trades_txt}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=250
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ Error generating summary: {str(e)}"
