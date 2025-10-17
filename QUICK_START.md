# 🚀 Quick Start Guide

## On Your Linux VM

### Step 1: Copy the Repository

```bash
# Download or clone this repository to your Linux VM
git clone <your-repo-url>
cd telegram-music-bot
```

### Step 2: Install Dependencies

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg git

# Install Python packages
pip3 install -r requirements.txt
```

### Step 3: Create .env File

**Option A - Using the setup script:**
```bash
./setup.sh
nano .env
```

**Option B - Manual copy:**
```bash
cp .env.example .env
nano .env
```

### Step 4: Fill in Your Credentials

Edit `.env` with your credentials:

```env
# Your provided credentials:
API_ID=28807899
API_HASH=f5a090037ba4cc92c3a87e4744e66003
OWNER_ID=7619316793
OWNER_USERNAME=Sexuatic

# You need to get these:
BOT_TOKEN=get_from_botfather
SESSION_STRING=generate_using_script_below
OWNER_PASSWORD=choose_secure_password
```

### Step 5: Get BOT_TOKEN

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow the instructions
4. Copy the token and add to `.env`

### Step 6: Generate SESSION_STRING

```bash
python3 session_generator.py
```

Follow the prompts:
- Enter your API_ID: `28807899`
- Enter your API_HASH: `f5a090037ba4cc92c3a87e4744e66003`
- Enter your phone number (with country code): `+1234567890`
- Enter verification code from Telegram
- Enter 2FA password (if enabled)

Copy the SESSION_STRING to your `.env` file.

### Step 7: Run the Bot

```bash
python3 bot.py
```

### Step 8: Test the Bot

1. Add your bot to a Telegram group
2. Make it an admin
3. Start a voice chat
4. Send `/play despacito` to test

### Step 9: Authenticate as Owner

Send `/auth <your_password>` in private chat with the bot to unlock owner commands.

## ⚠️ Important Notes

- **This bot CANNOT run on Replit** - it requires PyTgCalls native dependencies
- **You MUST use a Linux VM** (Ubuntu 20.04+ recommended)
- **Voice chat must be started** before bot can join
- **Keep SESSION_STRING private** - it gives full access to your account

## 🎵 Commands

### User Commands
- `/play <song>` - Play audio
- `/vplay <video>` - Play video
- `/pause` - Pause
- `/resume` - Resume
- `/skip` - Skip
- `/end` - Stop

### Owner Commands (after `/auth`)
- `/stats` - Bot statistics
- `/sysinfo` - System info
- `/broadcast` - Broadcast message
- `/eval` - Execute code
- `/shell` - Run shell command
- `/banuser` - Ban user
- `/unbanuser` - Unban user

## 🔄 Run 24/7

```bash
# Using systemd
sudo nano /etc/systemd/system/musicbot.service
# Add service configuration (see DEPLOYMENT_GUIDE.md)
sudo systemctl enable musicbot
sudo systemctl start musicbot
```

## 📚 Full Documentation

- **README.md** - Complete overview
- **DEPLOYMENT_GUIDE.md** - Detailed deployment steps
- **replit.md** - Project architecture and notes

---

**Need Help?** Check the logs: `tail -f logs/bot.log`
