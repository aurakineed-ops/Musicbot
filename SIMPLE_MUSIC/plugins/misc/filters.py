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
import re
import random
import config
from SIMPLE_MUSIC import app
from config import BOT_USERNAME
from SIMPLE_MUSIC.utils.Simple_ban import admin_filter
from SIMPLE_MUSIC.mongo.filtersdb import *
from SIMPLE_MUSIC.utils.filters_func import GetFIlterMessage, get_text_reason, SendFilterMessage
from SIMPLE_MUSIC.utils.senoritadb import user_admin
from pyrogram import filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

# 1. FILTER SET KARNE KA FUNCTION (Text, Sticker, Media Sab Support Karega)
@app.on_message(filters.command("filter") & filters.group & admin_filter)
@user_admin
async def _filter(client, message):
    chat_id = message.chat.id 
    
    if len(message.command) < 2:
        await message.reply_text("❌ <b>Filter ka naam batayein!</b>\nUsage: Kisi message/sticker par reply karein aur likhein `/filter <name>`")
        return

    # Filter ke naam ko space-free aur lowercase banayein uniform storage ke liye
    filter_name = message.command[1].strip().lower()
    if not filter_name:
        await message.reply_text("❌ <b>Filter ka naam empty nahi ho sakta!</b>")
        return
    
    if not message.reply_to_message:
        await message.reply_text("❌ <b>Kisi text, sticker, ya photo par reply karke ye command dein!</b>")
        return

    try:
        # GetFIlterMessage automatic sticker/media/text detect kar leta hai
        content, text, data_type = await GetFIlterMessage(message)
        if data_type is None:
            await message.reply_text(
                "❌ Is message type ke liye filter support nahi hai. "
                "Text, sticker, photo, video, audio, voice ya document use karein."
            )
            return
        await add_filter_db(chat_id, filter_name=filter_name, content=content, text=text, data_type=data_type)
        await message.reply_text(f"<emoji id='6082375377123023700'>✅</emoji> Saved filter '`{filter_name}`' successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Error saving filter: {e}")


# 2. FILTER CHECK KARNE KA FUNCTION (Jab koi group me chat karega)
@app.on_message(~filters.bot & filters.group, group=4)
async def FilterCheckker(client, message):
    if not message.text and not message.caption:
        return
        
    text = (message.text or message.caption).strip().lower()
    chat_id = message.chat.id
    
    try:
        ALL_FILTERS = await get_filters_list(chat_id)
    except Exception:
        return
    if not ALL_FILTERS or len(ALL_FILTERS) == 0:
        return

    for filter_ in ALL_FILTERS:
        # Agar user khud filter command check kar raha ho toh skip karein
        if (
            message.command
            and message.command[0] == 'filter'
            and len(message.command) >= 2
            and message.command[1].lower() == filter_.lower()
        ):
            return
            
        # Word matching filter logic
        pattern = r"( |^|[^\w])" + re.escape(filter_.lower()) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            try:
                filter_data = await get_filter(chat_id, filter_)
            except Exception:
                continue
            if not filter_data:
                continue
            filter_name, content, text, data_type = filter_data
            if not content and data_type != 1:
                continue
            try:
                await SendFilterMessage(
                    message=message,
                    filter_name=filter_,
                    content=content,
                    text=text,
                    data_type=data_type
                )
            except Exception:
                return
            break


# 3. FILTERS LIST DEKHNE KA FUNCTION
@app.on_message(filters.command('filters') & filters.group)
async def _filters(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    if message.chat.type == enums.ChatType.PRIVATE:
        chat_title = 'local'
        
    FILTERS = await get_filters_list(chat_id)
    
    if not FILTERS or len(FILTERS) == 0:
        await message.reply_text(f'No active filters in {chat_title}.')
        return

    filters_list = f'List of filters in {chat_title}:\n'
    for filter_ in FILTERS:
        filters_list += f'- `{filter_}`\n'
    
    await message.reply_text(filters_list)


# 4. FILTER STOP/DELETE KARNE KA FUNCTION (100% Fixed Bug)
@app.on_message(filters.command('stopfilter') & filters.group & admin_filter)
@user_admin
async def stop(client, message):
    chat_id = message.chat.id
    
    if len(message.command) < 2:
        await message.reply_text('❌ Please specify a filter name.\nExample: `/stopfilter hello`')
        return
    
    filter_name = message.command[1].strip().lower()
    current_filters = await get_filters_list(chat_id)
    
    if not current_filters:
        await message.reply_text("You haven't saved any filters in this group yet!")
        return
        
    current_filters_lowercase = [f.lower() for f in current_filters]

    if filter_name not in current_filters_lowercase:
        await message.reply_text(f"You haven't saved any filter on the word `{filter_name}` yet!")
        return
    
    # Db se exact matching string delete karne ke liye
    actual_name = current_filters[current_filters_lowercase.index(filter_name)]
    
    try:
        await stop_db(chat_id, actual_name)
        await message.reply_text(f"<emoji id='5472030751648127392'>🛑</emoji> I've successfully stopped and deleted `{actual_name}`.")
    except Exception as e:
        await message.reply_text(f"Error while deleting filter: {e}")


# 5. SARE FILTERS EK SATH STOP KARNE KA FUNCTION
@app.on_message(filters.command('stopall') & admin_filter)
async def stopall(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    user = await client.get_chat_member(chat_id, message.from_user.id)
    if not user.status == ChatMemberStatus.OWNER:
        return await message.reply_text("Only Group Owner Can Use This Command!!") 

    r1, r2 = random.choices(STYLES, k=2)
    KEYBOARD = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='Delete all filters', callback_data='custfilters_stopall', **_get_style(r1))],
        [InlineKeyboardButton(text='Cancel', callback_data='custfilters_cancel', **_get_style(r2))]]
    )

    await message.reply_text(
        text=(f'Are you sure you want to stop <b>ALL</b> filters in {chat_title}? This action is irreversible.'),
        reply_markup=KEYBOARD
    )


@app.on_callback_query(filters.regex("^custfilters_"))
async def stopall_callback(client, callback_query: CallbackQuery):  
    chat_id = callback_query.message.chat.id 
    query_data = callback_query.data.split('_')[1]  

    user = await client.get_chat_member(chat_id, callback_query.from_user.id)
    if not user.status == ChatMemberStatus.OWNER:
        return await callback_query.answer("Only Owner Can Use This!!", show_alert=True) 
    
    if query_data == 'stopall':
        await stop_all_db(chat_id)
        await callback_query.edit_message_text(text="I've successfully deleted all chat filters.")
    elif query_data == 'cancel':
        await callback_query.edit_message_text(text='Cancelled process.')
