# -----------------------------------------------
# 🔸 AALIYA MUSIC BOT Project
# 🔹 /autoplay command — auto-continues music when the queue ends
# -----------------------------------------------
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.utils.database import autoplay_off, autoplay_on, is_autoplay
from config import BANNED_USERS


def _autoplay_markup(enabled: bool) -> InlineKeyboardMarkup:
    if enabled:
        buttons = [[InlineKeyboardButton("🔴 Disable", callback_data="autoplay_disable")]]
    else:
        buttons = [[InlineKeyboardButton("🟢 Enable", callback_data="autoplay_enable")]]
    buttons.append([InlineKeyboardButton("ℹ️ How it works?", callback_data="autoplay_info")])
    return InlineKeyboardMarkup(buttons)


@app.on_message(
    filters.command(["autoplay"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
    & filters.group
    & ~BANNED_USERS
)
async def autoplay_command(client, message: Message):
    enabled = await is_autoplay(message.chat.id)
    status = "ON ✅" if enabled else "OFF ❌"
    text = (
        f"🎶 <b>Autoplay:</b>\n\n"
        f"• Keeps music playing automatically.\n"
        f"• Ensures smooth and uninterrupted listening.\n"
        f"• Designed for a seamless music experience.\n\n"
        f"Current status: <b>{status}</b>"
    )
    await message.reply_text(text, reply_markup=_autoplay_markup(enabled))


@app.on_callback_query(filters.regex("^autoplay_enable$") & ~BANNED_USERS)
async def autoplay_enable_cb(client, callback_query):
    chat_id = callback_query.message.chat.id
    await autoplay_on(chat_id)
    await callback_query.answer("Autoplay enabled ✅", show_alert=False)
    await callback_query.message.edit_text(
        "🎶 <b>Autoplay:</b>\n\n"
        "• Keeps music playing automatically.\n"
        "• Ensures smooth and uninterrupted listening.\n"
        "• Designed for a seamless music experience.\n\n"
        "Current status: <b>ON ✅</b>",
        reply_markup=_autoplay_markup(True),
    )


@app.on_callback_query(filters.regex("^autoplay_disable$") & ~BANNED_USERS)
async def autoplay_disable_cb(client, callback_query):
    chat_id = callback_query.message.chat.id
    await autoplay_off(chat_id)
    await callback_query.answer("Autoplay disabled ❌", show_alert=False)
    await callback_query.message.edit_text(
        "🎶 <b>Autoplay:</b>\n\n"
        "• Keeps music playing automatically.\n"
        "• Ensures smooth and uninterrupted listening.\n"
        "• Designed for a seamless music experience.\n\n"
        "Current status: <b>OFF ❌</b>",
        reply_markup=_autoplay_markup(False),
    )


@app.on_callback_query(filters.regex("^autoplay_info$") & ~BANNED_USERS)
async def autoplay_info_cb(client, callback_query):
    await callback_query.answer(
        "ℹ️ How Autoplay works?\n\n"
        "• Automatically continues music playback.\n"
        "• Follows current audio or video mode.\n"
        "• Designed for seamless listening.\n\n"
        "🎶 Sit back & enjoy the music.",
        show_alert=True,
    )
