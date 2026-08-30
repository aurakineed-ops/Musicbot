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
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from SIMPLE_MUSIC import app
from config import SUPPORT_CHAT

BUTTON = [[InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT)]]
HOT = "https://graph.org/file/745ba3ff07c1270958588.mp4"
HORNY = "https://graph.org/file/eaa834a1cbfad29bd1fe4.mp4"
SEMXY = "https://graph.org/file/58da22eb737af2f8963e6.mp4"
LESBIAN = "https://graph.org/file/ff258085cf31f5385db8a.mp4"
GAY = "https://graph.org/file/850290f1f974c5421ce54.mp4"
BIGBALL = "https://i.gifer.com/8ZUg.gif"
LANGD = "https://telegra.ph/file/423414459345bf18310f5.gif"
CUTIE = "https://graph.org/file/24375c6e54609c0e4621c.mp4"


@app.on_message(filters.command("cutie"))
async def cutie(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
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

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    CUTE = f"<emoji id='5852518588686011408'>🍑</emoji> {mention} {mm}% ᴄᴜᴛᴇ ʙᴀʙʏ<emoji id='5208923808169222461'>🥀</emoji>"

    await app.send_document(
        chat_id=message.chat.id,
        document=CUTIE,
        caption=CUTE,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
    )
    
###### horny

@app.on_message(filters.command("horny"))
async def horny(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
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

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    HORNE = f"<emoji id='6086954744268460848'>🔥</emoji> {mention} ɪꜱ {mm} % ʜᴏʀɴʏ!"

    await app.send_document(
        chat_id=message.chat.id,
        document=HORNY,
        caption=HORNE,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
    )

###### HOT 

@app.on_message(filters.command("hot"))
async def hot(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
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

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    HOTIE = f"<emoji id='6086954744268460848'>🔥</emoji>{mention} ɪꜱ {mm}% ʜᴏᴛ!"

    await app.send_document(
        chat_id=message.chat.id,
        document=HOT,
        caption=HOTIE,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
    )

########## SEXY 

@app.on_message(filters.command("sexy"))
async def sexy(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
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

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    SEXO = f" <emoji id='6086954744268460848'>🔥</emoji> {mention} ɪꜱ {mm}% sexy!"
    await app.send_document (
        chat_id=message.chat.id,
        document=SEMXY,
        caption=SEXO,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
)

#########gay
@app.on_message(filters.command("gay"))
async def gay(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
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

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    GAYE = f" <emoji id='5361964771509808811'>🍷</emoji> {mention} ɪꜱ {mm}% ɢᴀʏ!"
    await app.send_document (
        chat_id=message.chat.id,
        document=GAY,
        caption=GAYE,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
)

########### LESBIAN
@app.on_message(filters.command("lesbian"))
async def lesbian(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
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

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    LEZBIAN = f" <emoji id='5283077114319347060'>💜</emoji> {mention} ɪꜱ {mm}% ʟᴇꜱʙɪᴀɴ!"
    await app.send_document (
        chat_id=message.chat.id,
        document=LESBIAN,
        caption=LEZBIAN,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
)

########### BOOBS

@app.on_message(filters.command("boob"))
async def boob(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
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

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    BALL = f" <emoji id='5415722218569089767'>🍒</emoji> {mention}ꜱ ʙᴏᴏʙꜱ ꜱɪᴢᴇ ɪᴢ {mm} ! "
    await app.send_document (
        chat_id=message.chat.id,
        document=BIGBALL,
        caption=BALL,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
)

######### COCK

@app.on_message(filters.command("cock"))
async def cock(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    elif len(message.command) > 1 and message.command[1].startswith("@"):
        target_username = message.command[1][1:]
        try:
            target_user = await app.get_users(target_username)
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

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    BAT = f" <emoji id='5847995391122869577'>🍆</emoji> {mention}  ᴄᴏᴄᴋ ꜱɪᴢᴇ ɪᴢ {mm}ᴄᴍ"
    await app.send_document (
        chat_id=message.chat.id,
        document=LANGD,
        caption=BAT,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
)