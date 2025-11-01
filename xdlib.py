# This file is part of XDesai Mods.
# I made this library to share various utility functions across my modules.
# You can use this library in your own modules as well.

# P.S this library is still under development and may receive updates in the future.

# meta developer: @xdesai

from .. import loader, utils
import typing
import re
from telethon.tl.types import (
    Message,
    MessageEntityTextUrl,
    MessageEntityUrl,
    MessageEntityMention,
    MessageEntityMentionName,
)
from telethon.tl.functions.channels import InviteToChannelRequest


class XDLib(loader.Library):
    """A library with various utility functions for XDesai modules."""

    developer = "@xdesai"

    strings = {
        "name": "XDLib",
        "desc": "A library with various utility functions for XD modules.",
        "request_join_reason": "Stay tuned for updates.",
        "seconds": "seconds",
        "second": "second",
        "minutes": "minutes",
        "minute": "minute",
        "hours": "hours",
        "hour": "hour",
        "days": "days",
        "day": "day",
        "weeks": "weeks",
        "week": "week",
        "months": "months",
        "month": "month",
        "years": "years",
        "year": "year",
        "bytes": "bytes",
        "byte": "byte",
        "kb": "KB",
        "mb": "MB",
        "gb": "GB",
        "tb": "TB",
    }

    def parseopts(self, args: str) -> typing.Dict[str, typing.Any]:
        """Parses command-line style options from a string.
        Args:
            args (str): The input string containing options.
        Returns:
            Dict[str, Any]: A dictionary of parsed options.
        """
        pattern = r'(?:--?)(\w+)(?:[=\s]+("[^"]*"|\'[^\']*\'|\S+))?'
        matches = re.findall(pattern, args)

        options = {}

        def auto_cast(value: str):
            low = value.lower()
            if low in {"true", "yes", "on", "false", "no", "off"}:
                return self.parse_bool(low)
            if re.fullmatch(r"-?\d+", value):
                return int(value)
            if re.fullmatch(r"-?\d+\.\d+", value):
                return float(value)
            return value

        for key, value in matches:
            if value:
                value = value.strip("\"'")
                value = auto_cast(value)
            else:
                value = True
            options[key] = value

        return options

    def format_bytes(self, size: int) -> str:
        """Formats a size in bytes into a human-readable string.

        Args:
            size (int): The size in bytes.
        Returns:
            str: The formatted size string.
        """
        if size < 1024:
            if size == 1:
                return f"{size} {self.strings['byte']}"
            return f"{size} {self.strings['bytes']}"
        elif size < 1024**2:
            return f"{size / 1024:.2f} {self.strings['kb']}"
        elif size < 1024**3:
            return f"{size / 1024**2:.2f} {self.strings['mb']}"
        elif size < 1024**4:
            return f"{size / 1024**3:.2f} {self.strings['gb']}"
        else:
            return f"{size / 1024**4:.2f} {self.strings['tb']}"

    def format_time(self, seconds: int) -> str:
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
                result.append(f"{value} {self.strings[name]}")
        return ", ".join(result) if result else f"0 {self.strings['seconds']}"

    def parse_bool(self, value: str) -> bool:
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

    def parse_time(self, time_str: str) -> int:
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

    def parse_size(self, size_str: str) -> int:
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

    def parse_mentions(self, msg: Message) -> typing.List[str]:
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

    def parse_urls(self, msg: Message) -> typing.List[str]:
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

    def unload_lib(self, name: str):
        instance = self.lookup(name)
        if isinstance(instance, loader.Library):
            self.allmodules.libraries.remove(instance)
            return True
        return False

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

        if not matches:
            return

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
            return False
