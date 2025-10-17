"""
Autonomous Music Bot Configuration
Self-initializing, auto-healing, production-ready
"""

import os
import sys
import logging
from pathlib import Path
from typing import Tuple, List

# Auto-create base directory
BASE_DIR = Path(__file__).parent
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Auto-create all required directories
DOWNLOAD_DIR = BASE_DIR / "downloads"
TEMP_DIR = BASE_DIR / "temp"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"

for directory in [DOWNLOAD_DIR, TEMP_DIR, CACHE_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Telegram Configuration
API_ID = int(os.getenv("API_ID", "28807899"))
API_HASH = os.getenv("API_HASH", "f5a090037ba4cc92c3a87e4744e66003")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8039358878:AAGg38C2-wuqTGzSw8XVTVGC9sRG6gHHTO8")

# Owner Configuration
OWNER_ID = int(os.getenv("OWNER_ID", "7619316793"))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Sexuatic")
OWNER_SECRET_PASSWORD = os.getenv("OWNER_SECRET_PASSWORD", "fiVe55@@")

# Bot Settings
MAX_DOWNLOAD_SIZE_MB = 100
DEFAULT_AUDIO_QUALITY = 320
AVAILABLE_QUALITIES = [128, 192, 256, 320]

# Features
ENABLE_INLINE_MODE = True
ENABLE_VOICE_RECOGNITION = True
ENABLE_LYRICS = True
ENABLE_BROADCAST = True

# Rate Limiting
MAX_DOWNLOADS_PER_USER_PER_DAY = 50
DOWNLOAD_COOLDOWN_SECONDS = 5

# Setup Logging
LOG_FILE = LOG_DIR / "bot.log"

try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
except Exception:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

def validate_config() -> Tuple[bool, List[str]]:
    """Validate configuration"""
    errors = []
    
    if not API_ID or API_ID == 0:
        errors.append("API_ID not set")
    if not API_HASH:
        errors.append("API_HASH not set")
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN not set")
    if not OWNER_ID or OWNER_ID == 0:
        errors.append("OWNER_ID not set")
    
    return (len(errors) == 0, errors)
