# -----------------------------------------------
# 🔸 YORU MUSIC BOT Project
# 🔹 Developed & Maintained by: Yoru Music Bot ()
# 📅 Copyright © 2026 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by Yoru Music Bot
# -----------------------------------------------
import random
from pyrogram import filters
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC import *
from ... import *
import config
from ...logging import LOGGER
from SIMPLE_MUSIC import app, userbot
from SIMPLE_MUSIC.core.userbot import *
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from dotenv import load_dotenv
from SIMPLE_MUSIC.core.userbot import Userbot
from datetime import datetime

# Assuming Userbot is defined elsewhere
userbot = Userbot()


BOT_LIST = ["StrangerSuperbot", "zmnrobot", "SapnaMusicRobot", "ITZ_MERADHIKABOT", "StrangerHackBot"]

@app.on_message(filters.command("botschk") & filters.user(OWNER_ID))
async def bots_chk(_, message):
    msg = await message.reply_photo(photo="https://telegra.ph/file/4d303296e4fac9a40ea07.jpg", caption="<b>ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛs sᴛᴀᴛs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ...</b>")
    response = "<b>ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛs sᴛᴀᴛs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ</b>\n\n"
    for bot_username in BOT_LIST:
        try:
            bot = await app.get_users(bot_username)
            bot_id = bot.id
            await asyncio.sleep(0.5)
            bot_info = await app.send_message(bot_id, "/start")
            await asyncio.sleep(3)
            async for bot_message in app.get_chat_history(bot_id, limit=1):
                if bot_message.from_user.id == bot_id:
                    response += f"╭⎋ <a href='tg://user?id={bot.id}'>{bot.first_name}</a>\n╰⊚ <b>sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ <emoji id='5325547803936572038'>✨</emoji></b>\n\n"
                else:
                    response += f"╭⎋ <a href='tg://user?id={bot.id}'>{bot.first_name}</a>\n╰⊚ <b>sᴛᴀᴛᴜs: ᴏғғʟɪɴᴇ ❄</b>\n\n"
        except Exception:
            response += f"╭⎋ {bot_username}\n╰⊚ <b>sᴛᴀᴛᴜs: ᴇʀʀᴏʀ ❌</b>\n"
    
    await msg.edit_text(response)
                
