"""
Music Search and Download
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import config
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command(["search", "find"]))
async def search_music(client: Client, message: Message):
    """Search for music"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /search <song name>")
        return
    
    query = message.text.split(None, 1)[1]
    status = await message.reply_text("🔍 **Searching...**")
    
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{query}", download=False)
            
            if not info or 'entries' not in info:
                await status.edit_text("❌ **No results found**")
                return
            
            results_text = "🔍 **Search Results:**\n\n"
            buttons = []
            
            for i, entry in enumerate(info['entries'][:5], 1):
                title = entry.get('title', 'Unknown')
                duration = entry.get('duration', 0)
                url = entry.get('url', '')
                
                minutes, seconds = divmod(duration, 60)
                results_text += f"{i}. **{title}**\n⏱ {minutes}:{seconds:02d}\n\n"
                
                buttons.append([
                    InlineKeyboardButton(
                        f"{i}. {title[:30]}...",
                        callback_data=f"play_{entry.get('id', '')}"
                    )
                ])
            
            await status.edit_text(
                results_text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        await status.edit_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["song", "download"]))
async def download_song(client: Client, message: Message):
    """Download song as file"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /song <song name>")
        return
    
    query = message.text.split(None, 1)[1]
    status = await message.reply_text("🔍 **Searching and downloading...**")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{config.DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': str(config.DEFAULT_AUDIO_QUALITY),
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            if 'entries' in info:
                info = info['entries'][0]
            
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
            title = info.get('title', 'Unknown')
            
            await status.edit_text("📤 **Uploading...**")
            
            await message.reply_audio(
                audio=filename,
                title=title,
                caption=f"🎵 **{title}**\n\n@{(await client.get_me()).username}"
            )
            
            await status.delete()
            
            import os
            if os.path.exists(filename):
                os.remove(filename)
    
    except Exception as e:
        logger.error(f"Download error: {e}")
        await status.edit_text(f"❌ **Error:** {str(e)}")
