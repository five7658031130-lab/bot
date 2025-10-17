"""
Lyrics Fetcher
Get song lyrics
"""

from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import logging

logger = logging.getLogger(__name__)

async def fetch_lyrics(song_name: str):
    """Fetch lyrics from API"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.lyrics.ovh/v1/{song_name}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('lyrics', None)
                return None
    except Exception as e:
        logger.error(f"Lyrics fetch error: {e}")
        return None

@Client.on_message(filters.command(["lyrics", "lyric"]))
async def get_lyrics(client: Client, message: Message):
    """Get song lyrics"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /lyrics <song name>")
        return
    
    query = message.text.split(None, 1)[1]
    status = await message.reply_text("🔍 **Searching for lyrics...**")
    
    try:
        lyrics = await fetch_lyrics(query)
        
        if lyrics:
            if len(lyrics) > 4096:
                for i in range(0, len(lyrics), 4096):
                    await message.reply_text(lyrics[i:i+4096])
                await status.delete()
            else:
                await status.edit_text(f"🎵 **Lyrics for {query}:**\n\n{lyrics}")
        else:
            await status.edit_text("❌ **Lyrics not found**")
    
    except Exception as e:
        logger.error(f"Lyrics error: {e}")
        await status.edit_text(f"❌ **Error:** {str(e)}")
