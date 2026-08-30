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
import asyncio
import random
import config
from typing import List
from pyrogram import Client, enums, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.utils.admin_check import is_admin

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

chatQueue: set[int] = set()
stopProcess: bool = False

async def scan_deleted_members(chat_id: int) -> List:
    return [member.user async for member in app.get_chat_members(chat_id) if member.user and member.user.is_deleted]

async def safe_edit(msg: Message, text: str):
    try:
        await msg.edit(text)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await msg.edit(text)
    except Exception:
        pass

@app.on_message(filters.command(["zombies"]))
async def prompt_zombie_cleanup(_: Client, message: Message):
    if not await is_admin(message):
        return await message.reply("👮🏻 | <b>Only admins can execute this command.</b>")

    deleted_list = await scan_deleted_members(message.chat.id)
    if not deleted_list:
        return await message.reply("⟳ | <b>No deleted accounts found in this chat.</b>")

    total = len(deleted_list)
    est_time = max(1, total // 5)

    r1, r2 = random.choices(STYLES, k=2)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Yes, Clean", callback_data=f"confirm_zombies:{message.chat.id}", **_get_style(r1)),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_zombies", **_get_style(r2)),
            ]
        ]
    )

    await message.reply(
        (
            f"<emoji id='6098337704682984714'>⚠</emoji>️ | <b>Found `{total}` deleted accounts.</b>\n"
            f"⏳ | <b>Estimated cleanup time:</b> `{est_time}s`\n\n"
            "Do you want to clean them?"
        ),
        reply_markup=keyboard,
    )

@app.on_callback_query(filters.regex(r"^confirm_zombies"))
async def execute_zombie_cleanup(_: Client, cq: CallbackQuery):
    global stopProcess
    chat_id = int(cq.data.split(":")[1])

    if not await is_admin(cq):
        return await cq.answer("👮🏻 | Only admins can confirm this action.", show_alert=True)

    if chat_id in chatQueue:
        return await cq.answer("<emoji id='6098337704682984714'>⚠</emoji>️ | Cleanup already in progress.", show_alert=True)

    bot_me = await app.get_chat_member(chat_id, "self")
    if bot_me.status != ChatMemberStatus.ADMINISTRATOR:
        return await cq.edit_message_text("➠ | <b>I need admin rights to remove deleted accounts.</b>")

    chatQueue.add(chat_id)
    deleted_list = await scan_deleted_members(chat_id)
    total = len(deleted_list)

    status = await cq.edit_message_text(
        f"<emoji id='5433825729060018456'>🧭</emoji> | <b>Found `{total}` deleted accounts.</b>\n<emoji id='5208923808169222461'>🥀</emoji> | <b>Starting cleanup...</b>"
    )

    removed = 0

    async def ban_member(user_id):
        try:
            await app.ban_chat_member(chat_id, user_id)
            return True
        except FloodWait as e:
            await asyncio.sleep(e.value)
            return await ban_member(user_id)
        except Exception:
            return False

    tasks = []
    for user in deleted_list:
        if stopProcess:
            break
        tasks.append(ban_member(user.id))

    batch_size = 20
    for i in range(0, len(tasks), batch_size):
        results = await asyncio.gather(*tasks[i:i + batch_size], return_exceptions=True)
        removed += sum(1 for r in results if r is True)
        await safe_edit(status, f"<emoji id='5803057229909202251'>♻</emoji>️ | <b>Removed {removed}/{total} deleted accounts...</b>")
        await asyncio.sleep(2)

    chatQueue.discard(chat_id)
    await safe_edit(status, f"<emoji id='6082375377123023700'>✅</emoji> | <b>Successfully removed `{removed}` out of `{total}` zombies.</b>")

@app.on_callback_query(filters.regex(r"^cancel_zombies$"))
async def cancel_zombie_cleanup(_: Client, cq: CallbackQuery):
    await cq.edit_message_text("❌ | <b>Cleanup cancelled.</b>")

@app.on_message(filters.command(["admins", "staff"]))
async def list_admins(_: Client, message: Message):
    try:
        owners, admins = [], []
        async for m in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if m.privileges.is_anonymous or m.user.is_bot:
                continue
            (owners if m.status == ChatMemberStatus.OWNER else admins).append(m.user)

        txt = f"<b>Group Staff – {message.chat.title}</b>\n\n"
        owner_line = owners[0].mention if owners else "__Hidden__"
        txt += f"<emoji id='5217822164362739968'>👑</emoji> Owner\n└ {owner_line}\n\n👮🏻 Admins\n"

        if not admins:
            txt += "└ <i>No visible admins</i>"
        else:
            for i, adm in enumerate(admins):
                branch = "└" if i == len(admins) - 1 else "├"
                txt += f"{branch} {'@'+adm.username if adm.username else adm.mention}\n"
        txt += f"\n<emoji id='6082375377123023700'>✅</emoji> | <b>Total Admins</b>: {len(owners) + len(admins)}"
        await app.send_message(message.chat.id, txt)
    except FloodWait as e:
        await asyncio.sleep(e.value)

@app.on_message(filters.command("bots"))
async def list_bots(_: Client, message: Message):
    try:
        bots = [b.user async for b in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS)]
        txt = f"<b>Bot List – {message.chat.title}</b>\n\n<emoji id='5309832892262654231'>🤖</emoji> Bots\n"
        for i, bt in enumerate(bots):
            branch = "└" if i == len(bots) - 1 else "├"
            txt += f"{branch} @{bt.username}\n"
        txt += f"\n<emoji id='6082375377123023700'>✅</emoji> | <b>Total Bots</b>: {len(bots)}"
        await app.send_message(message.chat.id, txt)
    except FloodWait as e:
        await asyncio.sleep(e.value)
