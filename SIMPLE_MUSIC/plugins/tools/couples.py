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
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, UnidentifiedImageError
from pyrogram import errors, filters
from pyrogram.enums import ChatMembersFilter, ChatType
from pyrogram.types import Message

from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.mongo.couples_db import get_couple, save_couple


ASSETS = Path("SIMPLE_MUSIC/assets")
FALLBACK = ASSETS / "upic.png"
COUPLE_BG = ASSETS / "cppic.png"
OUT_DIR = Path("downloads")


COOLDOWN_SECONDS = 300
_last_used = {}


def today() -> str:
    return datetime.now().strftime("%d/%m/%Y")


def date_key(admins_only: bool, date: str) -> str:
    return f"{date}-admins" if admins_only else date


def tomorrow() -> str:
    return (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")


def circular(path) -> Image.Image:
    try:
        img = Image.open(path).convert("RGBA").resize((437, 437))
    except (FileNotFoundError, UnidentifiedImageError):
        img = Image.open(FALLBACK).convert("RGBA").resize((437, 437))
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + img.size, fill=255)
    img.putalpha(mask)
    return img


async def safe_get_user(uid: int):
    try:
        return await app.get_users(uid)
    except errors.PeerIdInvalid:
        return None
    except Exception:
        return None


async def safe_photo(uid: int, name: str):
    try:
        chat = await app.get_chat(uid)
        if chat.photo and chat.photo.big_file_id:
            path = await app.download_media(chat.photo.big_file_id, file_name=str(OUT_DIR / name))
            return Path(path) if path else FALLBACK
    except Exception:
        pass
    return FALLBACK


async def generate_image(chat_id: int, uid1: int, uid2: int, date: str) -> str:
    base = Image.open(COUPLE_BG).convert("RGBA")
    p1 = await safe_photo(uid1, "pfp1.png")
    p2 = await safe_photo(uid2, "pfp2.png")

    a1 = circular(p1)
    a2 = circular(p2)
    base.paste(a1, (116, 160), a1)
    base.paste(a2, (789, 160), a2)

    out_path = OUT_DIR / f"couple_{chat_id}_{date.replace('/', '-')}.png"
    base.save(out_path)

    for pf in (p1, p2):
        try:
            if pf != FALLBACK and pf.exists() and pf.parent == OUT_DIR:
                pf.unlink()
        except Exception:
            pass

    return str(out_path)


@app.on_message(filters.command("couples"))
async def couples_handler(_, message: Message):
    await _run_couple(message, admins_only=False)


@app.on_message(filters.command("couple"))
async def couple_admin_handler(_, message: Message):
    await _run_couple(message, admins_only=True)


async def _run_couple(message: Message, admins_only: bool):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("<b>ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.</b>")

    cid = message.chat.id
    key = (cid, admins_only)
    now = datetime.now()
    last = _last_used.get(key)
    if last:
        elapsed = (now - last).total_seconds()
        if elapsed < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - elapsed)
            mins, secs = divmod(remaining, 60)
            return await message.reply(
                f"<b>⏳ ᴡᴀɪᴛ {mins}ᴍ {secs}s ʙᴇғᴏʀᴇ ᴜsɪɴɢ ᴛʜɪs ᴀɢᴀɪɴ.</b>"
            )
    _last_used[key] = now

    wait = await message.reply("<emoji id='5316558987141852841'>🦋</emoji>")
    date = date_key(admins_only, today())

    record = await get_couple(cid, date)
    user1 = user2 = None
    img_path = None

    if record:
        uid1, uid2, img_path = record["c1_id"], record["c2_id"], record.get("img")
        user1 = await safe_get_user(uid1)
        user2 = await safe_get_user(uid2)

        if not (user1 and user2) or not img_path or not Path(img_path).exists():
            record = None

    if not record:
        if admins_only:
            members = [
                m.user.id async for m in app.get_chat_members(cid, filter=ChatMembersFilter.ADMINISTRATORS)
                if not m.user.is_bot
            ]
        else:
            members = [
                m.user.id async for m in app.get_chat_members(cid, limit=50)
                if not m.user.is_bot
            ]
        if len(members) < 2:
            msg = "<b>ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴀᴅᴍɪɴs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.</b>" if admins_only else "<b>ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.</b>"
            await wait.edit(msg)
            return

        tries = 0
        while tries < 5:
            uid1, uid2 = random.sample(members, 2)
            user1 = await safe_get_user(uid1)
            user2 = await safe_get_user(uid2)
            if user1 and user2:
                break
            tries += 1
        else:
            await wait.edit("<b>ᴄᴏᴜʟᴅ ɴᴏᴛ ғɪɴᴅ ᴠᴀʟɪᴅ ᴍᴇᴍʙᴇʀs.</b>")
            return

        img_path = await generate_image(cid, uid1, uid2, date)
        await save_couple(cid, date, {"c1_id": uid1, "c2_id": uid2}, img_path)

    caption = (
        "<b><emoji id='5238039443008408242'>💌</emoji> ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ! <emoji id='5364201435858744869'>💗</emoji></b>\n\n"
        f"<emoji id='5238039443008408242'>💌</emoji> <b>ᴛᴏᴅᴀʏ's ᴄᴏᴜᴘʟᴇ:</b>\n⤷ <a href='tg://openmessage?user_id={user1.id}'>{user1.first_name}</a> <emoji id='5219862119209520083'>💞</emoji> <a href='tg://openmessage?user_id={user2.id}'>{user2.first_name}</a>\n\n"
        f"<b>ɴᴇxᴛ sᴇʟᴇᴄᴛɪᴏɴ:</b> <code>{tomorrow()}</code>\n\n"
        f"<emoji id='5364201435858744869'>💗</emoji> <b>ᴛᴀɢ ʏᴏᴜʀ ᴄʀᴜsʜ — ʏᴏᴜ ᴍɪɢʜᴛ ʙᴇ ɴᴇxᴛ!</b>"
    )

    try:
        await message.reply_photo(img_path, caption=caption)
    finally:
        await wait.delete()


__mod__ = "COUPLES"
__help__ = """
<b>» /couples</b> - Get Todays Couples Of The Group In Interactive View
<b>» /couple</b> - Get Todays Couple picked from Group Admins only
"""
