# 🚀 Deployment Guide - Telegram Voice Chat Music Bot

This bot is designed to run on a **Linux VM** (not on Replit) because it requires PyTgCalls which needs native dependencies.

## ⚠️ Important: This Bot Cannot Run on Replit

PyTgCalls requires:
- Native C++ extensions
- System-level audio/video processing
- WebRTC libraries

These are not available in Replit's environment. You MUST deploy this to your own Linux server or VM.

## 📋 Prerequisites

### System Requirements
- **Linux Server/VM** (Ubuntu 20.04+ recommended)
- Python 3.9 or higher
- 1GB+ RAM
- 10GB+ Storage
- Stable internet connection

### Required Software
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git

# CentOS/RHEL
sudo yum install -y python3 python3-pip ffmpeg git

# Arch Linux
sudo pacman -S python python-pip ffmpeg git
```

## 🔑 Getting Credentials

### 1. API_ID and API_HASH
1. Visit https://my.telegram.org
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy your `API_ID` and `API_HASH`

### 2. BOT_TOKEN
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the `BOT_TOKEN` provided

### 3. SESSION_STRING (Important!)
This bot needs a **USER account** session (not just the bot token) to join voice chats.

#### On Your Linux VM:
```bash
cd /path/to/bot
python3 session_generator.py
```

Follow the prompts:
1. Enter your `API_ID`
2. Enter your `API_HASH`
3. Enter your phone number (with country code, e.g., +1234567890)
4. Enter the verification code sent to your Telegram
5. Enter your 2FA password (if enabled)

**Copy the SESSION_STRING displayed!**

### 4. OWNER_ID
1. Open Telegram
2. Search for `@userinfobot`
3. Send `/start`
4. Copy your user ID

### 5. OWNER_USERNAME
Your Telegram username (without @)

### 6. OWNER_PASSWORD
Choose a strong password for owner authentication

## 📦 Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd telegram-music-bot

# Or download the files manually
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

The bot uses Replit's secret management system. You need to set these environment variables on your server:

```bash
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
export SESSION_STRING="your_session_string"
export OWNER_ID="your_user_id"
export OWNER_USERNAME="your_username"
export OWNER_PASSWORD="your_secure_password"
```

Or create a `.env` file (if running locally):
```bash
cp .env.example .env
nano .env
# Fill in your credentials
```

### Step 5: Test the Bot

```bash
python3 bot.py
```

If everything is configured correctly, you should see:
```
🎵 Starting Advanced Voice Chat Music Bot
✅ Bot: @YourBotUsername (ID: ...)
✅ User: @YourUsername (ID: ...)
✅ Owner: @OwnerUsername (ID: ...)
🎶 Voice chat streaming ready!
```

Press `Ctrl+C` to stop.

## 🔄 Running 24/7

### Method 1: systemd Service (Recommended)

Create a service file:
```bash
sudo nano /etc/systemd/system/musicbot.service
```

Add this content (replace paths and username):
```ini
[Unit]
Description=Telegram Voice Chat Music Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegram-music-bot
ExecStart=/path/to/telegram-music-bot/venv/bin/python3 /path/to/telegram-music-bot/bot.py
Restart=always
RestartSec=10
Environment="API_ID=your_api_id"
Environment="API_HASH=your_api_hash"
Environment="BOT_TOKEN=your_bot_token"
Environment="SESSION_STRING=your_session_string"
Environment="OWNER_ID=your_user_id"
Environment="OWNER_USERNAME=your_username"
Environment="OWNER_PASSWORD=your_password"

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable musicbot
sudo systemctl start musicbot
sudo systemctl status musicbot
```

View logs:
```bash
sudo journalctl -u musicbot -f
```

Stop the bot:
```bash
sudo systemctl stop musicbot
```

### Method 2: screen/tmux (Simple)

Using screen:
```bash
screen -S musicbot
cd /path/to/telegram-music-bot
source venv/bin/activate
python3 bot.py

# Press Ctrl+A then D to detach
# Reattach: screen -r musicbot
```

Using tmux:
```bash
tmux new -s musicbot
cd /path/to/telegram-music-bot
source venv/bin/activate
python3 bot.py

# Press Ctrl+B then D to detach
# Reattach: tmux attach -t musicbot
```

### Method 3: nohup (Background)

```bash
cd /path/to/telegram-music-bot
nohup python3 bot.py > bot.log 2>&1 &

# View logs: tail -f bot.log
# Stop: kill $(pgrep -f bot.py)
```

## 📝 Usage

### For Users

1. Add the bot to your group
2. Make the bot an admin (required for voice chat)
3. Start a voice chat in the group
4. Use commands:
   - `/play <song name>` - Play audio
   - `/vplay <video name>` - Play video
   - `/pause` - Pause
   - `/resume` - Resume
   - `/skip` - Skip
   - `/end` - Stop and leave

### For Owner (You)

1. Send `/auth <your_password>` to the bot in private
2. Once authenticated, you can use hidden commands:
   - `/stats` - Bot statistics
   - `/sysinfo` - System information
   - `/broadcast <message>` - Broadcast to all users
   - `/eval <code>` - Execute Python code
   - `/shell <command>` - Execute shell command
   - `/banuser <user_id>` - Ban a user
   - `/unbanuser <user_id>` - Unban a user
   - `/logout` - Logout

## 🔧 Troubleshooting

### Bot won't start

**Check logs:**
```bash
# If using systemd:
sudo journalctl -u musicbot -n 50

# If running directly:
tail -f logs/bot.log
```

**Common issues:**
1. **Invalid credentials** - Double-check all values in your .env or environment variables
2. **Session string invalid** - Regenerate using `session_generator.py`
3. **Missing dependencies** - Run `pip install -r requirements.txt` again

### Can't join voice chat

1. **Make sure voice chat is already started** in the group
2. **Make sure the user account** (from SESSION_STRING) is a member of the group
3. **Check that the user account has permission** to join voice chats
4. Try leaving and rejoining the group with the user account

### PyTgCalls installation fails

```bash
# Make sure you have Python 3.9+
python3 --version

# Upgrade pip
pip install --upgrade pip

# Install with no cache
pip install py-tgcalls --no-cache-dir
```

### FFmpeg not found

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

## 🔒 Security Best Practices

1. **Never share your credentials** (API_ID, API_HASH, BOT_TOKEN, SESSION_STRING)
2. **Use a strong OWNER_PASSWORD**
3. **Keep your server updated:**
   ```bash
   sudo apt update && sudo apt upgrade
   ```
4. **Use a firewall:**
   ```bash
   sudo ufw enable
   sudo ufw allow 22
   ```
5. **Regular backups** of your bot configuration

## 📊 Monitoring

### Check bot status:
```bash
sudo systemctl status musicbot
```

### View real-time logs:
```bash
sudo journalctl -u musicbot -f
```

### Check resource usage:
Use the `/sysinfo` command in Telegram after authentication

## 🆘 Getting Help

If you encounter issues:
1. Check the logs (`logs/bot.log`)
2. Verify all credentials are correct
3. Ensure all dependencies are installed
4. Make sure you're running on Linux (not Windows or Replit)
5. Check that FFmpeg is installed: `ffmpeg -version`

## ⚠️ Important Notes

- This bot **requires a Linux server/VM** - it cannot run on Replit or Windows easily
- You need **both a bot token AND a user session string**
- The user account must be a member of groups where you want to play music
- Voice chat must be **started before** the bot can join
- Make sure the bot has **admin rights** in the group

## 🔄 Updating the Bot

```bash
cd /path/to/telegram-music-bot
git pull
pip install -r requirements.txt --upgrade
sudo systemctl restart musicbot
```

---

**Enjoy your advanced Telegram music bot!** 🎵
