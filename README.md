# 🤖 ByBit Bot By X Project

An autonomous, real-money crypto trading bot powered by **dual AI engines**:
- 🧠 XGBoost (technical prediction)
- 💡 GPT (smart override, reasoning)

Built with ❤️ by X Project.

---

## 🚀 Features

- ✅ Machine learning signal generation (XGBoost)
- ✅ GPT-4 trading override & logic explanation
- ✅ Real funds trading (mainnet Bybit)
- ✅ Balance-aware capital allocation
- ✅ Leverage support + market orders
- ✅ Telegram trade alerts
- ✅ Profit tracking and charting
- ✅ Flask web dashboard (login + graphs)
- ✅ Modular code & .env config

---

## 🧠 How the Dual AI Works

1. XGBoost predicts: *BUY* / *HOLD*
2. GPT receives data + AI suggestion
3. GPT confirms or overrides the action
4. If both agree on *BUY* → place the trade

Example:
> "AI said BUY, GPT agrees — executing order on BTC/USDT"

---

## 📁 Folder Structure

bybit_bot/ ├── core/ # AI, logic, config │ ├── config.py │ ├── ai_model.py │ ├── ai_executor.py │ ├── gpt_brain.py │ ├── profit_logger.py │ ├── telegram.py │ └── trading_features.py │ ├── bot/ # Main runner │ └── bot_ai.py │ ├── dashboard/ # Flask web app │ ├── dashboard.py │ ├── templates/ │ └── static/ │ ├── data/ # Logs │ └── profits.csv │ ├── .env # Secrets (not committed) ├── .env.example ├── requirements.txt

yaml
Copy
Edit

---

## ⚙️ Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
Create .env from .env.example and insert:

Bybit API Key

Telegram Bot Token + Chat ID

OpenAI API Key

Run bot:

bash
Copy
Edit
cd bot
python3 bot_ai.py
Start dashboard:

bash
Copy
Edit
cd dashboard
python3 dashboard.py
💬 Live Dashboard
URL: http://your-vps-ip:5000

Login: admin / xproject2024

View: Profit charts, daily logs, footer:

pgsql
Copy
Edit
© 2025 @ Developed by X Project | Version 1.0.1