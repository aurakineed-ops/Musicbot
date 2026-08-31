# -----------------------------------------------
# 🔸 AALIYA MUSIC BOT Project
# 🔹 Developed & Maintained by: Aaliya Music Bot ()
# 📅 Copyright © 2026 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by Aaliya Music Bot
# -----------------------------------------------
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import config
import requests
from SIMPLE_MUSIC import app 


@app.on_message(filters.command("wish"))
async def wish(_, m):
    if len(m.command) < 2:
        await m.reply("ᴀᴅᴅ ᴡɪꜱʜ ʙᴀʙʏ<emoji id='5208923808169222461'>🥀</emoji>!")
        return 

    api = requests.get("https://nekos.best/api/v2/happy").json()
    url = api["results"][0]['url']
    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)
    wish = f"<emoji id='5325547803936572038'>✨</emoji> ʜᴇʏ! {m.from_user.first_name}! "
    wish += f"<emoji id='5325547803936572038'>✨</emoji> ʏᴏᴜʀ ᴡɪꜱʜ: {text} "
    wish += f"<emoji id='5325547803936572038'>✨</emoji> ᴘᴏꜱꜱɪʙʟᴇ ᴛᴏ: {wish_count}%"
    
    await app.send_animation(
        chat_id=m.chat.id,
        animation=url,
        caption=wish,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT)]])
    )
            
    
BUTTON = [[InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT)]]
CUTIE = "https://64.media.tumblr.com/d701f53eb5681e87a957a547980371d2/tumblr_nbjmdrQyje1qa94xto1_500.gif"

@app.on_message(filters.command("cute"))
async def cute(_, message):
    if message.reply_to_message:
        if message.reply_to_message.from_user:
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.first_name
        else:
            try:
                replied = await app.get_messages(message.chat.id, message.reply_to_message.id)
                user_id = replied.from_user.id
                user_name = replied.from_user.first_name
            except Exception:
                return await message.reply("<emoji id='5472267631979405211'>🚫</emoji> ᴄᴏᴜʟᴅɴ'ᴛ ᴅᴇᴛᴇᴄᴛ ᴛʜᴀᴛ ᴜꜱᴇʀ, ᴛʀʏ ᴀɢᴀɪɴ!")
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
            if not target_user.username or target_user.username.lower() != target_username.lower():
                return await message.reply("<emoji id='5472267631979405211'>🚫</emoji> ᴄᴏᴜʟᴅɴ'ᴛ ᴠᴇʀɪғʏ ᴛʜᴀᴛ ᴜꜱᴇʀ, ᴛʀʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴇɪʀ ᴍᴇꜱꜱᴀɢᴇ ɪɴꜱᴛᴇᴀᴅ!")
            user_id = target_user.id
            user_name = target_user.first_name
        except Exception:
            return await message.reply("<emoji id='5472267631979405211'>🚫</emoji> ᴄᴏᴜʟᴅɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ!")
    elif message.entities:
        target_id = None
        target_name = None
        for entity in message.entities:
            if entity.type.name == "TEXT_MENTION":
                target_id = entity.user.id
                target_name = entity.user.first_name
                break
        if target_id:
            user_id = target_id
            user_name = target_name
        else:
            user_id = message.from_user.id
            user_name = message.from_user.first_name
    else:
        user_id = message.from_user.id
        user_name = message.from_user.first_name

    mention = f"<a href='tg://openmessage?user_id={user_id}'>{user_name}</a>"
    mm = random.randint(1, 100)
    CUTE = f"<emoji id='5852518588686011408'>🍑</emoji> {mention} {mm}% ᴄᴜᴛᴇ ʙᴀʙʏ<emoji id='5208923808169222461'>🥀</emoji>"

    try:
        await app.send_document(
            chat_id=message.chat.id,
            document=CUTIE,
            caption=CUTE,
            reply_markup=InlineKeyboardMarkup(BUTTON),
        )
    except Exception:
        await message.reply(
            CUTE,
            reply_markup=InlineKeyboardMarkup(BUTTON),
        )
