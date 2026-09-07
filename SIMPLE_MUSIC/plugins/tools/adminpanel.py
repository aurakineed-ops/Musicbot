# -----------------------------------------------
# Owner Admin Panel — /admin
# Lets the bot owner change bot media (start photo, welcome video,
# loading sticker, now-playing thumbnails, etc.) and a few on/off
# switches (colour buttons, premium emoji icons) live, without
# touching config.py or any plugin file by hand.
# -----------------------------------------------
import config
from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from SIMPLE_MUSIC import app
from config import OWNER_ID
from SIMPLE_MUSIC.utils.dynamic_settings import (
    MEDIA_SETTINGS,
    TOGGLE_SETTINGS,
    get_media,
    get_toggle,
    set_setting,
)

MEDIA_KEYS = list(MEDIA_SETTINGS.keys())

# admin_id -> media key currently being changed (waiting for their next message)
_pending = {}


def _close_icon():
    if getattr(config, "BUTTON_ICON", False):
        return {"icon_custom_emoji_id": "5424756476117807727"}
    return {}


def _home_markup():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⚙️ ʙᴏᴛ ᴛᴏɢɢʟᴇs", callback_data="adm_toggles")],
            [InlineKeyboardButton("🖼 ᴍᴇᴅɪᴀ sᴇᴛᴛɪɴɢs", callback_data="adm_media")],
            [InlineKeyboardButton("✕ ᴄʟᴏsᴇ", callback_data="close", **_close_icon())],
        ]
    )


def _toggles_markup():
    rows = []
    for key, label in TOGGLE_SETTINGS.items():
        state = "✅ ᴏɴ" if get_toggle(key) else "❌ ᴏғғ"
        rows.append([InlineKeyboardButton(f"{label} — {state}", callback_data=f"adm_tg_{key}")])
    rows.append([InlineKeyboardButton("← ʙᴀᴄᴋ", callback_data="adm_home")])
    return InlineKeyboardMarkup(rows)


def _media_list_markup():
    rows = []
    for i, key in enumerate(MEDIA_KEYS):
        label = MEDIA_SETTINGS[key][0]
        rows.append([InlineKeyboardButton(label, callback_data=f"adm_mv_{i}")])
    rows.append([InlineKeyboardButton("← ʙᴀᴄᴋ", callback_data="adm_home")])
    return InlineKeyboardMarkup(rows)


def _media_detail_markup(i):
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✏️ ᴄʜᴀɴɢᴇ", callback_data=f"adm_mc_{i}")],
            [InlineKeyboardButton("← ʙᴀᴄᴋ", callback_data="adm_media")],
        ]
    )


@app.on_message(filters.command("admin") & filters.user(OWNER_ID))
async def admin_panel_cmd(_, message: Message):
    await message.reply_text(
        "👑 <b>ᴏᴡɴᴇʀ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ</b>\n\n"
        "ʏᴀʜᴀɴ sᴇ ʙᴏᴛ ᴋɪ ᴍᴇᴅɪᴀ ᴀᴜʀ sᴇᴛᴛɪɴɢs ʙᴀᴅᴀʟ sᴀᴋᴛᴇ ʜᴏ — code touch karne ki zaroorat nahi.",
        reply_markup=_home_markup(),
    )


@app.on_callback_query(filters.regex("^adm_home$") & filters.user(OWNER_ID))
async def adm_home_cb(_, query: CallbackQuery):
    _pending.pop(query.from_user.id, None)
    await query.message.edit_text(
        "👑 <b>ᴏᴡɴᴇʀ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ</b>\n\n"
        "ʏᴀʜᴀɴ sᴇ ʙᴏᴛ ᴋɪ ᴍᴇᴅɪᴀ ᴀᴜʀ sᴇᴛᴛɪɴɢs ʙᴀᴅᴀʟ sᴀᴋᴛᴇ ʜᴏ — code touch karne ki zaroorat nahi.",
        reply_markup=_home_markup(),
    )


@app.on_callback_query(filters.regex("^adm_toggles$") & filters.user(OWNER_ID))
async def adm_toggles_cb(_, query: CallbackQuery):
    await query.message.edit_text(
        "⚙️ <b>ʙᴏᴛ ᴛᴏɢɢʟᴇs</b>\n\nᴛᴀᴘ ᴋᴀʀᴋᴇ ᴏɴ/ᴏғғ ᴋᴀʀᴏ:",
        reply_markup=_toggles_markup(),
    )


@app.on_callback_query(filters.regex(r"^adm_tg_(.+)$") & filters.user(OWNER_ID))
async def adm_toggle_flip_cb(_, query: CallbackQuery):
    key = query.matches[0].group(1)
    if key not in TOGGLE_SETTINGS:
        return await query.answer("Unknown setting.", show_alert=True)
    new_value = not get_toggle(key)
    await set_setting(key, new_value)
    await query.answer(f"{TOGGLE_SETTINGS[key]} → {'ON' if new_value else 'OFF'}")
    await query.message.edit_reply_markup(_toggles_markup())


@app.on_callback_query(filters.regex("^adm_media$") & filters.user(OWNER_ID))
async def adm_media_cb(_, query: CallbackQuery):
    _pending.pop(query.from_user.id, None)
    await query.message.edit_text(
        "🖼 <b>ᴍᴇᴅɪᴀ sᴇᴛᴛɪɴɢs</b>\n\nᴋᴏɴsᴀ ᴍᴇᴅɪᴀ ᴅᴇᴋʜɴᴀ/ʙᴀᴅᴀʟɴᴀ ʜᴀɪ?",
        reply_markup=_media_list_markup(),
    )


@app.on_callback_query(filters.regex(r"^adm_mv_(\d+)$") & filters.user(OWNER_ID))
async def adm_media_view_cb(_, query: CallbackQuery):
    i = int(query.matches[0].group(1))
    if i >= len(MEDIA_KEYS):
        return await query.answer("Invalid item.", show_alert=True)
    key = MEDIA_KEYS[i]
    label, mtype, _default = MEDIA_SETTINGS[key]
    current = get_media(key)
    text = f"🖼 <b>{label}</b>\n\nᴛʏᴘᴇ: {mtype}\nᴄᴜʀʀᴇɴᴛ: {current if current else 'Not set'}"
    try:
        await query.message.delete()
    except Exception:
        pass
    sender = {
        "photo": app.send_photo,
        "video": app.send_video,
        "sticker": app.send_sticker,
    }.get(mtype)
    sent = False
    if current and sender:
        try:
            if mtype == "sticker":
                await sender(query.message.chat.id, current)
                await app.send_message(query.message.chat.id, text, reply_markup=_media_detail_markup(i))
            else:
                await sender(query.message.chat.id, current, caption=text, reply_markup=_media_detail_markup(i))
            sent = True
        except Exception:
            sent = False
    if not sent:
        await app.send_message(query.message.chat.id, text, reply_markup=_media_detail_markup(i))


@app.on_callback_query(filters.regex(r"^adm_mc_(\d+)$") & filters.user(OWNER_ID))
async def adm_media_change_cb(_, query: CallbackQuery):
    i = int(query.matches[0].group(1))
    if i >= len(MEDIA_KEYS):
        return await query.answer("Invalid item.", show_alert=True)
    key = MEDIA_KEYS[i]
    label, mtype, _default = MEDIA_SETTINGS[key]
    _pending[query.from_user.id] = key
    hint = {
        "photo": "ᴇᴋ ᴘʜᴏᴛᴏ ʙʜᴇᴊᴏ ʏᴀ ᴜsᴋᴀ ᴅɪʀᴇᴄᴛ URL.",
        "video": "ᴇᴋ ᴠɪᴅᴇᴏ ʙʜᴇᴊᴏ ʏᴀ ᴜsᴋᴀ ᴅɪʀᴇᴄᴛ URL.",
        "sticker": "ᴡᴏ sᴛɪᴄᴋᴇʀ ʏᴀʜᴀɴ ʙʜᴇᴊᴏ ᴊᴏ sᴇᴛ ᴋᴀʀɴᴀ ʜᴀɪ.",
    }.get(mtype, "ɴᴀʏᴀ ᴠᴀʟᴜᴇ ʙʜᴇᴊᴏ.")
    await query.answer()
    await app.send_message(
        query.message.chat.id,
        f"✏️ <b>{label}</b> ᴋᴇ ʟɪᴇ {hint}\n\nCancel karne ke liye /admin bhejo.",
    )


@app.on_message(filters.private & filters.user(OWNER_ID) & ~filters.command(["admin"]), group=5)
async def adm_capture_media(_, message: Message):
    admin_id = message.from_user.id
    if admin_id not in _pending:
        return
    key = _pending.get(admin_id)
    label, mtype, _default = MEDIA_SETTINGS.get(key, (key, "text", None))

    value = None
    if mtype == "photo" and message.photo:
        value = message.photo.file_id
    elif mtype == "video" and message.video:
        value = message.video.file_id
    elif mtype == "sticker" and message.sticker:
        value = message.sticker.file_id
    elif message.text and message.text.strip().startswith("http"):
        value = message.text.strip()

    if not value:
        return await message.reply_text(
            f"ʏᴇ {mtype} ᴋᴇ ᴀɴᴜsᴀʀ ɴᴀʜɪ ʜᴀɪ. sᴀʜɪ ᴛʏᴘᴇ ᴋᴀ ᴍᴇᴅɪᴀ ʏᴀ URL ʙʜᴇᴊᴏ, ʏᴀ /admin sᴇ ᴄᴀɴᴄᴇʟ ᴋᴀʀᴏ."
        )

    await set_setting(key, value)
    _pending.pop(admin_id, None)
    await message.reply_text(f"✅ <b>{label}</b> ᴜᴘᴅᴀᴛᴇ ʜᴏ ɢᴀʏᴀ — ᴀʙʜɪ sᴇ ʟᴀɢᴜ ʜᴀɪ, ʀᴇsᴛᴀʀᴛ ᴋɪ ᴢᴀʀᴜʀᴀᴛ ɴᴀʜɪ.")
