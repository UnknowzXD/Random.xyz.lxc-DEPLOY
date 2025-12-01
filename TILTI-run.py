import discord
from discord.ext import commands
import asyncio
import subprocess
import json
from datetime import datetime
import shlex
import logging
import shutil
import os
from typing import Optional, List, Dict, Any
import threading
import time
from dotenv import load_dotenv

load_dotenv()

# ============= CONFIGURATION SECTION =============
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
BOT_NAME = "VPS HOSTS"
BOT_VERSION = "V2.0"
THUMBNAIL_IMAGE_URL = "https://i.postimg.cc/XYYnZGG5/trashed-1765164388-image-3.jpg"
FOOTER_ICON_URL = "https://i.postimg.cc/XYYnZGG5/trashed-1765164388-image-3.jpg"
MESSAGES_GIF_URL = "https://i.postimg.cc/htW4t2B7/200w-(1).webp"

DEFAULT_STORAGE_POOL = "default"

COLOR_PRIMARY = 0x00cc44
COLOR_SUCCESS = 0x00aa3a
COLOR_ERROR = 0xFFEE00
COLOR_INFO = 0x112244
COLOR_WARNING = 0x800000

CPU_THRESHOLD = 90
CHECK_INTERVAL = 60
cpu_monitor_active = True

MESSAGE_REWARD = 10
MESSAGE_THRESHOLD = 55
# ============= END CONFIGURATION =============

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('vps_bot')

if not shutil.which("lxc"):
    logger.error("LXC command not found. Please ensure LXC is installed.")
    raise SystemExit("LXC command not found. Please ensure LXC is installed.")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

MAIN_ADMIN_ID = {YOUR_USER_ID}  # Replace with your Discord ID
VPS_USER_ROLE_ID = None
protected_users = set()

PLANS = {
    "Starter": {"ram": "2GB", "cpu": "1", "storage": 10},
    "Basic": {"ram": "4GB", "cpu": "2", "storage": 30},
    "Standard": {"ram": "8GB", "cpu": "2.5", "storage": 50},
    "Pro": {"ram": "12GB", "cpu": "3.5", "storage": 80}
}

PRICES = {
    "Starter": {"Intel": 42, "AMD": 83},
    "Basic": {"Intel": 96, "AMD": 164},
    "Standard": {"Intel": 192, "AMD": 320},
    "Pro": {"Intel": 220, "AMD": 340}
}

def load_json_file(path: str, default):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning(f"{path} not found or invalid - initializing default")
        return default

user_data = load_json_file('user_data.json', {})
vps_data = load_json_file('vps_data.json', {})
admin_data = load_json_file('admin_data.json', {"admins": [str(MAIN_ADMIN_ID)]})
protected_data = load_json_file('protected_users.json', {"protected": []})
protected_users = set(protected_data.get("protected", []))

def save_data():
    try:
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f, indent=4)
        with open('vps_data.json', 'w') as f:
            json.dump(vps_data, f, indent=4)
        with open('admin_data.json', 'w') as f:
            json.dump(admin_data, f, indent=4)
        with open('protected_users.json', 'w') as f:
            json.dump({"protected": list(protected_users)}, f, indent=4)
        logger.info("Data saved")
    except Exception as e:
        logger.exception(f"Failed to save data: {e}")

def is_admin():
    async def predicate(ctx):
        user_id = str(ctx.author.id)
        if user_id == str(MAIN_ADMIN_ID) or user_id in admin_data.get("admins", []):
            return True
        await ctx.send(embed=create_error_embed("Access Denied", "You don't have permission to use this command."))
        return False
    return commands.check(predicate)

def is_main_admin():
    async def predicate(ctx):
        if str(ctx.author.id) == str(MAIN_ADMIN_ID):
            return True
        await ctx.send(embed=create_error_embed("Access Denied", "Only the main admin can use this command."))
        return False
    return commands.check(predicate)

# YOUR CREDITS IN EVERY EMBED — PERMANENT & UNREMOVABLE
def create_embed(title, description="", color=COLOR_PRIMARY, fields=None):
    embed = discord.Embed(title=f"■ {title}", description=description, color=color, timestamp=datetime.now())
    embed.set_thumbnail(url=THUMBNAIL_IMAGE_URL)
    
    if fields:
        for field in fields:
            embed.add_field(name=f"► {field['name']}", value=field['value'], inline=field.get('inline', False))
    
    embed.set_footer(
        text=f"{BOT_NAME} {BOT_VERSION} • made with ❤️ by UNKN0WN USER",
        icon_url=FOOTER_ICON_URL
    )
    return embed

def create_success_embed(title, description=""):
    return create_embed(title, description, color=COLOR_SUCCESS)

def create_error_embed(title, description=""):
    return create_embed(title, description, color=COLOR_ERROR)

def create_info_embed(title, description=""):
    return create_embed(title, description, color=COLOR_INFO)

def create_warning_embed(title, description=""):
    return create_embed(title, description, color=COLOR_WARNING)

# ... [rest of your functions: execute_lxc, cpu_monitor, etc. remain unchanged]

@bot.event
async def on_ready():
    logger.info(f"{bot.user} is now online!")
    print(f"""
╔══════════════════════════════════════════════════════════╗
║                VPS HOSTS BOT V2.0 IS LIVE                ║
║           made with ❤️ by UNKN0WN USER                   ║
╚══════════════════════════════════════════════════════════╝
    """)

# made with ❤️ by UNKN0WN USER
# Legend. Never forgotten.

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
