
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import add_movie_group, remove_movie_group, get_movie_groups, is_movie_group


@app.on_message(filters.command(["add_movie"]) & SUDOERS)
async def add_movie_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("» ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴄʜᴀᴛ ɪᴅ.\n\nᴇxᴀᴍᴘʟᴇ: `/add_movie -1001234567890`")
    
    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("» ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍᴇʀɪᴄ ᴄʜᴀᴛ ɪᴅ.")
    
    if chat_id > 0:
        return await message.reply_text("» ᴏɴʟʏ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ. ᴄʜᴀᴛ ɪᴅ sʜᴏᴜʟᴅ ʙᴇ ɴᴇɢᴀᴛɪᴠᴇ.")
    
    if await is_movie_group(chat_id):
        return await message.reply_text(f"» ᴄʜᴀᴛ `{chat_id}` ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘs ʟɪsᴛ.")
    
    await add_movie_group(chat_id)
    await message.reply_text(f"» ᴄʜᴀᴛ `{chat_id}` ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘs.\n\n✅ ᴛʜɪs ɢʀᴏᴜᴘ ᴄᴀɴ ɴᴏᴡ ᴜᴘʟᴏᴀᴅ ᴠɪᴅᴇᴏs ᴡɪᴛʜᴏᴜᴛ ғɪʟᴇ sɪᴢᴇ ʟɪᴍɪᴛs.")


@app.on_message(filters.command(["rem_movie", "remove_movie"]) & SUDOERS)
async def remove_movie_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("» ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴄʜᴀᴛ ɪᴅ.\n\nᴇxᴀᴍᴘʟᴇ: `/rem_movie -1001234567890`")
    
    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("» ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍᴇʀɪᴄ ᴄʜᴀᴛ ɪᴅ.")
    
    if not await is_movie_group(chat_id):
        return await message.reply_text(f"» ᴄʜᴀᴛ `{chat_id}` ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘs ʟɪsᴛ.")
    
    await remove_movie_group(chat_id)
    await message.reply_text(f"» ᴄʜᴀᴛ `{chat_id}` ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘs.\n\n❌ ғɪʟᴇ sɪᴢᴇ ʟɪᴍɪᴛs ᴀʀᴇ ɴᴏᴡ ᴀᴄᴛɪᴠᴇ ғᴏʀ ᴛʜɪs ɢʀᴏᴜᴘ.")


@app.on_message(filters.command(["list_movie", "movie_list"]) & SUDOERS)
async def list_movie_command(client: Client, message: Message):
    movie_groups = await get_movie_groups()
    
    if not movie_groups:
        return await message.reply_text("» ɴᴏ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘs ғᴏᴜɴᴅ.\n\nᴜsᴇ `/add_movie <chat_id>` ᴛᴏ ᴀᴅᴅ ᴀ ɢʀᴏᴜᴘ.")
    
    groups_text = "🎬 **ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘs ʟɪsᴛ:**\n\n"
    for i, chat_id in enumerate(movie_groups, 1):
        try:
            chat = await app.get_chat(chat_id)
            chat_name = chat.title if chat.title else "Unknown"
            groups_text += f"{i}. **{chat_name}**\n   ᴄʜᴀᴛ ɪᴅ: `{chat_id}`\n\n"
        except:
            groups_text += f"{i}. **Unknown Group**\n   ᴄʜᴀᴛ ɪᴅ: `{chat_id}`\n\n"
    
    groups_text += f"**ᴛᴏᴛᴀʟ:** {len(movie_groups)} ɢʀᴏᴜᴘ(s)\n\n"
    groups_text += "**ɴᴏᴛᴇ:** ᴛʜᴇsᴇ ɢʀᴏᴜᴘs ᴄᴀɴ ᴜᴘʟᴏᴀᴅ ᴠɪᴅᴇᴏs ᴡɪᴛʜᴏᴜᴛ ғɪʟᴇ sɪᴢᴇ ʟɪᴍɪᴛs."
    
    await message.reply_text(groups_text)


@app.on_message(filters.command(["allow_movie"]) & SUDOERS)
async def allow_movie_current_chat(client: Client, message: Message):
    chat_id = message.chat.id
    
    if chat_id > 0:
        return await message.reply_text("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")
    
    if await is_movie_group(chat_id):
        return await message.reply_text("» ᴛʜɪs ɢʀᴏᴜᴘ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘs ʟɪsᴛ.")
    
    await add_movie_group(chat_id)
    await message.reply_text("» ᴛʜɪs ɢʀᴏᴜᴘ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘs.\n\n✅ ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴜᴘʟᴏᴀᴅ ᴠɪᴅᴇᴏs ᴡɪᴛʜᴏᴜᴛ ғɪʟᴇ sɪᴢᴇ ʟɪᴍɪᴛs.")