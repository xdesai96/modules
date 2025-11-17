# This file is part of XDesai Mods.
# I made this library to share various utility functions across my modules.
# You can use this library in your own modules as well.

# P.S this library is still under development and may receive updates in the future.

# meta developer: @xdesai

import logging
import re
import typing

from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.custom.participantpermissions import ParticipantPermissions
from telethon.tl.functions.channels import (EditAdminRequest,
                                            InviteToChannelRequest)
from telethon.tl.functions.messages import (HideAllChatJoinRequestsRequest,
                                            HideChatJoinRequestRequest)
from telethon.tl.types import (ChannelParticipantCreator,
                               ChannelParticipantsAdmins,
                               ChannelParticipantsBots, ChatAdminRights,
                               Message, MessageEntityMention,
                               MessageEntityMentionName, MessageEntityTextUrl,
                               MessageEntityUrl, PeerUser, User)

from .. import loader, utils
from ..types import SelfUnload

logger = logging.getLogger("XDLib")


class XDLib(loader.Library):
    """A library with various utility functions for XDesai modules."""

    developer = "@xdesai"

    strings = {
        "name": "XDLib",
        "desc": "A library with various utility functions for XD modules.",
        "request_join_reason": "Stay tuned for updates.",
        "not_legacy": "The module is supported only on <a href='https://github.com/Crayz310/Legacy'>{label}</a>",
    }

    async def init(self):
        self.format = FormatUtils()
        self.parse = ParseUtils()
        self.messages = MessageUtils(self._client)
        self.admin = AdminUtils(self._client, self)
        self.chat = ChatUtils(self._client, self._db)
        self.user = UserUtils(self._client, self._db)
        self.rights = AdminRights

    @classmethod
    async def only_legacy(self):
        if not __package__.startswith("legacy"):
            raise SelfUnload("The module is supported ONLY for Legacy userbot")

    def unload_lib(self, name: str):
        instance = self.lookup(name)
        if isinstance(instance, loader.Library):
            self.allmodules.libraries.remove(instance)
            logger.info(f"Unloaded library: {name}")
            return True
        return False


class UserUtils:
    def __init__(self, client, db):
        self._client = client
        self._db = db

    async def get_user(user_id: typing.Union[str, int, PeerUser, User]):
        userfull = await self._client.get_fulluser(user_id)
        full_user - userfull.full_user
        user = full_user.users[0]

        return {
            "common_chats_count": full_user.common_chats_count,
            "id": user.id,
            "personal_photo": full_user.personal_photo,
            "business_work_hours": full_user.business_work_hours,
            "business_intro": full_user.business_intro,
            "birthday": full_user.birthday,
            "personal_channel_id": full_user.personal_channel_id,
            "stargifts_count": full_user.stargifts_count,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username or user.usernames or None,
            "emoji_status": user.emoji_status,
            "color": user.color,
            "blocked": full_user.blocked,
            "phone_calls_available", full_user.phone_calls_available,
            "about": full_user.about,
            "profile_photo": full_user.profile_photo,
        }


class ParseUtils:
    def opts(self, args: list) -> typing.Dict[str, typing.Any]:
        """
        Parses command-line style options from a list of arguments.
        Supports sequential operations (+, -, *, /) for numeric values.
        """
        options = {}
        i = 0

        def auto_cast(value: str):
            if not value:
                return True
            low = value.lower()
            if low in {"true", "yes", "on"}:
                return True
            if low in {"false", "no", "off"}:
                return False
            if re.fullmatch(r"-?\d+", value):
                return int(value)
            if re.fullmatch(r"-?\d+\.\d+", value):
                return float(value)
            return value

        def apply_operations(base, ops: list[str]):
            val = base
            for op_str in ops:
                m = re.fullmatch(r"([+*/])(\d+(\.\d+)?)", op_str)
                if not m:
                    val = auto_cast(op_str)
                    continue
                op, number, _ = m.groups()
                number = float(number) if "." in number else int(number)
                if op == "+":
                    val += number
                elif op == "*":
                    val *= number
                elif op == "/":
                    val /= number
            return val

        while i < len(args):
            arg = args[i]

            if "=" in arg:
                key, value = arg.split("=", 1)
                key = key.lstrip("-")
                options[key] = auto_cast(value.strip("\"'"))

            elif arg.startswith("-"):
                key = arg.lstrip("-")
                values = []
                i += 1
                while i < len(args) and not args[i].startswith("-"):
                    values.append(args[i].strip("\"'"))
                    i += 1
                i -= 1

                if key in options and isinstance(options[key], (int, float)):
                    options[key] = apply_operations(options[key], values)
                else:
                    if values:
                        base = auto_cast(values[0])
                        options[key] = apply_operations(base, values[1:])
                    else:
                        options[key] = True

            i += 1

        return options

    def bool(self, value: str) -> bool:
        """Parses a string into a boolean value.

        Args:
            value (str): The input string.
        Returns:
            bool: The parsed boolean value.
        """
        true_values = {"true", "yes", "1", "on"}
        false_values = {"false", "no", "0", "off"}
        low_value = value.lower()
        if low_value in true_values:
            return True
        elif low_value in false_values:
            return False
        else:
            raise ValueError(f"Cannot parse boolean from '{value}'")

    def time(self, time_str: str) -> int:
        """Parses a time duration string into seconds.

        Args:
            time_str (str): The time duration string (e.g., "2h 30m").
        Returns:
            int: The total duration in seconds.
        """
        time_units = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
            "w": 604800,
            "y": 31536000,
        }
        total_seconds = 0
        pattern = r"(\d+)([smhdwy])"
        matches = re.findall(pattern, time_str)
        for value, unit in matches:
            total_seconds += int(value) * time_units[unit]
        return total_seconds

    def size(self, size_str: str) -> int:
        """Parses a size string into bytes.

        Args:
            size_str (str): The size string (e.g., "10MB").
        Returns:
            int: The size in bytes.
        """
        size_units = {
            "b": 1,
            "kb": 1024,
            "mb": 1024**2,
            "gb": 1024**3,
            "tb": 1024**4,
        }
        pattern = r"(\d+)([bkmgt]b?)"
        match = re.match(pattern, size_str.lower())
        if match:
            value, unit = match.groups()
            return int(value) * size_units[unit]
        return 0

    def mentions(self, msg: Message) -> typing.List[str]:
        """Extracts mentions from a given message.

        Args:
            msg (Message): The message.
        Returns:
            List[str]: A list of extracted mentions.
        """
        if msg.entities:
            mentions = []
            for entity in msg.entities:
                if isinstance(entity, MessageEntityMention):
                    offset = entity.offset
                    length = entity.length
                    mentions.append(msg.message[offset : offset + length])
                elif isinstance(entity, MessageEntityMentionName):
                    mentions.append(entity.user_id)
            return mentions
        return []

    def urls(self, msg: Message) -> typing.List[str]:
        """Extracts URLs from a given message.

        Args:
            msg (Message): The message.
        Returns:
            List[str]: A list of extracted URLs.
        """
        if msg.entities or msg.media:
            urls = []
            for entity in msg.entities:
                if isinstance(entity, MessageEntityTextUrl):
                    urls.append(entity.url)
                elif isinstance(entity, MessageEntityUrl):
                    offset = entity.offset
                    length = entity.length
                    urls.append(msg.message[offset : offset + length])
                elif msg.media and hasattr(msg.media, "webpage"):
                    if msg.media.webpage.url:
                        urls.append(msg.media.webpage.url)
            return urls
        return []


class DialogUtils:
    def __init__(self, client) -> None:
        self._client = client


class MessageUtils:
    def __init__(self, client):
        self._client = client

    async def delete_messages(self, msg: Message):
        """Deletes multiple messages based on a specific pattern.
        Args:
            msg (Message): The message containing the command and pattern.
        Returns:
            None
        """
        reply = await msg.get_reply_message()
        pattern = r"([ab])(\d+)"
        matches = re.findall(pattern, utils.get_args_raw(msg))

        ids_to_delete = [msg.id]
        if reply:
            ids_to_delete.append(reply.id)

        for direction, count_str in matches:
            count = int(count_str)
            if direction == "a":  # after
                if reply:
                    async for m in self._client.iter_messages(
                        msg.chat_id, min_id=reply.id, limit=count, reverse=True
                    ):
                        ids_to_delete.append(m.id)
            elif direction == "b":  # before
                async for m in self._client.iter_messages(
                    msg.chat_id, max_id=(reply if reply else msg).id, limit=count
                ):
                    ids_to_delete.append(m.id)

        await self._client.delete_messages(msg.chat_id, message_ids=ids_to_delete)

    async def get_sender(self, message):
        if message.out:
            return await self._client.get_me()
        if message.is_private:
            return message.peer_id
        if message.is_group and message.is_channel:
            return message.sender or message.chat


class ChatUtils:
    def __init__(self, client, db) -> None:
        self._client = client
        self._db = db

    async def join_request(self, chat, user_id, approved):
        await self._client(
            HideChatJoinRequestRequest(peer=chat, user_id=user_id, approved=approved)
        )

    async def join_requests(self, chat, approved):
        await self._client(
            HideAllChatJoinRequestsRequest(
                peer=chat,
                approved=approved,
            )
        )

    async def get_members(self, chat):
        try:
            members = await self._client.get_participants(chat)
            users = [member for member in members if not getattr(member, "bot")]
            if members:
                return members
            return None
        except Exception:
            logger.error(f"Couldn't get members of the chat {chat}")
            return None

    async def get_deleted(self, chat):
        try:
            members = await self._client.get_participants(chat)
            deleted = [member for member in members if getattr(member, "deleted")]
            if deleted:
                return deleted
            return None
        except Exception:
            logger.error(f"Couldn't get members of the chat {chat}")
            return None

    async def get_bots(self, chat):
        try:
            bots = await self._client.get_participants(
                chat, filter=ChannelParticipantsBots()
            )
            if bots:
                return bots
            return None
        except Exception:
            logger.error(f"Couldn't get bots from the chat {chat}")
            return None

    async def get_admins(self, chat, only_users: bool = False):
        try:
            admins = await self._client.get_participants(
                chat, filter=ChannelParticipantsAdmins()
            )
            users = [
                user
                for user in admins
                if user
                and not getattr(user, "bot")
                and not isinstance(
                    getattr(user, "participant"), ChannelParticipantCreator
                )
            ]
            if only_users:
                return users
            return admins
        except Exception:
            logger.error(f"Couldn't get admins from the chat {chat}")
            return None

    async def get_creator(self, chat):
        try:
            admins = await self._client.get_participants(
                chat, filter=ChannelParticipantsAdmins()
            )
            if not admins:
                return None
            for admin in admins:
                if hasattr(admin, "participant") and isinstance(
                    getattr(admin, "participant"), ChannelParticipantCreator
                ):
                    return admin
            return None
        except Exception:
            logger.error(f"Couldn't get the creator from the chat {chat}")
            return None

    async def is_member(self, chat, user) -> bool:
        """Checks if a user is a member of a chat.

        Args:
            chat_id (int): The ID of the chat.
            user_id (Union[int, str]): The ID or username of the user.
        Returns:
            bool: True if the user is a member, False otherwise.
        """
        try:
            perms = await self._client.get_perms_cached(chat, user)
            return True if perms else False
        except UserNotParticipantError:
            return False
        except Exception:
            logger.error(
                f"Failed to check membership for user {user} in chat {chat.title}",
                exc_info=True,
            )
            return False

    async def get_rights(self, chat, user) -> typing.Optional[ParticipantPermissions]:
        """Checks if a user is a member of a chat.

        Args:
            chat_id (int): The ID of the chat.
            user_id (Union[int, str]): The ID or username of the user.
        Returns:
            bool: True if the user is a member, False otherwise.
        """
        try:
            perms = await self._client.get_perms_cached(chat, user)
            return perms
        except UserNotParticipantError:
            return None
        except Exception:
            logger.error(
                f"Failed to check membership for user {user} in chat {chat.title}",
                exc_info=True,
            )
            return None

    async def invite_user(self, chat, user):
        """Invites a user to a chat.

        Args:
            chat_id (int): The ID of the chat.
            user_id (Union[int, str]): The ID or username of the user to invite.
        Returns:
            None
        """
        try:
            await self._client(InviteToChannelRequest(channel=chat, users=[user]))
            return True
        except Exception:
            logger.error(
                f"Failed to invite user {user} to chat {chat.title}", exc_info=True
            )
            return False

    async def get_info(self, chat) -> dict:
        try:
            chat_full = await self._client.get_fullchannel(chat)
            full_chat = chat_full.full_chat
            chat = chat_full.chats[0]
            return {
                "id": full_chat.id or 0,
                "about": full_chat.about or "",
                "chat_photo": full_chat.chat_photo,
                "admins_count": full_chat.admins_count or 0,
                "online_count": full_chat.online_count or 0,
                "participants_count": full_chat.participants_count or 0,
                "kicked_count": full_chat.kicked_count,
                "slowmode_seconds": full_chat.slowmode_seconds or 0,
                "call": full_chat.call or None,
                "title": chat.title or "",
                "ttl_period": full_chat.ttl_period or 0,
                "available_reactions": full_chat.available_reactions or None,
                "requests_pending": full_chat.requests_pending or 0,
                "recent_requesters": full_chat.recent_requesters or [],
                "is_forum": getattr(chat, "forum"),
                "linked_chat_id": full_chat.linked_chat_id or 0,
                "antispam": full_chat.antispam or False,
                "participants_hidden": full_chat.participants_hidden or False,
                "link": (
                    f"https://t.me/{chat.username}"
                    if chat.username
                    else (
                        full_chat.exported_invite.link
                        if full_chat.exported_invite
                        else ""
                    )
                ),
                "is_channel": chat.broadcast or False,
                "is_group": chat.megagroup or False,
            }
        except Exception:
            logger.error("Failed to get the chat info")
            return {}

    async def invite_bot(self, client, chat) -> bool:
        """Invites an inline bot to a chat.

        Args:
            client: The Telethon client instance.
            chat: The chat to invite the bot to.
        Returns:
            bool: True if the invitation was successful, False otherwise.
        """
        try:
            await self._client(
                InviteToChannelRequest(
                    chat,
                    [client.loader.inline.bot_username or client.loader.inline.bot_id],
                )
            )
        except Exception:
            logger.error("Failed to invite inline bot to chat", exc_info=True)
            return False

        rights = AdminRights.all()
        rights.remove("anonymous")
        admin = AdminUtils(self._client, self._db)
        await admin.set_rights(
            chat,
            client.loader.inline.bot_username or client.loader.inline.bot_id,
            rights.to_int(),
            rank="XD Bot",
        )
        return True


class AdminUtils:
    def __init__(self, client, lib) -> None:
        self._client = client
        self._lib = lib

    async def get_rights_table(self):
        return f"<pre><code>{AdminRights.stringify()}</code></pre>"

    async def set_role(self, chat, user, role_name, rank="XD Admin") -> bool:
        rights_obj = self._lib.roles.get_role_perms(role_name)
        if rights_obj is None:
            return False

        return await self.set_rights(chat, user, rights_obj.to_int(), rank)

    async def set_rights(self, chat, user, mask: int, rank: str = "XD Admin") -> bool:
        """Sets admin rights for a user in a chat based on a mask.

        Args:
            chat_id (int): The ID of the chat.
            user_id (Union[int, str]): The ID or username of the user.
            mask (int): The rights mask to set.
        Returns:
            bool: True if the rights were set successfully, False otherwise.
        """
        try:
            rights = AdminRights(mask)

            new_admin_rights = rights.to_chat_rights()

            await self._client(
                EditAdminRequest(
                    chat,
                    user,
                    new_admin_rights,
                    rank=rank,
                )
            )
            return True
        except Exception:
            logger.error(
                f"Failed to set rights with mask {mask} for user {user.id} in chat {chat.title}",
                exc_info=True,
            )
            return False


class FormatUtils:

    def bytes(self, size: int) -> str:
        """Formats a size in bytes into a human-readable string.

        Args:
            size (int): The size in bytes.
        Returns:
            str: The formatted size string.
        """
        if size < 1024:
            if size == 1:
                return f"{size} byte"
            return f"{size} bytes"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024**2:.2f} MB"
        elif size < 1024**4:
            return f"{size / 1024**3:.2f} GB"
        else:
            return f"{size / 1024**4:.2f} TB"

    def time(self, seconds: int) -> str:
        """Formats a time duration in seconds into a human-readable string.

        Args:
            seconds (int): The time duration in seconds.
        Returns:
            str: The formatted time string.
        """
        intervals = (
            ("years", 31536000),
            ("months", 2592000),
            ("weeks", 604800),
            ("days", 86400),
            ("hours", 3600),
            ("minutes", 60),
            ("seconds", 1),
        )
        result = []
        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip("s")
                result.append(f"{value} {name}")
        return ", ".join(result) if result else "0 seconds"


class AdminRights:

    RIGHTS_LIST = [x for x in ChatAdminRights().to_dict().keys() if x != "_"]

    RIGHTS = {name: 1 << i for i, name in enumerate(RIGHTS_LIST)}

    MAX_MASK = (1 << len(RIGHTS)) - 1

    def __init__(self, mask: int = 0):
        self.mask = mask & self.MAX_MASK

    def add(self, *right_names: str) -> None:
        for name in right_names:
            if name in self.RIGHTS:
                self.mask |= self.RIGHTS[name]

    def remove(self, *right_names: str) -> None:
        for name in right_names:
            if name in self.RIGHTS:
                self.mask &= ~self.RIGHTS[name]

    def has(self, right_name: str) -> bool:
        return bool(self.mask & self.RIGHTS.get(right_name, 0))

    def add_index(self, idx: int) -> bool:
        if 0 <= idx < len(self.RIGHTS_LIST):
            self.mask |= 1 << idx

    def remove_index(self, idx: int):
        if 0 <= idx < len(self.RIGHTS_LIST):
            self.mask &= ~(1 << idx)

    def has_index(self, idx: int) -> bool:
        if 0 <= idx < len(self.RIGHTS_LIST):
            return bool(self.mask & (1 << idx))
        return False

    def to_dict(self) -> dict[str, bool]:
        return {name: self.has(name) for name in self.RIGHTS_LIST}

    def to_int(self) -> int:
        return self.mask

    def to_chat_rights(self) -> ChatAdminRights:
        return ChatAdminRights(**self.to_dict())

    @classmethod
    def stringify_masks(cls):
        max_len = max(len(name) for name in cls.RIGHTS_LIST)
        lines = []
        for name in cls.RIGHTS_LIST:
            mask = cls.RIGHTS[name]
            lines.append(f"{name.ljust(max_len)} — {mask}")
        return "\n".join(lines)

    @classmethod
    def list_rights(cls):
        return [(i, name) for i, name in enumerate(cls.RIGHTS_LIST)]

    @classmethod
    def from_int(cls, mask: int):
        return cls(mask)

    @classmethod
    def all(cls):
        return cls(cls.MAX_MASK)

    @classmethod
    def none(cls):
        return cls(0)
