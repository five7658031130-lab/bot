# Advanced Telegram Voice Chat Music Bot

## 🎵 Project Overview

**Created:** October 17, 2025  
**Owner:** @Sexuatic (User ID: 7619316793)  
**Platform:** Telegram Bot using Pyrogram + PyTgCalls  
**Deployment:** Linux VM (NOT Replit - see below)

## ⚠️ CRITICAL: This Bot Cannot Run on Replit

This bot uses **PyTgCalls** for voice chat streaming, which requires:
- Native C++ extensions (NTgCalls, WebRTC)
- System-level audio/video processing libraries
- Compiled binaries not available in Replit's environment

**You MUST deploy this to your own Linux server or VM.**

## 🎯 Project Purpose

An advanced Telegram music bot with voice chat capabilities:
- **Audio streaming** in Telegram voice chats (YouTube, Spotify, SoundCloud)
- **Video streaming** with `/vplay` command
- **Live stream** support
- **Comprehensive owner commands** (hidden, password-protected)
- **Music search and download**
- **Lyrics fetching**
- **Voice recognition** (Shazam)
- **Inline mode** for quick searches

## 🏗️ Architecture

### Core Components

1. **bot.py** - Main bot initialization with PyTgCalls
2. **config.py** - Configuration management
3. **session_generator.py** - Generate user session string
4. **plugins/** - Modular feature system:
   - `start.py` - Welcome and help commands
   - `voice_chat.py` - Voice chat streaming (play, pause, volume, etc.)
   - `owner.py` - Hidden owner commands
   - `search.py` - Music search and download
   - `lyrics.py` - Lyrics fetching

### Technology Stack

- **Language:** Python 3.11
- **Telegram Client:** Pyrogram 2.0.106
- **Voice Chat:** PyTgCalls 2.2.8
- **Download:** yt-dlp
- **Audio Processing:** FFmpeg
- **Async:** aiohttp, aiofiles

## 🔑 Required Credentials

You need to obtain and configure these in your Linux VM:

1. **API_ID** - From https://my.telegram.org
2. **API_HASH** - From https://my.telegram.org
3. **BOT_TOKEN** - From @BotFather
4. **SESSION_STRING** - Generate using `session_generator.py`
5. **OWNER_ID** - Your Telegram user ID (from @userinfobot)
6. **OWNER_USERNAME** - Your Telegram username
7. **OWNER_PASSWORD** - Choose a strong password

## 📁 Project Structure

```
/
├── bot.py                      # Main entry point
├── config.py                   # Configuration
├── session_generator.py        # Generate SESSION_STRING
├── requirements.txt            # Python dependencies
├── README.md                   # User documentation
├── DEPLOYMENT_GUIDE.md         # Step-by-step deployment guide
├── replit.md                   # This file (project memory)
│
├── plugins/                    # Bot features
│   ├── start.py               # /start, /help
│   ├── voice_chat.py          # Voice chat streaming
│   ├── owner.py               # Owner commands
│   ├── search.py              # Music search
│   └── lyrics.py              # Lyrics fetching
│
├── logs/                       # Bot logs
├── downloads/                  # Temporary downloads
├── temp/                       # Temporary files
└── cache/                      # Cache files
```

## 🚀 Deployment Instructions

**READ DEPLOYMENT_GUIDE.md for complete step-by-step instructions.**

### Quick Start (Linux VM Only)

```bash
# 1. Install dependencies
sudo apt install -y python3 python3-pip ffmpeg git

# 2. Install Python packages
pip install -r requirements.txt

# 3. Generate session string
python3 session_generator.py

# 4. Set environment variables
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
export SESSION_STRING="your_session_string"
export OWNER_ID="your_user_id"
export OWNER_USERNAME="your_username"
export OWNER_PASSWORD="your_password"

# 5. Run the bot
python3 bot.py
```

## 🎵 Features

### Voice Chat Streaming
- `/play <song>` - Play audio in voice chat
- `/vplay <video>` - Play video in voice chat
- `/pause` - Pause playback
- `/resume` - Resume playback
- `/skip` - Skip current track
- `/end` - Stop and leave voice chat
- `/volume <1-200>` - Adjust volume
- `/mute` / `/unmute` - Mute/unmute audio
- `/current` - Show current playing track

### Music Search & Download
- `/search <query>` - Search for music
- `/song <query>` - Download song as file
- `/lyrics <song>` - Get lyrics

### Owner Commands (Hidden)

After authentication with `/auth <password>`:
- `/stats` - Bot statistics
- `/sysinfo` - System information
- `/broadcast <message>` - Broadcast to all users
- `/eval <code>` - Execute Python code
- `/shell <command>` - Execute shell command
- `/banuser <user_id>` - Ban a user
- `/unbanuser <user_id>` - Unban a user
- `/logout` - Logout

## 🔒 Security Features

1. **Owner Authentication** - Password-protected owner commands
2. **User Ban System** - Block abusive users
3. **Environment-based Configuration** - No hardcoded credentials
4. **Input Validation** - All user inputs validated
5. **Rate Limiting** - Download cooldown system

## 🛠️ Development Notes

### Why Not Replit?

Replit cannot support this bot because:
- PyTgCalls requires native binaries (WebRTC, NTgCalls)
- Voice chat streaming needs system-level audio/video processing
- FFmpeg integration requires native libraries
- Compiled C++ extensions aren't available in Replit's sandbox

### Session String Requirement

Voice chat bots need **TWO** Telegram accounts:
1. **Bot account** (BOT_TOKEN) - For receiving commands
2. **User account** (SESSION_STRING) - For joining voice chats

The user account is necessary because only user accounts can join group voice chats, not bot accounts.

### Testing on Replit

The code is hosted here for:
- Development and editing
- Version control
- Code review
- Documentation

But it **must be deployed to a Linux VM** to actually run.

## 📊 Current Status

- ✅ Core bot structure complete
- ✅ Voice chat streaming handlers implemented
- ✅ Owner authentication system ready
- ✅ Music search and download functional
- ✅ Lyrics fetching implemented
- ✅ Comprehensive documentation created
- ⚠️ **Requires deployment to Linux VM to test**

## 🔄 Next Steps

1. Deploy to your Linux VM
2. Install system dependencies (FFmpeg, Python 3.9+)
3. Generate SESSION_STRING using `session_generator.py`
4. Configure environment variables
5. Run `python3 bot.py`
6. Test voice chat streaming in a group
7. Authenticate as owner with `/auth`

## 📝 Recent Changes

**October 17, 2025:**
- Created complete voice chat music bot
- Implemented PyTgCalls integration for audio/video streaming
- Added comprehensive owner commands system
- Created music search and lyrics fetching
- Built session generator for user authentication
- Wrote detailed deployment guide for Linux VM
- Set up project structure with modular plugins

## 👤 Owner Information

**Owner:** @Sexuatic  
**User ID:** 7619316793  
**Authentication:** Password-protected (`/auth` command)

## ⚠️ Important Reminders

1. **Never commit credentials** to version control
2. **Regenerate bot token and API keys** if accidentally exposed
3. **Keep SESSION_STRING private** - it provides full account access
4. **This bot needs a Linux server** - Replit cannot run it
5. **Voice chat must be started** before bot can join
6. **User account must be group member** to join voice chat

## 📚 Documentation Files

- **README.md** - Basic overview and quick start
- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions for Linux VM
- **.env.example** - Example environment configuration
- **replit.md** - This file (project documentation and memory)

---

**Last Updated:** October 17, 2025  
**Status:** ✅ Code complete, ready for Linux VM deployment  
**Version:** 1.0.0
