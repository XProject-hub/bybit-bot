# 🤖 ByBit Bot By X Project

A real-money, AI-powered trading bot for Bybit — trades automatically using machine learning and advanced features like leverage, trailing stop, and live balance tracking.

---

## 🚀 Features

- ✅ XGBoost-based AI signals (expandable to LSTM)
- ✅ Automated buy/sell using real Bybit funds
- ✅ Capital split across multiple trades
- ✅ Live USDT balance check
- ✅ Leverage control
- ✅ Trailing stop & conditional orders
- ✅ Telegram trade alerts
- ✅ Profit logging to CSV
- ✅ Flask web dashboard with charts and login

---

## 📁 Folder Structure

bybit_bot/ ├── core/ │ ├── config.py │ ├── telegram.py │ ├── ai_model.py │ ├── ai_executor.py │ ├── profit_logger.py │ ├── trading_features.py │ ├── bot/ │ └── bot_ai.py │ ├── dashboard/ │ ├── dashboard.py │ ├── templates/ │ │ ├── login.html │ │ └── dashboard.html │ └── static/ │ └── style.css │ ├── data/ │ ├── profits.csv │ ├── .env ├── .env.example ├── requirements.txt

yaml
Copy
Edit

---

## ⚙️ Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
Create .env:

env
Copy
Edit
API_KEY=your_api_key
API_SECRET=your_api_secret
TELEGRAM_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
Run bot:

bash
Copy
Edit
cd bot
python3 bot_ai.py
Run dashboard:

bash
Copy
Edit
cd dashboard
python3 dashboard.py