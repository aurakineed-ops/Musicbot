# -----------------------------------------------
# 🔸 YORU MUSIC BOT Project
# 🔹 /autoplay command — auto-continues music when the queue ends
# -----------------------------------------------
import asyncio
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.utils.database import autoplay_off, autoplay_on, is_autoplay
from config import BANNED_USERS

USAGE = (
    "🎶 <b>Autoplay</b>\n\n"
    "• Keeps music playing automatically when the queue runs out.\n"
    "• If someone adds a song with /play, that plays FIRST — "
    "autoplay only resumes once the queue is empty again.\n"
    "• Never repeats a recently played song.\n\n"
    "<b>ᴜsᴀɢᴇ:</b>\n"
    "⦿ /autoplay enable\n"
    "⦿ /autoplay disable"
)


@app.on_message(
    filters.command(["autoplay"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
    & filters.group
    & ~BANNED_USERS
)
async def autoplay_command(client, message: Message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        enabled = await is_autoplay(chat_id)
        status = "ON ✅" if enabled else "OFF ❌"
        return await message.reply_text(f"{USAGE}\n\nCurrent status: <b>{status}</b>")

    state = message.text.split(None, 1)[1].strip().lower()

    if state == "enable":
        if await is_autoplay(chat_id):
            return await message.reply_text("🎶 Autoplay is already <b>ON ✅</b>")
        await autoplay_on(chat_id)
        await message.reply_text("🎶 Autoplay enabled <b>✅</b>")

        from SIMPLE_MUSIC.core.call import SIMPLE
        from SIMPLE_MUSIC.misc import db
        check = db.get(chat_id)
        if check and len(check) == 1:
            asyncio.create_task(
                SIMPLE.reserve_next_autoplay(chat_id, check[0]["chat_id"], check[0]["title"], "Autoplay", check[0].get("vidid"))
            )

    elif state == "disable":
        if not await is_autoplay(chat_id):
            return await message.reply_text("🎶 Autoplay is already <b>OFF ❌</b>")
        await autoplay_off(chat_id)
        await message.reply_text("🎶 Autoplay disabled <b>❌</b>")

    else:
        await message.reply_text(USAGE)


@app.on_callback_query(filters.regex(r"^autoplay_toggle (-?\d+)$"))
async def autoplay_toggle_cb(client, callback_query: CallbackQuery):
    chat_id = int(callback_query.matches[0].group(1))

    if await is_autoplay(chat_id):
        await autoplay_off(chat_id)
        await callback_query.answer("Autoplay OFF ❌")
    else:
        await autoplay_on(chat_id)
        await callback_query.answer("Autoplay ON ✅")

        from SIMPLE_MUSIC.core.call import SIMPLE
        from SIMPLE_MUSIC.misc import db
        check = db.get(chat_id)
        if check and len(check) == 1:
            asyncio.create_task(
                SIMPLE.reserve_next_autoplay(chat_id, check[0]["chat_id"], check[0]["title"], "Autoplay", check[0].get("vidid"))
            )

    try:
        from pyrogram.types import InlineKeyboardMarkup
        from SIMPLE_MUSIC.misc import db
        from SIMPLE_MUSIC.utils.database import get_lang
        from SIMPLE_MUSIC.utils.formatters import seconds_to_min
        from SIMPLE_MUSIC.utils.inline.play import stream_markup, stream_markup_timer
        from strings import get_string

        language = await get_lang(chat_id)
        _ = get_string(language)
        playing = db.get(chat_id)
        if playing and int(playing[0].get("seconds", 0)) != 0:
            buttons = await stream_markup_timer(_, chat_id, seconds_to_min(playing[0]["played"]), playing[0]["dur"])
        else:
            buttons = await stream_markup(_, chat_id)
        await callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except Exception:
        pass


@app.on_callback_query(filters.regex(r"^autoplay_search_now (-?\d+)$"))
async def autoplay_search_now_cb(client, callback_query: CallbackQuery):
    """The 'No More Songs' card's Autoplay button — deletes that card and
    immediately searches for + plays a fresh song, then leaves autoplay ON
    so it keeps going from here."""
    chat_id = int(callback_query.matches[0].group(1))
    await callback_query.answer("🔎 Searching...")

    try:
        await callback_query.message.delete()
    except Exception:
        pass

    await autoplay_on(chat_id)

    from SIMPLE_MUSIC.core.call import SIMPLE
    from SIMPLE_MUSIC.utils.database import group_assistant

    seed = SIMPLE._pending_seed.pop(chat_id, None)
    if not seed or not seed.get("title"):
        return await client.send_message(
            chat_id, "🎶 Couldn't find a recent song to continue from — use /play to start again."
        )

    try:
        assistant = await group_assistant(SIMPLE, chat_id)
    except Exception:
        return await client.send_message(chat_id, "🎶 Couldn't rejoin the videochat — try /play again.")

    started = await SIMPLE._autoplay_next(assistant, chat_id, seed)
    if not started:
        await client.send_message(
            chat_id, "🎶 Couldn't find a fresh song right now — use /play to start something."
        )
