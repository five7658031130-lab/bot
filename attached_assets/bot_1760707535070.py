"""
Advanced Music Bot - Autonomous + Voice Chat Streaming
Complete production-ready bot with voice chat support
"""

import asyncio
import sys
import os
from pathlib import Path

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import logging

log_file = Path(__file__).parent / "logs" / "bot.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def install_missing_packages():
    """Auto-install missing packages"""
    import subprocess
    
    packages = [
        ("pyrogram", "pyrogram==2.0.106"),
        ("TgCrypto", "TgCrypto==1.2.5"),
        ("yt_dlp", "yt-dlp==2024.8.6"),
        ("aiohttp", "aiohttp==3.9.1"),
        ("aiofiles", "aiofiles==23.2.1"),
        ("psutil", "psutil==5.9.6"),
    ]
    
    for module, package in packages:
        try:
            __import__(module)
        except ImportError:
            logger.warning(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

try:
    install_missing_packages()
except Exception as e:
    logger.error(f"Package installation failed: {e}")

try:
    from pyrogram import Client, idle
    from pyrogram.errors import (
        ApiIdInvalid, AccessTokenInvalid, AuthKeyUnregistered
    )
    from config import (
        API_ID, API_HASH, BOT_TOKEN, OWNER_ID, OWNER_USERNAME,
        validate_config, LOG_DIR, BASE_DIR
    )
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    sys.exit(1)

try:
    app = Client(
        name="AdvancedMusicBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="plugins"),
        sleep_threshold=60,
        workdir=str(BASE_DIR),
    )
except Exception as e:
    logger.error(f"Failed to initialize bot: {e}")
    sys.exit(1)

async def main():
    """Main bot function"""
    try:
        is_valid, errors = validate_config()
        
        logger.info("=" * 70)
        logger.info("Starting Advanced Music Bot with Voice Chat Support")
        logger.info("=" * 70)
        
        await app.start()
        logger.info("Bot started successfully")
        
        bot = await app.get_me()
        logger.info(f"Bot: @{bot.username} (ID: {bot.id})")
        logger.info(f"Owner: @{OWNER_USERNAME} (ID: {OWNER_ID})")
        logger.info("=" * 70)
        
        try:
            await app.send_message(
                OWNER_ID,
                f"Bot started: @{bot.username}\n"
                f"Voice chat streaming ready\n"
                f"Commands: /start, /search, /play, /help"
            )
        except:
            pass
        
        await idle()
        
    except ApiIdInvalid:
        logger.error("Invalid API credentials")
        sys.exit(1)
    except AccessTokenInvalid:
        logger.error("Invalid bot token")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        try:
            await app.stop()
        except:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
