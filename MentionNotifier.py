# meta developer: @xdesai & @devjmodules

from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class MentionNotifierMod(loader.Module):
    """Notifies you when you are mentioned in groups and channels"""
    strings = {"name": "MentionNotifier"}
    def __init__(self):
        self.name = self.strings["name"]
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "BLACKLIST", [], validator=loader.validators.Series(),
            ),
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def mnblockcmd(self, message):
        """Adds a user to the blacklist"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user_id = (
            int(args) if args.isdigit() else (await self.client.get_entity(args)).id
        ) if args else reply.sender_id
        blacklist = self.config["BLACKLIST"]
        if user_id not in blacklist:
            blacklist.append(user_id)
            self.set("BLACKLIST", blacklist)
            await message.edit(f"Added {user_id} to the blacklist")
        else:
            await message.edit(f"{user_id} is already in the blacklist")

    async def mnunblockcmd(self, message):
        """Removes a user from the blacklist"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user_id = (
            int(args) if args.isdigit() else (await self.client.get_entity(args)).id
        ) if args else reply.sender_id
        blacklist = self.config["BLACKLIST"]
        if user_id in blacklist:
            blacklist.remove(user_id)
            self.set("BLACKLIST", blacklist)
            await message.edit(f"Removed {user_id} from the blacklist")
        else:
            await message.edit(f"{user_id} is not in the blacklist")

    async def mnlistcmd(self, message):
        """Lists the users to ignore mentions from"""
        blacklist = self.config["BLACKLIST"]
        output = "Users to ignore mentions from:\n"
        if blacklist:
            for user in blacklist:
                output += f"- {user}\n"
                await message.edit(f"{output}")
        else:
            await message.edit("No users to ignore mentions from")

    async def watcher(self, message : Message):
        if isinstance(message, Message):
            if message.mentioned and (message.is_group or message.is_channel):
                chat = await message.get_chat()
                sender = await message.get_sender()
                me = await self.client.get_me()
                if sender.id == me.id or sender.bot or sender.id in self.config["BLACKLIST"]:
                    return
                chat_link = f"https://t.me/c/{chat.id}/{message.id}"
                if sender.username:
                    notification = f"You were mentioned by @{sender.username} in <b>{chat.title}</b>.\nLink: {chat_link}"
                else:
                    notification = f"You were mentioned by <i><b>{sender.first_name}</b></i> in <b>{chat.title}</b>.\nLink: {chat_link}"
                await self.inline.bot.send_message(892742378, notification, parse_mode="html")
