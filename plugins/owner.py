"""
Owner Commands
Hidden commands for bot owner only
"""

from pyrogram import Client, filters
from pyrogram.types import Message
import config
from bot import authenticated_owners
import psutil
import platform
import time
from datetime import datetime

start_time = time.time()

def is_owner(_, __, message: Message):
    """Check if user is owner"""
    return message.from_user.id == config.OWNER_ID

is_owner_filter = filters.create(is_owner)

@Client.on_message(filters.command("auth") & filters.private & is_owner_filter)
async def authenticate_owner(client: Client, message: Message):
    """Authenticate as owner"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /auth <password>")
        return
    
    password = message.command[1]
    
    if password == config.OWNER_PASSWORD:
        authenticated_owners.add(message.from_user.id)
        await message.reply_text(
            "✅ **Authentication successful!**\n\n"
            "🔓 Owner commands unlocked:\n"
            "/stats - Bot statistics\n"
            "/sysinfo - System information\n"
            "/broadcast - Broadcast message\n"
            "/eval - Execute Python code\n"
            "/shell - Execute shell command\n"
            "/banuser - Ban a user\n"
            "/unbanuser - Unban a user\n"
            "/logout - Logout from owner session"
        )
        await message.delete()
    else:
        await message.reply_text("❌ **Invalid password**")
        await message.delete()

def is_authenticated(_, __, message: Message):
    """Check if owner is authenticated"""
    return message.from_user.id in authenticated_owners

is_authenticated_filter = filters.create(is_authenticated)

@Client.on_message(filters.command("logout") & filters.private & is_authenticated_filter)
async def logout_owner(client: Client, message: Message):
    """Logout from owner session"""
    authenticated_owners.discard(message.from_user.id)
    await message.reply_text("🔒 **Logged out successfully**")

@Client.on_message(filters.command("stats") & is_authenticated_filter)
async def bot_stats(client: Client, message: Message):
    """Show bot statistics"""
    uptime = time.time() - start_time
    hours, remainder = divmod(int(uptime), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    stats_text = f"""
📊 **Bot Statistics**

⏰ **Uptime:** {hours}h {minutes}m {seconds}s
💾 **RAM Usage:** {psutil.virtual_memory().percent}%
💿 **Disk Usage:** {psutil.disk_usage('/').percent}%
🖥 **CPU Usage:** {psutil.cpu_percent()}%

👥 **Users:** Coming soon
🎵 **Active Calls:** Coming soon
"""
    await message.reply_text(stats_text)

@Client.on_message(filters.command("sysinfo") & is_authenticated_filter)
async def system_info(client: Client, message: Message):
    """Show system information"""
    sys_info = f"""
🖥 **System Information**

**OS:** {platform.system()} {platform.release()}
**Architecture:** {platform.machine()}
**Python:** {platform.python_version()}

**CPU:**
Cores: {psutil.cpu_count()}
Usage: {psutil.cpu_percent()}%

**Memory:**
Total: {psutil.virtual_memory().total / (1024**3):.2f} GB
Used: {psutil.virtual_memory().used / (1024**3):.2f} GB
Free: {psutil.virtual_memory().available / (1024**3):.2f} GB

**Disk:**
Total: {psutil.disk_usage('/').total / (1024**3):.2f} GB
Used: {psutil.disk_usage('/').used / (1024**3):.2f} GB
Free: {psutil.disk_usage('/').free / (1024**3):.2f} GB
"""
    await message.reply_text(sys_info)

@Client.on_message(filters.command("broadcast") & is_authenticated_filter)
async def broadcast_message(client: Client, message: Message):
    """Broadcast message to all users"""
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("❌ **Usage:** /broadcast <message> or reply to a message")
        return
    
    broadcast_msg = message.text.split(None, 1)[1] if len(message.command) > 1 else message.reply_to_message.text
    
    status = await message.reply_text("📡 **Broadcasting...**")
    
    await status.edit_text("✅ **Broadcast feature coming soon** (requires database)")

@Client.on_message(filters.command("eval") & is_authenticated_filter & filters.private)
async def eval_code(client: Client, message: Message):
    """Execute Python code"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /eval <code>")
        return
    
    code = message.text.split(None, 1)[1]
    
    try:
        result = eval(code)
        await message.reply_text(f"```python\n{result}\n```")
    except Exception as e:
        await message.reply_text(f"❌ **Error:**\n```\n{e}\n```")

@Client.on_message(filters.command("shell") & is_authenticated_filter & filters.private)
async def shell_command(client: Client, message: Message):
    """Execute shell command"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /shell <command>")
        return
    
    command = message.text.split(None, 1)[1]
    
    try:
        import subprocess
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        await message.reply_text(f"```\n{output[:4000]}\n```")
    except Exception as e:
        await message.reply_text(f"❌ **Error:**\n```\n{e}\n```")

@Client.on_message(filters.command("banuser") & is_authenticated_filter)
async def ban_user(client: Client, message: Message):
    """Ban a user"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /banuser <user_id>")
        return
    
    try:
        user_id = int(message.command[1])
        config.BANNED_USERS.append(user_id)
        await message.reply_text(f"✅ **User {user_id} has been banned**")
    except ValueError:
        await message.reply_text("❌ **Invalid user ID**")

@Client.on_message(filters.command("unbanuser") & is_authenticated_filter)
async def unban_user(client: Client, message: Message):
    """Unban a user"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /unbanuser <user_id>")
        return
    
    try:
        user_id = int(message.command[1])
        if user_id in config.BANNED_USERS:
            config.BANNED_USERS.remove(user_id)
            await message.reply_text(f"✅ **User {user_id} has been unbanned**")
        else:
            await message.reply_text("❌ **User is not banned**")
    except ValueError:
        await message.reply_text("❌ **Invalid user ID**")

@Client.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Check bot latency"""
    start = datetime.now()
    msg = await message.reply_text("🏓 **Pong!**")
    end = datetime.now()
    latency = (end - start).total_seconds() * 1000
    await msg.edit_text(f"🏓 **Pong!**\n⚡️ **Latency:** {latency:.2f}ms")
