#!/bin/bash
# Setup script for Telegram Music Bot

echo "=================================="
echo "Telegram Music Bot Setup"
echo "=================================="
echo ""

# Create .env file from example
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

cp .env.example .env
echo "✅ Created .env file"
echo ""
echo "📝 Now you need to edit .env and fill in your credentials:"
echo ""
echo "1. API_ID and API_HASH (from https://my.telegram.org)"
echo "2. BOT_TOKEN (from @BotFather on Telegram)"
echo "3. SESSION_STRING (generate using: python3 session_generator.py)"
echo "4. OWNER_ID (your Telegram user ID)"
echo "5. OWNER_USERNAME (your Telegram username)"
echo "6. OWNER_PASSWORD (choose a secure password)"
echo ""
echo "Edit the file with: nano .env"
echo ""
echo "After filling in credentials, run: python3 bot.py"
echo ""
