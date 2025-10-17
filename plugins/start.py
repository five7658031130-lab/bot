"""
Start and Help Commands
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Start command handler"""
    await message.reply_text(
        f"🎵 **Welcome to Advanced Music Bot!**\n\n"
        f"I can stream music and videos in voice chats!\n\n"
        f"**Quick Commands:**\n"
        f"🎶 /play [song name] - Play audio in voice chat\n"
        f"📹 /vplay [video name] - Play video in voice chat\n"
        f"⏸ /pause - Pause playback\n"
        f"▶️ /resume - Resume playback\n"
        f"⏭ /skip - Skip current track\n"
        f"🛑 /end - Stop and leave voice chat\n\n"
        f"📋 /help - Show all commands\n"
        f"🔍 /search [query] - Search for music",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📚 Help", callback_data="help"),
             InlineKeyboardButton("ℹ️ About", callback_data="about")],
            [InlineKeyboardButton("👤 Owner", url=f"https://t.me/{config.OWNER_USERNAME}")]
        ])
    )

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Help command handler"""
    help_text = """
🎵 **Music Bot Commands**

**🎶 Playback Commands:**
/play [song name or link] - Play audio in voice chat
/vplay [video name or link] - Play video in voice chat
/pause - Pause current playback
/resume - Resume playback
/skip - Skip to next track
/end or /stop - Stop and leave voice chat

**📋 Queue Management:**
/queue - Show current queue
/clearqueue - Clear the queue
/shuffle - Shuffle the queue
/loop [on/off] - Enable/disable loop

**🎚️ Controls:**
/volume [1-200] - Adjust volume
/mute - Mute audio
/unmute - Unmute audio
/seek [seconds] - Seek to position

**🔍 Search & Info:**
/search [query] - Search for music
/lyrics [song name] - Get song lyrics
/song [query] - Download song as file

**ℹ️ Information:**
/current or /playing - Show current track
/stats - Bot statistics
/ping - Check bot latency

**Owner Only:** (Hidden commands available after authentication)
"""
    await message.reply_text(help_text)
