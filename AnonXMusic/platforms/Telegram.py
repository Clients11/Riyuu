import asyncio
import os
import time
from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Voice
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode

import config
from AnonXMusic import app
from AnonXMusic.utils.formatters import (
    check_duration,
    convert_bytes,
    get_readable_time,
    seconds_to_min,
)


class TeleAPI:
    def __init__(self):
        self.chars_limit = 4096
        self.sleep = 5

    async def send_split_text(self, message, string):
        n = self.chars_limit
        out = [(string[i : i + n]) for i in range(0, len(string), n)]
        j = 0
        for x in out:
            if j <= 2:
                j += 1
                await message.reply_text(x, disable_web_page_preview=True)
        return True

    async def get_link(self, message):
        return message.link

    async def get_filename(self, file, audio: Union[bool, str] = None):
        try:
            file_name = file.file_name
            if file_name is None:
                file_name = "ᴛᴇʟᴇɢʀᴀᴍ ᴀᴜᴅɪᴏ" if audio else "ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏ"
        except:
            file_name = "ᴛᴇʟᴇɢʀᴀᴍ ᴀᴜᴅɪᴏ" if audio else "ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏ"
        return file_name

    async def get_duration(self, file):
        try:
            dur = seconds_to_min(file.duration)
        except:
            dur = "Unknown"
        return dur

    async def get_duration(self, filex, file_path):
        try:
            dur = seconds_to_min(filex.duration)
        except:
            try:
                dur = await asyncio.get_event_loop().run_in_executor(
                    None, check_duration, file_path
                )
                dur = seconds_to_min(dur)
            except:
                return "Unknown"
        return dur

    async def get_filepath(
        self,
        audio: Union[bool, str] = None,
        video: Union[bool, str] = None,
    ):
        if audio:
            try:
                file_name = (
                    audio.file_unique_id
                    + "."
                    + (
                        (audio.file_name.split(".")[-1])
                        if (not isinstance(audio, Voice))
                        else "ogg"
                    )
                )
            except:
                file_name = audio.file_unique_id + "." + "ogg"
            file_name = os.path.join(os.path.realpath("downloads"), file_name)
        if video:
            try:
                file_name = (
                    video.file_unique_id + "." + (video.file_name.split(".")[-1])
                )
            except:
                file_name = video.file_unique_id + "." + "mp4"
            file_name = os.path.join(os.path.realpath("downloads"), file_name)
        return file_name

    async def download(self, _, message, mystic, fname):
        speed_counter = {}
        last_update_time = {}  # Track last update time to prevent flooding
        if os.path.exists(fname):
            return True

        async def down_load():
            async def progress(current, total):
                if current == total:
                    return
                    
                current_time = time.time()
                start_time = speed_counter.get(message.id)
                if not start_time:
                    return
                    
                # Flood control: Update only every 5 seconds minimum
                last_update = last_update_time.get(message.id, 0)
                if current_time - last_update < 5:
                    return
                    
                check_time = current_time - start_time
                if check_time < 1:  # Avoid division by zero
                    return
                    
                percentage = (current * 100) / total
                speed = current / check_time
                eta = int((total - current) / speed) if speed > 0 else 0
                eta_readable = get_readable_time(eta) if eta > 0 else "0 sᴇᴄᴏɴᴅs"
                
                total_size = convert_bytes(total)
                completed_size = convert_bytes(current)
                speed_readable = convert_bytes(speed)
                
                # Create progress bar
                filled_length = int(20 * current // total)
                bar = "█" * filled_length + "░" * (20 - filled_length)
                
                # Create attractive UI
                progress_text = f"""
🎵 **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴍᴇᴅɪᴀ...**

📊 **ᴘʀᴏɢʀᴇss:**
`{bar}` **{percentage:.1f}%**

📁 **ғɪʟᴇ ɪɴғᴏ:**
**ᴄᴏᴍᴘʟᴇᴛᴇᴅ:** `{completed_size}`
**ᴛᴏᴛᴀʟ sɪᴢᴇ:** `{total_size}`

⚡ **sᴘᴇᴇᴅ:** `{speed_readable}/s`
⏰ **ᴇᴛᴀ:** `{eta_readable}`

🤖 **ʙᴏᴛ:** {app.mention}
"""

                upl = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="❌ ᴄᴀɴᴄᴇʟ ᴅᴏᴡɴʟᴏᴀᴅ",
                                callback_data="stop_downloading",
                            ),
                        ]
                    ]
                )
                
                try:
                    await mystic.edit_text(
                        text=progress_text,
                        reply_markup=upl,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    last_update_time[message.id] = current_time
                except FloodWait as x:
                    await asyncio.sleep(int(x.x))
                except Exception as e:
                    pass

            speed_counter[message.id] = time.time()
            last_update_time[message.id] = 0  # Initialize update time tracker
            try:
                await app.download_media(
                    message.reply_to_message,
                    file_name=fname,
                    progress=progress,
                )
                try:
                    elapsed = get_readable_time(
                        int(int(time.time()) - int(speed_counter[message.id]))
                    )
                except:
                    elapsed = "0 sᴇᴄᴏɴᴅs"
                
                # Final success message with attractive UI
                success_text = f"""
✅ **ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**

⏱️ **ᴛɪᴍᴇ ᴛᴀᴋᴇɴ:** `{elapsed}`
🎵 **ʀᴇᴀᴅʏ ᴛᴏ ᴘʟᴀʏ!**

🤖 **ʙᴏᴛ:** {app.mention}
"""
                await mystic.edit_text(success_text, parse_mode=ParseMode.MARKDOWN)

                # Clean up tracking data
                if message.id in speed_counter:
                    del speed_counter[message.id]
                if message.id in last_update_time:
                    del last_update_time[message.id]
                    
            except Exception as e:
                error_text = f"""
❌ **ᴅᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ!**

⚠️ **ᴇʀʀᴏʀ:** Something went wrong during download
🔄 **sᴏʟᴜᴛɪᴏɴ:** Please try again

🤖 **ʙᴏᴛ:** {app.mention}
"""
                await mystic.edit_text(error_text, parse_mode=ParseMode.MARKDOWN)
                
                # Clean up tracking data
                if message.id in speed_counter:
                    del speed_counter[message.id]
                if message.id in last_update_time:
                    del last_update_time[message.id]

        task = asyncio.create_task(down_load())
        config.lyrical[mystic.id] = task
        await task
        verify = config.lyrical.get(mystic.id)
        if not verify:
            return False
        config.lyrical.pop(mystic.id)
        return True
