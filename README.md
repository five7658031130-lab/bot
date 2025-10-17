# Advanced Telegram Voice Chat Music Bot

🎵 A powerful Telegram bot that can stream music and videos in voice chats with comprehensive owner commands.

## Features

### 🎶 Voice Chat Streaming
- Stream audio from YouTube, Spotify, SoundCloud
- Video streaming support with `/vplay` command
- High-quality audio/video playback
- Live stream support

### 🎚️ Playback Controls
- Play, pause, resume, stop
- Skip tracks
- Volume control (1-200%)
- Mute/unmute
- Seek to position
- Queue management
- Shuffle and loop

### 🔍 Search & Download
- Search music from multiple platforms
- Download songs as files
- Inline mode for quick searches
- Lyrics fetching

### 👑 Owner Commands (Hidden)
- Authentication system
- User ban/unban
- Broadcast messages
- System statistics
- Code execution
- Shell commands
- And more...

## Installation (Linux VM)

### Prerequisites
- Python 3.9 or higher
- FFmpeg
- Git

### Step 1: Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg git

# CentOS/RHEL
sudo yum install -y python3 python3-pip ffmpeg git

# Arch Linux
sudo pacman -S python python-pip ffmpeg git
```

### Step 2: Clone Repository

```bash
git clone <your-repo-url>
cd telegram-music-bot
```

### Step 3: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 4: Generate Session String

```bash
python3 session_generator.py
```

Follow the prompts to:
1. Enter your API_ID and API_HASH
2. Enter your phone number
3. Enter the verification code
4. Enter 2FA password (if enabled)

Copy the generated SESSION_STRING.

### Step 5: Configure Environment

```bash
cp .env.example .env
nano .env
```

Fill in your credentials:
```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
SESSION_STRING=your_session_string
OWNER_ID=your_user_id
OWNER_USERNAME=your_username
OWNER_PASSWORD=your_secure_password
```

### Step 6: Run the Bot

```bash
python3 bot.py
```

## Getting Credentials

### API_ID and API_HASH
1. Go to https://my.telegram.org
2. Log in with your phone number
3. Click on "API Development Tools"
4. Create a new application
5. Copy API_ID and API_HASH

### BOT_TOKEN
1. Open Telegram and search for @BotFather
2. Send `/newbot` and follow the instructions
3. Copy the bot token

### OWNER_ID
1. Open Telegram and search for @userinfobot
2. Send `/start`
3. Copy your user ID

## Usage

### Basic Commands
- `/start` - Start the bot
- `/help` - Show all commands
- `/play <song>` - Play audio in voice chat
- `/vplay <video>` - Play video in voice chat
- `/pause` - Pause playback
- `/resume` - Resume playback
- `/skip` - Skip current track
- `/end` - Stop and leave voice chat

### Owner Commands
First authenticate: `/auth <your_password>`

Then you can use:
- `/stats` - Bot statistics
- `/sysinfo` - System information
- `/broadcast <message>` - Broadcast to all users
- `/eval <code>` - Execute Python code
- `/shell <command>` - Execute shell command
- `/banuser <user_id>` - Ban a user
- `/unbanuser <user_id>` - Unban a user
- `/logout` - Logout from owner session

## Running 24/7

### Using systemd (Recommended for Linux)

Create a service file:
```bash
sudo nano /etc/systemd/system/musicbot.service
```

Add the following content:
```ini
[Unit]
Description=Telegram Music Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegram-music-bot
ExecStart=/usr/bin/python3 /path/to/telegram-music-bot/bot.py
Restart=always
RestartSec=10

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

### Using screen (Simple method)

```bash
screen -S musicbot
python3 bot.py
# Press Ctrl+A then D to detach
```

To reattach:
```bash
screen -r musicbot
```

## Troubleshooting

### PyTgCalls installation fails
Make sure you have Python 3.9+ and try:
```bash
pip3 install --upgrade pip
pip3 install py-tgcalls --no-cache-dir
```

### FFmpeg not found
Install FFmpeg using your package manager as shown in Step 1.

### Session string invalid
Regenerate your session string using `session_generator.py`.

### Bot can't join voice chat
Make sure:
1. Your SESSION_STRING is correctly set
2. The user account has permission to join the voice chat
3. Voice chat is already started in the group

## Support

For issues and questions:
- Check the logs in `logs/bot.log`
- Ensure all dependencies are installed
- Verify your .env configuration

## License

This project is for educational purposes. Make sure to comply with Telegram's Terms of Service.

## Credits

Built with:
- [Pyrogram](https://github.com/pyrogram/pyrogram)
- [PyTgCalls](https://github.com/pytgcalls/pytgcalls)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
