#!/bin/bash

echo "📦 Creating AI Bybit Bot project structure..."

# Root files
touch .env .env.example requirements.txt README.md

# Create folders
mkdir -p core bot dashboard/templates dashboard/static data/logs utils

# Create core files
touch core/config.py
touch core/telegram.py
touch core/profit_logger.py
touch core/ai_model.py
touch core/ai_executor.py
touch core/position_manager.py
touch core/trainer.py
touch core/strategies.py

# Create bot file
touch bot/bot_ai.py

# Create dashboard files
touch dashboard/dashboard.py
touch dashboard/templates/login.html
touch dashboard/templates/dashboard.html
touch dashboard/static/style.css

# Create data files
touch data/profits.csv
touch data/logs/train.log

# Create utils
touch utils/profit_summary.py
touch utils/get_chat_id.py

echo "✅ Done! Your project structure is ready. Now copy in your code or push to GitHub."
