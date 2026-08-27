# Goodbye message disabled
from SIMPLE_MUSIC import app
from pyrogram import filters
from pyrogram.types import ChatMemberUpdated

@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client, member: ChatMemberUpdated):
    # Goodbye message permanently disabled
    return
