from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import (
    BotCommand, 
    BotCommandScopeChat,
    BotCommandScopeDefault,
    BotCommandScopeAllPrivateChats, 
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllChatAdministrators
)

import config
from ..misc import SUDOERS

from ..logging import LOGGER


class Anony(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="AnonXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

        try:
            # Commands for private chats
            private_commands = [
                BotCommand("start", "🚀 Start the bot"),
                BotCommand("help", "❓ Get help menu"),
                BotCommand("ping", "🏓 Check bot ping"),
                BotCommand("lang", "🌐 Change language"),
            ]
            
            # Commands for group chats (regular members only)
            group_commands = [
                # Music Commands (All Users)
                BotCommand("play", "🎵 Play music from YouTube/Spotify"),
                BotCommand("vplay", "📹 Play video from YouTube"),
                BotCommand("cplay", "🎵 Play music in linked channel"),
                BotCommand("cvplay", "📹 Play video in linked channel"),
                BotCommand("playforce", "🎵 Force play (skip queue)"),
                BotCommand("vplayforce", "📹 Force play video (skip queue)"),
                BotCommand("cplayforce", "🎵 Channel force play"),
                BotCommand("cvplayforce", "📹 Channel force play video"),
                
                # Info Commands (All Users)
                BotCommand("queue", "📜 Show current queue"),
                BotCommand("playing", "🎵 Currently playing track"),
                BotCommand("ping", "🏓 Check bot response time"),
                BotCommand("stats", "📊 Show bot statistics"),
                BotCommand("help", "❓ Get help menu"),
                BotCommand("lang", "🌐 Change group language"),
            ]
            
            # Commands for group administrators (includes all regular commands + admin commands)
            admin_commands = group_commands + [
                # Admin Commands (Group Admins)
                BotCommand("pause", "⏸️ Pause current playback"),
                BotCommand("resume", "▶️ Resume paused playback"),
                BotCommand("skip", "⏭️ Skip to next track"),
                BotCommand("stop", "⏹️ Stop music and clear queue"),
                BotCommand("shuffle", "🔀 Shuffle current queue"),
                BotCommand("loop", "🔁 Toggle loop modes"),
                BotCommand("seek", "⏩ Seek forward/backward"),
                BotCommand("speed", "⚡ Change playback speed"),
                BotCommand("auth", "👑 Give user music permissions"),
                BotCommand("unauth", "❌ Remove user permissions"),
                BotCommand("authlist", "📋 List authorized users"),
                BotCommand("settings", "⚙️ Open group settings"),
                BotCommand("playmode", "🎮 Change play mode"),
                BotCommand("channelplay", "📢 Setup channel play"),
                BotCommand("reload", "🔄 Reload admin cache"),
                BotCommand("reboot", "🔄 Restart voice chat"),
            ]
            
            # Commands for sudo users (includes admin commands + sudo commands)
            sudo_commands = admin_commands + [
                # Sudo Commands
                BotCommand("maintenance", "🔧 Toggle maintenance mode"),
                BotCommand("gban", "🚫 Global ban user"),
                BotCommand("ungban", "✅ Remove global ban"),
                BotCommand("gbannedusers", "📋 List globally banned users"),
                BotCommand("getlog", "📄 Get bot logs"),
                BotCommand("update", "⬆️ Update bot from git"),
                BotCommand("restart", "🔄 Restart bot"),
                BotCommand("block", "🚫 Block user from bot"),
                BotCommand("unblock", "✅ Unblock user"),
                BotCommand("blocked", "📋 List blocked users"),
                BotCommand("blchat", "🚫 Blacklist chat"),
                BotCommand("whitelistchat", "✅ Whitelist chat"),
                BotCommand("blchats", "📋 List blacklisted chats"),
                BotCommand("logger", "📝 Toggle logger"),
                BotCommand("cookies", "🍪 Get cookies file"),
                BotCommand("autoend", "⏰ Toggle auto end stream"),
                BotCommand("groupinfo", "ℹ️ Get group information"),
                BotCommand("add_movie", "🎬 Add movie group"),
                BotCommand("rem_movie", "❌ Remove movie group"),
                BotCommand("list_movie", "📋 List movie groups"),
                BotCommand("allow_movie", "🎬 Allow movie in current chat"),
                BotCommand("sudolist", "👑 List sudo users"),
            ]
            
            # Commands for owner (includes sudo commands + owner commands)
            owner_commands = sudo_commands + [
                # Owner Commands
                BotCommand("addsudo", "👑 Add sudo user"),
                BotCommand("delsudo", "❌ Remove sudo user"),
                BotCommand("eval", "🐍 Execute Python code"),
                BotCommand("sh", "💻 Execute shell commands"),
            ]
            
            await self.set_bot_commands(
                commands=private_commands,
                scope=BotCommandScopeAllPrivateChats()
            )
            
            await self.set_bot_commands(
                commands=group_commands,
                scope=BotCommandScopeAllGroupChats()
            )
            
            await self.set_bot_commands(
                commands=admin_commands,
                scope=BotCommandScopeAllChatAdministrators()
            )
            
            try:
                await self.set_bot_commands(
                    commands=owner_commands,
                    scope=BotCommandScopeChat(chat_id=config.OWNER_ID)
                )
            except Exception as e:
                LOGGER(__name__).error(f"❌ Failed to set owner commands: {e}")
            
            for sudo_user in SUDOERS:
                if sudo_user != config.OWNER_ID:
                    try:
                        await self.set_bot_commands(
                            commands=sudo_commands,
                            scope=BotCommandScopeChat(chat_id=sudo_user)
                        )
                    except Exception as e:
                        LOGGER(__name__).error(f"❌ Failed to set sudo commands for {sudo_user}: {e}")
            
        except Exception as e:
            LOGGER(__name__).error(f"❌ Failed to set bot commands: {e}")

    async def stop(self):
        await super().stop()
