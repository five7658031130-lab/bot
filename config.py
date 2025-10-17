"""
Advanced Voice Chat Music Bot Configuration
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

DOWNLOAD_DIR = BASE_DIR / "downloads"
TEMP_DIR = BASE_DIR / "temp"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"

for directory in [DOWNLOAD_DIR, TEMP_DIR, CACHE_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "")
OWNER_PASSWORD = os.getenv("OWNER_PASSWORD", "")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN", "")

MONGO_URI = os.getenv("MONGO_URI", "")

MAX_DOWNLOAD_SIZE_MB = int(os.getenv("MAX_DOWNLOAD_SIZE_MB", "100"))
DEFAULT_AUDIO_QUALITY = int(os.getenv("DEFAULT_AUDIO_QUALITY", "320"))
AUTO_LEAVE_TIMEOUT = int(os.getenv("AUTO_LEAVE_TIMEOUT", "300"))

ENABLE_LYRICS = os.getenv("ENABLE_LYRICS", "True").lower() == "true"
ENABLE_VOICE_RECOGNITION = os.getenv("ENABLE_VOICE_RECOGNITION", "True").lower() == "true"
ENABLE_INLINE_MODE = os.getenv("ENABLE_INLINE_MODE", "True").lower() == "true"

SUDO_USERS = []
BANNED_USERS = []

def validate_config():
    """Validate required configuration"""
    errors = []
    
    if not API_ID or API_ID == 0:
        errors.append("API_ID is required")
    if not API_HASH:
        errors.append("API_HASH is required")
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN is required")
    if not SESSION_STRING:
        errors.append("SESSION_STRING is required for voice chat streaming")
    if not OWNER_ID or OWNER_ID == 0:
        errors.append("OWNER_ID is required")
    if not OWNER_PASSWORD:
        errors.append("OWNER_PASSWORD is required")
    
    if errors:
        print("\n❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        print("\n💡 Please create a .env file based on .env.example")
        return False
    
    return True
