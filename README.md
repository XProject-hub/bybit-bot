# 🤖 AI Crypto Trading Bot with Dashboard

An autonomous AI trading bot for Bybit with full web dashboard, Telegram alerts, and profit logging.

## 🔧 Features

- AI-based signal predictions
- Automated buy/sell on Bybit
- Capital allocation logic
- Profit tracking and logging
- Real-time dashboard with charts
- Telegram alerts on trades
- Web login system

## 🧠 Technologies

- Python, Flask, CCXT, XGBoost, pandas, dotenv
- Matplotlib (for charts)
- Telegram Bot API

## 🗂 Folder Structure

core/ # Bot logic (AI, trading, config) bot/ # Main bot runner dashboard/ # Flask-based web dashboard data/ # Logs and model output utils/ # Extra tools (optional) .env # API keys

yaml
Copy
Edit

## 🚀 Quickstart

1. `pip install -r requirements.txt`
2. Create `.env` from `.env.example`
3. Run bot: `cd bot && python3 bot_ai.py`
4. Run dashboard: `cd dashboard && python3 dashboard.py`

---

**Built by X Project 💡**