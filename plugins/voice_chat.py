"""
Voice Chat Streaming Handlers
Audio and Video playback in Telegram voice chats
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from py_tgcalls import PyTgCalls
from py_tgcalls.types import Update, StreamAudioEnded
from py_tgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from py_tgcalls.types.input_stream.quality import HighQualityVideo, HighQualityAudio
import asyncio
import yt_dlp
import config
from bot import calls, call_queues, active_calls
import logging

logger = logging.getLogger(__name__)

async def download_media(query: str, video: bool = False):
    """Download media using yt-dlp"""
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best' if video else 'bestaudio/best',
            'outtmpl': f'{config.TEMP_DIR}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'geo_bypass': True,
        }
        
        if not video:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': str(config.DEFAULT_AUDIO_QUALITY),
            }]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if query.startswith('http'):
                info = ydl.extract_info(query, download=True)
            else:
                info = ydl.extract_info(f"ytsearch:{query}", download=True)
                if 'entries' in info:
                    info = info['entries'][0]
            
            filename = ydl.prepare_filename(info)
            if not video:
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            return {
                'file': filename,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail'),
            }
    except Exception as e:
        logger.error(f"Download error: {e}")
        return None

@Client.on_message(filters.command(["play", "p"]) & filters.group)
async def play_audio(client: Client, message: Message):
    """Play audio in voice chat"""
    chat_id = message.chat.id
    
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("❌ **Usage:** /play [song name or link]")
        return
    
    query = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    
    status = await message.reply_text("🔍 **Searching...**")
    
    try:
        media_info = await download_media(query, video=False)
        
        if not media_info:
            await status.edit_text("❌ **Failed to download audio**")
            return
        
        await status.edit_text(f"🎵 **Playing:** {media_info['title']}")
        
        await calls.play(
            chat_id,
            AudioPiped(media_info['file'], HighQualityAudio())
        )
        
        active_calls[chat_id] = media_info
        
    except Exception as e:
        logger.error(f"Play error: {e}")
        await status.edit_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["vplay", "vp"]) & filters.group)
async def play_video(client: Client, message: Message):
    """Play video in voice chat"""
    chat_id = message.chat.id
    
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /vplay [video name or link]")
        return
    
    query = message.text.split(None, 1)[1]
    
    status = await message.reply_text("🔍 **Searching video...**")
    
    try:
        media_info = await download_media(query, video=True)
        
        if not media_info:
            await status.edit_text("❌ **Failed to download video**")
            return
        
        await status.edit_text(f"📹 **Playing video:** {media_info['title']}")
        
        await calls.play(
            chat_id,
            AudioVideoPiped(
                media_info['file'],
                HighQualityAudio(),
                HighQualityVideo()
            )
        )
        
        active_calls[chat_id] = media_info
        
    except Exception as e:
        logger.error(f"Video play error: {e}")
        await status.edit_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["pause", "ps"]) & filters.group)
async def pause_playback(client: Client, message: Message):
    """Pause playback"""
    chat_id = message.chat.id
    
    try:
        await calls.pause(chat_id)
        await message.reply_text("⏸ **Paused**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["resume", "rs"]) & filters.group)
async def resume_playback(client: Client, message: Message):
    """Resume playback"""
    chat_id = message.chat.id
    
    try:
        await calls.resume(chat_id)
        await message.reply_text("▶️ **Resumed**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["skip", "next"]) & filters.group)
async def skip_track(client: Client, message: Message):
    """Skip current track"""
    chat_id = message.chat.id
    
    try:
        await calls.change_stream(chat_id, AudioPiped(""))
        await message.reply_text("⏭ **Skipped**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["end", "stop", "leave"]) & filters.group)
async def end_playback(client: Client, message: Message):
    """Stop playback and leave voice chat"""
    chat_id = message.chat.id
    
    try:
        await calls.leave_call(chat_id)
        if chat_id in active_calls:
            del active_calls[chat_id]
        await message.reply_text("🛑 **Stopped and left voice chat**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["volume", "vol"]) & filters.group)
async def volume_control(client: Client, message: Message):
    """Control volume"""
    chat_id = message.chat.id
    
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /volume [1-200]")
        return
    
    try:
        volume = int(message.command[1])
        if not 1 <= volume <= 200:
            await message.reply_text("❌ **Volume must be between 1 and 200**")
            return
        
        await calls.change_volume_call(chat_id, volume)
        await message.reply_text(f"🔊 **Volume set to {volume}%**")
    except ValueError:
        await message.reply_text("❌ **Please provide a valid number**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["mute"]) & filters.group)
async def mute_audio(client: Client, message: Message):
    """Mute audio"""
    chat_id = message.chat.id
    
    try:
        await calls.mute_stream(chat_id)
        await message.reply_text("🔇 **Muted**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["unmute"]) & filters.group)
async def unmute_audio(client: Client, message: Message):
    """Unmute audio"""
    chat_id = message.chat.id
    
    try:
        await calls.unmute_stream(chat_id)
        await message.reply_text("🔊 **Unmuted**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@Client.on_message(filters.command(["current", "playing", "now"]) & filters.group)
async def current_track(client: Client, message: Message):
    """Show current playing track"""
    chat_id = message.chat.id
    
    if chat_id in active_calls:
        info = active_calls[chat_id]
        await message.reply_text(
            f"🎵 **Now Playing:**\n"
            f"📝 {info['title']}\n"
            f"⏱ Duration: {info['duration']}s"
        )
    else:
        await message.reply_text("❌ **Nothing is playing**")
