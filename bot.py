"""
Advanced Voice Chat Music Bot
Supports audio/video streaming in Telegram voice chats
"""

import asyncio
import sys
import logging
from pathlib import Path

Path('logs').mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

try:
    from pyrogram import Client, idle
    from pyrogram.errors import ApiIdInvalid, AccessTokenInvalid
    from pytgcalls import PyTgCalls
    import config
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    logger.critical("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)

if not config.validate_config():
    logger.critical("Configuration validation failed. Please check your .env file.")
    sys.exit(1)

bot = Client(
    name="MusicBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins"),
    sleep_threshold=60,
    workdir=str(config.BASE_DIR),
)

user = Client(
    name="UserSession",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING,
    sleep_threshold=60,
    workdir=str(config.BASE_DIR),
)

calls = PyTgCalls(user)

active_calls = {}
call_queues = {}
authenticated_owners = set()

async def main():
    """Main bot function"""
    try:
        logger.info("="*70)
        logger.info("🎵 Starting Advanced Voice Chat Music Bot")
        logger.info("="*70)
        
        await bot.start()
        await user.start()
        await calls.start()
        
        bot_info = await bot.get_me()
        user_info = await user.get_me()
        
        logger.info(f"✅ Bot: @{bot_info.username} (ID: {bot_info.id})")
        logger.info(f"✅ User: @{user_info.username} (ID: {user_info.id})")
        logger.info(f"✅ Owner: @{config.OWNER_USERNAME} (ID: {config.OWNER_ID})")
        logger.info("="*70)
        logger.info("🎶 Voice chat streaming ready!")
        logger.info("="*70)
        
        try:
            await bot.send_message(
                config.OWNER_ID,
                f"🎵 **Voice Chat Music Bot Started**\n\n"
                f"🤖 Bot: @{bot_info.username}\n"
                f"👤 Assistant: @{user_info.username}\n\n"
                f"✅ All systems operational\n"
                f"🎶 Voice chat streaming enabled\n\n"
                f"Use /help for commands"
            )
        except Exception as e:
            logger.warning(f"Could not send startup message to owner: {e}")
        
        await idle()
        
    except ApiIdInvalid:
        logger.error("❌ Invalid API credentials")
        sys.exit(1)
    except AccessTokenInvalid:
        logger.error("❌ Invalid bot token or session string")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
    finally:
        try:
            await calls.stop()
            await user.stop()
            await bot.stop()
        except:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
