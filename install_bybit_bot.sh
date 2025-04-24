#!/bin/bash

echo "🚀 Starting installation of Bybit Bot by X Project..."

# 1. System Update & Dependencies
echo "🔧 Updating system and installing dependencies..."
apt update && apt install -y python3 python3-pip git

# 2. Clone the GitHub repository
echo "📥 Cloning the repository from GitHub..."
git clone https://github.com/XProject-hub/bybit-bot.git /opt/bybit-bot

cd /opt/bybit-bot

# 3. Create virtual environment (optional but good practice)
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 4. Install Python dependencies
echo "📦 Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create folders if they don't exist
echo "📁 Creating necessary folders..."
mkdir -p data
mkdir -p utils
mkdir -p bot
mkdir -p dashboard
mkdir -p static
mkdir -p templates

# 6. Permissions
chmod +x *.sh

# 7. Done
echo "✅ Installation complete."
echo "➡️ To start the dashboard: cd /opt/bybit-bot/dashboard && python3 dashboard.py"
echo "➡️ To start the bot: cd /opt/bybit-bot/bot && python3 bot_ai.py"
