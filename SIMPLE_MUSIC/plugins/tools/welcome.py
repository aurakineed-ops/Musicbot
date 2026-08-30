# -----------------------------------------------
# 🔸 AALIYA MUSIC BOT Project
# 🔹 Developed & Maintained by: Aaliya Music Bot ()
# 📅 Copyright © 2026 – All Rights Reserved
#
# ❤️ Made with dedication and love by Aaliya Music Bot
# -----------------------------------------------
import html
from datetime import datetime
from logging import getLogger

from pyrogram import enums, filters
from pyrogram.enums import ParseMode
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Message

from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.utils.database import (
    add_served_chat,
    clear_welcome_message,
    get_assistant,
    get_welcome_message,
    is_active_chat,
    is_welcome_enabled,
    set_welcome_enabled,
    set_welcome_message,
)

LOGGER = getLogger(__name__)

WELCOME_VIDEO_URL = "https://files.catbox.moe/9iom66.mp4"
WELCOME_USAGE = "<b>ᴜsᴀɢᴇ:</b>\n<b>⦿ /wel [on|off]</b>"
SET_USAGE = (
    "<b>Reply to a text, photo, or video with `/set welcome` to save it.</b>\n\n"
    "Supported placeholders: `{ID}`, `{NAME}`, `{SURNAME}`, `{NAMESURNAME}`, `{LANG}`, "
    "`{DATE}`, `{TIME}`, `{WEEKDAY}`, `{MENTION}`, `{USERNAME}`, `{GROUPNAME}`, `{RULES}`"
)


def _is_admin(member):
    return member.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    )


def _welcome_markup():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="✙ ᴋɪᴅɴᴀᴘ ᴍᴇ ✙", url=f"https://t.me/{app.username}?startgroup=true")]]
    )


async def _render_template(template: str, user, chat_id: int) -> str:
    try:
        chat = await app.get_chat(chat_id)
        group_name = chat.title or ""
        rules = getattr(chat, "description", None) or "Not set"
    except Exception:
        group_name = ""
        rules = "Not set"

    first_name = user.first_name or ""
    last_name = user.last_name or ""
    username = f"@{user.username}" if user.username else ""
    namesurname = " ".join(part for part in (first_name, last_name) if part).strip()
    now = datetime.now()
    values = {
        "{ID}": str(user.id),
        "{NAME}": first_name,
        "{SURNAME}": last_name,
        "{NAMESURNAME}": namesurname,
        "{LANG}": getattr(user, "language_code", None) or "Unknown",
        "{DATE}": now.strftime("%d-%m-%Y"),
        "{TIME}": now.strftime("%H:%M"),
        "{WEEKDAY}": now.strftime("%A"),
        "{MENTION}": user.mention,
        "{USERNAME}": username,
        "{GROUPNAME}": group_name,
        "{RULES}": rules,
    }
    rendered = template
    for placeholder, value in values.items():
        safe_value = value if placeholder == "{MENTION}" else html.escape(str(value))
        rendered = rendered.replace(placeholder, safe_value)
    return rendered


async def _message_content(message: Message):
    if message.text:
        return {"type": "text", "text": message.text}
    if message.photo:
        return {
            "type": "photo",
            "file_id": message.photo.file_id,
            "caption": message.caption or "",
        }
    if message.video:
        return {
            "type": "video",
            "file_id": message.video.file_id,
            "caption": message.caption or "",
        }
    if message.animation:
        return {
            "type": "animation",
            "file_id": message.animation.file_id,
            "caption": message.caption or "",
        }
    if message.document:
        return {
            "type": "document",
            "file_id": message.document.file_id,
            "caption": message.caption or "",
        }
    return None


async def _send_custom_welcome(chat_id: int, content: dict, user, group_name: str, count: int):
    content_type = content.get("type")
    if content_type == "text":
        text = await _render_template(content.get("text", ""), user, chat_id)
        return await app.send_message(
            chat_id,
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=_welcome_markup(),
        )

    caption = await _render_template(content.get("caption", ""), user, chat_id)
    send_kwargs = {
        "chat_id": chat_id,
        "caption": caption or None,
        "parse_mode": ParseMode.HTML,
        "reply_markup": _welcome_markup(),
    }
    if content_type == "photo":
        return await app.send_photo(photo=content["file_id"], **send_kwargs)
    if content_type == "video":
        return await app.send_video(video=content["file_id"], **send_kwargs)
    if content_type == "animation":
        return await app.send_animation(animation=content["file_id"], **send_kwargs)
    if content_type == "document":
        return await app.send_document(document=content["file_id"], **send_kwargs)
    return None


@app.on_message(filters.command(["welcome", "wel"]) & filters.group)
async def auto_state(_, message: Message):
    if len(message.command) == 1:
        return await message.reply_text(WELCOME_USAGE)
    member = await app.get_chat_member(message.chat.id, message.from_user.id)
    if not _is_admin(member):
        return await message.reply_text("<b>sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄʜᴀɴɢᴇ ᴡᴇʟᴄᴏᴍᴇ sᴇᴛᴛɪɴɢs!</b>")

    state = message.command[1].strip().lower()
    enabled = await is_welcome_enabled(message.chat.id)
    if state == "off":
        if not enabled:
            return await message.reply_text("<b>ᴡᴇʟᴄᴏᴍᴇ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ !</b>")
        await set_welcome_enabled(message.chat.id, False)
        return await message.reply_text(f"<b>ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɪɴ</b> {message.chat.title}")
    if state == "on":
        if enabled:
            return await message.reply_text("<b>ᴡᴇʟᴄᴏᴍᴇ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ !</b>")
        await set_welcome_enabled(message.chat.id, True)
        return await message.reply_text(f"<b>ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɪɴ</b> {message.chat.title}")
    return await message.reply_text(WELCOME_USAGE)


@app.on_message(filters.command("set") & filters.group)
async def set_welcome(_, message: Message):
    if len(message.command) < 2 or message.command[1].lower() != "welcome":
        return
    member = await app.get_chat_member(message.chat.id, message.from_user.id)
    if not _is_admin(member):
        return await message.reply_text("<b>sɪʀғ ᴀᴅᴍɪɴ ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ sᴇᴛ ᴋᴀʀ sᴀᴋᴛᴇ ʜᴀɪɴ.</b>")
    if not message.reply_to_message:
        return await message.reply_text(SET_USAGE, parse_mode=ParseMode.MARKDOWN)
    content = await _message_content(message.reply_to_message)
    if not content:
        return await message.reply_text(SET_USAGE, parse_mode=ParseMode.MARKDOWN)
    await set_welcome_message(message.chat.id, content)
    await message.reply_text("<b><emoji id='6082375377123023700'>✅</emoji> ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ sᴀᴠᴇᴅ.</b>\nNaye member ke liye ab ye message use hoga.")


@app.on_message(filters.command("del") & filters.group)
async def delete_welcome(_, message: Message):
    if len(message.command) < 2 or message.command[1].lower() != "welcome":
        return
    member = await app.get_chat_member(message.chat.id, message.from_user.id)
    if not _is_admin(member):
        return await message.reply_text("<b>sɪʀғ ᴀᴅᴍɪɴ ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ ʜᴀᴛᴀ sᴀᴋᴛᴇ ʜᴀɪɴ.</b>")
    await clear_welcome_message(message.chat.id)
    await message.reply_text("<b><emoji id='6082375377123023700'>✅</emoji> ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ ʀᴇᴍᴏᴠᴇᴅ.</b>\nAb default welcome use hoga.")


@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    if not await is_welcome_enabled(chat_id):
        return
    if not member.new_chat_member or member.old_chat_member:
        return
    if str(member.new_chat_member.status).lower().endswith("kicked"):
        return

    user = member.new_chat_member.user
    count = await app.get_chat_members_count(chat_id)
    custom = await get_welcome_message(chat_id)
    try:
        if custom:
            await _send_custom_welcome(chat_id, custom, user, member.chat.title or "", count)
            return
        caption_text = f"""
<b>⎊─────☵ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ☵─────⎊</b>
<emoji id='5197269100878907942'>📋</emoji> <b>ɢʀᴏᴜᴘ ⧽</b> {html.escape(member.chat.title or '')}
<b>▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬</b>
☉ <b>ɴᴀᴍᴇ ⧽</b> {user.mention}
☉ <b>ɪᴅ ⧽</b> `{user.id}`
☉ <b>ᴜ_ɴᴀᴍᴇ ⧽</b> @{html.escape(user.username) if user.username else 'None'}
☉ <b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ⧽</b> {count}

<b>▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬</b>
<b>⎉──────▢✭ 侖 ✭▢──────⎉</b>
"""
        await app.send_video(
            chat_id,
            video=WELCOME_VIDEO_URL,
            caption=caption_text,
            reply_markup=_welcome_markup(),
        )
    except Exception as e:
        LOGGER.error("Welcome send failed: %s", e)
