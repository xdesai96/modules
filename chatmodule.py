# meta developer: @xdesai
# scope: disable_onload_docs
# packurl: https://raw.githubusercontent.com/xdesai96/modules/refs/heads/main/translations/chatmodule.yml

import logging
from datetime import datetime, timedelta, timezone

from telethon.tl import types
from telethon.tl.functions import channels, messages

from .. import loader, utils
from ..types import SelfUnload

logger = logging.getLogger("ChatModule")


@loader.tds
class ChatModuleMod(loader.Module):
    strings = {
        "name": "ChatModule",
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self.xdlib = await self.import_lib(
            "https://mods.xdesai.top/xdlib.py",
            suspend_on_error=True,
        )
        await self.xdlib.only_legacy()
        self._roles = self.xdlib._db.pointer(
            self.xdlib.__class__.__name__, "ChatModule_Roles", {}
        )
        await self.request_join(
            "@xdesai_modules", self.xdlib.strings["request_join_reason"]
        )

    @loader.command(ru_doc="[reply] - Узнать ID")
    async def id(self, message):
        """[reply] - Get the ID"""
        ids = [self.strings["my_id"].format(id=self.tg_id)]
        if message.is_private:
            ids.append(self.strings["user_id"].format(id=message.to_id.user_id))
            return await utils.answer(message, "\n".join(ids))
        ids.append(self.strings["chat_id"].format(id=message.chat_id))
        reply = await message.get_reply_message()
        if (
            reply
            and not getattr(reply, "is_private")
            and not getattr(reply, "sender_id") == self.tg_id
        ):
            user_id = (await reply.get_sender()).id
            ids.append(self.strings["user_id"].format(id=user_id))
        return await utils.answer(message, "\n".join(ids))

    @loader.command(
        ru_doc="[reply/-u username/id] - Посмотреть права администратора пользователя",
    )
    @loader.tag("no_pm")
    async def rights(self, message):
        """[reply/-u username/id] - Check user's admin rights"""
        args = utils.get_args(message)
        opts = self.xdlib.parse.opts(args)
        reply = await message.get_reply_message()
        user = opts.get("u") or opts.get("user") or (reply.sender_id if reply else None)
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        rights = await self.xdlib.chat.get_rights(message.chat, user)

        participant = rights.participant
        user = await self._client.get_entity(user)
        if not hasattr(participant, "admin_rights"):
            return await utils.answer(
                message, self.strings["not_an_admin"].format(user=user.first_name)
            )
        if participant.admin_rights:
            can_do = []
            rights = participant.to_dict().get("admin_rights")
            for right, is_permitted in rights.items():
                if right == "_":
                    continue
                if is_permitted:
                    can_do.append(right)
            promoter = (
                await self._client.get_entity(participant.promoted_by)
                if hasattr(participant, "promoted_by")
                else None
            )
            return await utils.answer(
                message,
                self.strings["admin_rights"].format(
                    rights="\n".join(
                        [
                            f"<emoji document_id=5409029658794537988>✅</emoji> {self.strings[right]}"
                            for right in can_do
                        ]
                    ),
                    promoter_id=promoter.id if promoter else 0,
                    promoter_name=(
                        promoter.first_name if promoter else self.strings["no"]
                    ),
                    name=user.first_name,
                ),
            )
        return await utils.answer(
            message, self.strings["not_an_admin"].format(user=user.first_name)
        )

    @loader.command(
        ru_doc="Покинуть чат",
    )
    @loader.tag("no_pm")
    async def leave(self, message):
        """Leave chat"""
        await message.delete()
        await self._client(channels.LeaveChannelRequest((await message.get_chat()).id))

    @loader.command(
        ru_doc="[a[1-100] b[1-100]] | [reply] Удалить сообщения",
    )
    async def d(self, message):
        """[a[1-100] b[1-100]] | [reply] - Delete messages"""
        await self.xdlib.messages.delete_messages(message)

    @loader.command(ru_doc="[reply] - Закрепить сообщение")
    @loader.tag("only_reply")
    async def pin(self, message):
        """[reply] - Pin a message"""
        reply = await message.get_reply_message()
        try:
            await reply.pin(notify=True, pm_oneside=False)
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["pin_failed"])
        await utils.answer(message, self.strings["pinned"])

    @loader.command(ru_doc="Открепить сообщение")
    @loader.tag("only_reply")
    async def unpin(self, message):
        """Unpin a message"""
        reply = await message.get_reply_message()
        try:
            await reply.unpin()
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["unpin_failed"])
        await utils.answer(message, self.strings["unpinned"])

    @loader.command(ru_doc="[-c id] Удаляет группу/канал")
    async def dgc(self, message):
        """[-c id] Delete chat/channel"""
        args = utils.get_args(message)
        opts = self.xdlib.parse.opts(args)
        chat_id = opts.get("c") or opts.get("chat")
        if chat_id:
            chat = await self._client.get_entity(chat_id)
            if isinstance(chat, types.Channel):
                await self._client(channels.DeleteChannelRequest(chat.id))
            elif isinstance(chat, types.Chat):
                await self._client(messages.DeleteChatRequest(chat.id))
            else:
                return await utils.answer(message, self.strings["failed_to_delete"])
            return
        if isinstance(message.chat, types.Channel):
            await self._client(channels.DeleteChannelRequest(message.chat))
        elif isinstance(message.chat, types.Chat):
            await self._client(messages.DeleteChatRequest(message.chat))
        else:
            return await utils.answer(message, self.strings["failed_to_delete"])
        return

    @loader.command(ru_doc="Очищает группу/канал от удаленных аккаунтов")
    @loader.tag("no_pm")
    async def flush(self, message):
        """Removes deleted accounts from the chat/channel"""
        chat = await message.get_chat()

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings["no_rights"])

        deleted = await self.xdlib.chat.get_deleted(chat)
        if not deleted:
            return await utils.answer(message, self.strings["no_deleted_accounts"])
        for to_delete in deleted:
            try:
                await self._client.kick_participant(chat, to_delete)
            except Exception as e:
                logger.error(str(e))
                return await utils.answer(message, self.strings["error"])
        return await utils.answer(message, self.strings["kicked_deleted_accounts"])

    @loader.command(ru_doc="Показывает админов в группе/канале")
    @loader.tag("no_pm")
    async def admins(self, message):
        """Shows the admins in the chat/channel"""
        admins = await self.xdlib.chat.get_admins(message.chat, True)
        creator = await self.xdlib.chat.get_creator(message.chat)
        return await utils.answer(
            message,
            self.strings["admin_list"].format(
                id=creator.id if creator else 0,
                name=creator.first_name if creator else self.strings["no"],
                admins_count=len(admins) or 0,
                admins=(
                    "\n".join(
                        f"<emoji document_id=5774022692642492953>✅</emoji> <a href='tg://user?id={admin.id}'>{admin.first_name}</a> [<code>{admin.id}</code>] / <code>{admin.participant.rank}</code>"
                        for admin in admins
                    )
                    if admins
                    else f"\n{self.strings['no_admins_in_chat']}"
                ),
            ),
        )

    @loader.command(ru_doc="Показывает забаненых участников в группе/канале")
    @loader.tag("no_pm")
    async def banlist(self, message):
        """Shows the banned participants in the chat/channel"""
        banned = await self._client.get_participants(
            message.chat_id, filter=types.ChannelParticipantsKicked("")
        )
        title = (await message.get_chat()).title
        banned_header = self.strings["banned_in_chat"].format(
            title=title, count=len(banned)
        )
        if len(banned) == 0:
            return await utils.answer(message, self.strings["no_banned_in_chat"])
        for user in banned:
            if not user.deleted:
                banned_header += f'<emoji document_id=5316712579467321913>🔴</emoji> <a href="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
        await utils.answer(
            message, f"<blockquote expandable><b>{banned_header}</b></blockquote>"
        )

    @loader.command(ru_doc="Показывает ботов в группе/канале")
    @loader.tag("no_pm")
    async def bots(self, message):
        """Shows the bots in the chat/channel"""
        bots = await self.xdlib.chat.get_bots(message.chat)
        if not bots:
            return await utils.answer(message, self.strings["no_bots_in_chat"])
        await utils.answer(
            message,
            self.strings["bot_list"].format(
                count=len(bots),
                bots="\n".join(
                    [
                        f"<emoji document_id=5774022692642492953>✅</emoji> <a href='tg://user?id={bot.id}'>{bot.first_name}</a> [<code>{bot.id}</code>]"
                        for bot in bots
                    ]
                ),
            ),
        )

    @loader.command(ru_doc="Показывает простых участников чата/канала")
    @loader.tag("no_pm")
    async def users(self, message):
        """Shows the users in the chat/channel"""
        users = await self.xdlib.chat.get_members(message.chat)
        if not users:
            return await utils.answer(message, self.strings["no_user_in_chat"])
        await utils.answer(
            message,
            self.strings["user_list"].format(
                count=len(users),
                users="\n".join(
                    [
                        f"<emoji document_id=5774022692642492953>✅</emoji> <a href='tg://user?id={user.id}'>{user.first_name}</a> [<code>{user.id}</code>]"
                        for user in users
                    ]
                ),
            ),
        )

    @loader.command(ru_doc="Забанить участника")
    @loader.tag("no_pm")
    async def ban(self, message):
        """Ban a participant temporarily or permanently"""
        text = message.text.split("\n", 1)
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        user = (
            next(iter(self.xdlib.parse.mentions(message)), None)
            or reply.sender_id
            or None
        )
        strings = []
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        if not user:
            return await utils.answer(message, self.strings["no_user"])

        seconds = self.xdlib.parse.time(utils.get_args_raw(message))
        until_date = datetime.now(timezone.utc) + timedelta(seconds=seconds)
        time_info = f" {self.xdlib.format.time(seconds)}" if seconds else None
        try:
            await self._client.edit_permissions(
                message.chat,
                user,
                until_date=until_date if seconds else None,
                view_messages=False,
            )
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        strings.append(
            self.strings["user_is_banned"].format(
                id=user.id,
                name=getattr(user, "first_name") or getattr(user, "title"),
                time_info=time_info or self.strings["forever"],
            )
        )

        if reason:
            strings.append(self.strings["reason"].format(reason=reason))
        return await utils.answer(message, "\n".join(strings))

    @loader.command(ru_doc="Разбанить пользователя")
    @loader.tag("no_pm")
    async def unban(self, message):
        """Unban a user"""
        reply = await message.get_reply_message()
        user = (
            next(iter(self.xdlib.parse.mentions(message)), None)
            or reply.sender_id
            or None
        )
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        try:
            await self._client.edit_permissions(message.chat, user, view_messages=True)
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        return await utils.answer(
            message,
            self.strings["user_is_unbanned"].format(
                id=user.id,
                name=getattr(user, "first_name") or getattr(user, "title"),
            ),
        )

    @loader.command(ru_doc="Кикнуть участника")
    @loader.tag("no_pm")
    async def kick(self, message):
        """Kick a participant"""
        text = message.text.split("\n", 1)
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        user = (
            next(iter(self.xdlib.parse.mentions(message)), None)
            or reply.sender_id
            or None
        )
        strings = []
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        try:
            await self._client.kick_participant(message.chat, user)
        except Exception as e:
            logging.error(str(e))
            return await utils.answer(message, self.strings["error"])
        strings.append(
            self.strings["user_is_kicked"].format(
                id=user.id,
                name=getattr(user, "first_name") or getattr(user, "title"),
            )
        )
        if reason:
            strings.append(self.strings["reason"].format(reason=reason))
        return await utils.answer(message, "\n".join(strings))

    @loader.command(ru_doc="Замутить участника")
    @loader.tag("no_pm")
    async def mute(self, message):
        """Mute a participant temporarily or permanently"""
        text = message.text.split("\n", 1)
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        user = (
            next(iter(self.xdlib.parse.mentions(message)), None)
            or reply.sender_id
            or None
        )
        strings = []
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        if not user:
            return await utils.answer(message, self.strings["no_user"])

        seconds = self.xdlib.parse.time(utils.get_args_raw(message))
        until_date = datetime.now(timezone.utc) + timedelta(seconds=seconds)
        time_info = f" {self.xdlib.format.time(seconds)}" if seconds else None
        try:
            await self._client.edit_permissions(
                message.chat,
                user,
                until_date=until_date if seconds else None,
                send_messages=False,
            )
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        strings.append(
            self.strings["user_is_muted"].format(
                id=user.id,
                name=getattr(user, "first_name") or getattr(user, "title"),
                time_info=time_info or self.strings["forever"],
            )
        )

        if reason:
            strings.append(self.strings["reason"].format(reason=reason))
        return await utils.answer(message, "\n".join(strings))

    @loader.command(ru_doc="Размутить участника")
    @loader.tag("no_pm")
    async def unmute(self, message):
        """Unmute a participant"""
        reply = await message.get_reply_message()
        user = (
            next(iter(self.xdlib.parse.mentions(message)), None)
            or reply.sender_id
            or None
        )
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        if not user:
            return await utils.answer(message, self.strings["no_user"])

        try:
            await self._client.edit_permissions(message.chat, user, send_messages=True)
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])
        return await utils.answer(
            message,
            self.strings["user_is_unmuted"].format(
                id=user.id,
                name=getattr(user, "first_name") or getattr(user, "title"),
            ),
        )

    @loader.command(ru_doc="Переименовать группу/канал")
    @loader.tag("no_pm")
    async def rename(self, message):
        """Rename the chat/channel"""
        chat = await message.get_chat()
        old_title = chat.title
        new_title = utils.get_args_raw(message)
        if message.is_channel:
            if message.is_group:
                type_of = self.strings["type_group"]
            else:
                type_of = self.strings["type_channel"]
            try:
                await self._client(
                    channels.EditTitleRequest(channel=chat, title=new_title)
                )
            except Exception as e:
                logger.error(str(e))
                return await utils.answer(message, self.strings["error"])
        else:
            type_of = self.strings["type_group"]
            try:
                await self._client(
                    messages.EditChatTitleRequest(chat_id=chat.id, title=new_title)
                )
            except Exception as e:
                logger.error(str(e))
                return await utils.answer(message, self.strings["error"])
        return await utils.answer(
            message,
            self.strings["title_changed"].format(
                old_title=old_title, new_title=new_title, type_of=type_of
            ),
        )

    @loader.command(
        ru_doc="[-g|--group name] [-c|--channel name] - Создать группу/канал"
    )
    async def create(self, message):
        """[-g|--group name] [-c|--channel name] - Create group/channel"""
        args = utils.get_args(message)
        opts = self.xdlib.parse.opts(args)
        group_name = opts.get("g") or opts.get("group")
        channel_name = opts.get("c") or opts.get("channel")
        if channel_name:
            result = await self._client(
                channels.CreateChannelRequest(
                    title=channel_name, broadcast=True, about=""
                )
            )
            chat = self.xdlib.chat.get_info(result.chats[0])
            return await utils.answer(
                message,
                self.strings["channel_created"].format(
                    link=chat.get("link"), title=channel_name
                ),
            )
        if group_name:
            result = await self._client(
                channels.CreateChannelRequest(
                    title=group_name, megagroup=True, about=""
                )
            )
            chat = await self.xdlib.chat.get_info(result.chats[0])
            return await utils.answer(
                message,
                self.strings["group_created"].format(
                    link=chat.get("link"), title=group_name
                ),
            )
        return await utils.answer(message, self.strings["invalid_args"])

    @loader.command(
        ru_doc="Отключает звук и архивирует чат",
    )
    async def dnd(self, message):
        """Mutes and archives the current chat"""
        dnd = await utils.dnd(self._client, await message.get_chat())
        if dnd:
            return await utils.answer(message, self.strings["dnd"])
        else:
            return await utils.answer(message, self.strings["dnd_failed"])

    @loader.command(ru_doc="Получить ссылку на сообщение")
    async def geturl(self, message):
        """Get the link to the replied messages"""
        if reply := await message.get_reply_message():
            link = await reply.link
            return await utils.answer(
                message, self.strings["msg_link"].format(link=link)
            )
        return await utils.answer(message, self.strings["msg_link_failed"])

    @loader.command(
        ru_doc="-u username/id - Пригласить пользователя в чат (-b пригласить инлайн бота)"
    )
    async def invite(self, message):
        """-u username/id - Invite a user to the chat (use -b to invite the inline bot)"""
        args = utils.get_args(message)
        opts = self.xdlib.parse.opts(args)
        if opts.get("b") or opts.get("bot"):
            invited = await self.xdlib.chat.invite_bot(self._client, message.chat)
            entity = await self._client.get_entity(self.inline.bot_id)
            if invited:
                return await utils.answer(
                    message,
                    self.strings["user_invited"].format(
                        user=entity.first_name, id=entity.id
                    ),
                )
            return await utils.answer(message, self.strings["user_not_invited"])
        reply = await message.get_reply_message()
        user = opts.get("u") or opts.get("user") or (reply.sender_id if reply else None)
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        entity = await self._client.get_entity(user)
        invited = await self.xdlib.chat.invite_user(message.chat, user)
        if invited:
            return await utils.answer(
                message,
                self.strings["user_invited"].format(
                    user=entity.first_name, id=entity.id
                ),
            )
        return await utils.answer(message, self.strings["user_not_invited"])

    @loader.command(ru_doc="-n название_роли -p число - Создать роль")
    async def addrole(self, message):
        """-n role_name -p number - Create a role"""
        args = utils.get_args(message)
        opts = self.xdlib.parse.opts(args)
        name = opts.get("name") or opts.get("n")
        perms = opts.get("perms") or opts.get("p")
        if not name:
            return await utils.answer(message, self.strings["invalid_args"])
        self._roles[name] = perms
        return await utils.answer(message, self.strings["role_created"])

    @loader.command(ru_doc="-n название_роли - Удалить роль")
    async def delrole(self, message):
        """-n role_name - Delete the role"""
        args = utils.get_args(message)
        opts = self.xdlib.parse.opts(args)
        name = opts.get("name") or opts.get("n")
        if not name:
            return await utils.answer(message, self.strings["invalid_args"])
        del self._roles[name]
        return await utils.answer(message, self.strings["role_removed"])

    @loader.command(
        ru_doc="<username/mention> [-h|--help] [-f|--fullrights] [-r|--rank rank] <right> - Назначить пользователя администратором"
    )
    @loader.tag("no_pm")
    async def setrights(self, message):
        """<username/mention> [-h|--help] [-f|--fullrights] [-r|--rank rank] <right> - Promote a participant"""
        opts = self.xdlib.parse.opts(utils.get_args(message))
        if opts.get("h") or opts.get("help"):
            return await utils.answer(
                message,
                f"<pre><code>{self.xdlib.rights.stringify_masks()}</code></pre>",
            )
        reply = await message.get_reply_message()
        user = opts.get("u") or opts.get("user") or (reply.sender_id if reply else None)
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        user = await self._client.get_entity(user)
        rank = opts.get("r") or opts.get("rank") or ("Admin" if not user.bot else "Bot")
        if opts.get("f") or opts.get("fullrights"):
            rights = self.xdlib.rights.all()
            rights.remove("anonymous")
            await self.xdlib.admin.set_rights(
                message.chat, user, rights.to_int(), rank=rank
            )
            return await utils.answer(
                message,
                self.strings["promoted"].format(id=user.id, name=user.first_name),
            )
        perms = opts.get("p") or opts.get("perms") or 0
        rights = self.xdlib.rights.from_int(perms)
        try:
            await self.xdlib.admin.set_rights(message.chat, user, rights.to_int(), rank)
            return await utils.answer(
                message,
                (
                    self.strings["promoted"].format(id=user.id, name=user.first_name)
                    if perms
                    else self.strings["demoted"].format(
                        id=user.id, name=user.first_name
                    )
                ),
            )
        except Exception as e:
            return await utils.answer(message, f"<code>{e}</code>")

    @loader.command(ru_doc="Показать все созданные роли")
    async def roles(self, message):
        """Get the created roles"""
        roles = self._roles
        args = utils.get_args(message)
        opts = self.xdlib.parse.opts(args)
        if not roles:
            return await utils.answer(message, self.strings["no_roles"])
        selected_role = opts.get("n") or opts.get("name")
        if not selected_role:
            return await utils.answer(
                message,
                self.strings["all_roles"].format(
                    roles="\n".join(
                        [
                            f"<emoji document_id=5807829874877930085>➡️</emoji> <code>{role}</code>"
                            for role in roles.keys()
                        ]
                    )
                ),
            )
        rights = []
        for right, permitted in (
            self.xdlib.rights.from_int(roles[selected_role]).to_dict().items()
        ):
            if permitted:
                rights.append(right)
                continue

        return await utils.answer(
            message,
            self.strings["role_info"].format(
                name=selected_role,
                rights=(
                    "\n".join(
                        [
                            f"<emoji document_id=5409029658794537988>✅</emoji> <code>{self.strings[right]}</code>"
                            for right in rights
                        ]
                    )
                    if rights
                    else self.strings["no_role_rights"]
                ),
            ),
        )

    @loader.command(ru_doc="-u username/id -n role -r rank - Назначить роль участнику")
    @loader.tag("no_pm")
    async def setrole(self, message):
        """-u username/id -n role -r rank - Set the role for the user"""
        args = utils.get_args(message)
        opts = self.xdlib.parse.opts(args)
        reply = await message.get_reply_message()
        user = opts.get("user") or opts.get("u") or getattr(reply, "sender_id")
        role = opts.get("name") or opts.get("n")
        if role not in self._roles:
            return await utils.answer(message, self.strings["invalid_args"])
        rank = opts.get("rank") or opts.get("r") or role
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        role_set = await self.xdlib.admin.set_rights(
            message.chat, user, self._roles[role], rank=rank
        )
        if not role_set:
            return await utils.answer(message, self.strings["role_not_set"])
        return await utils.answer(message, self.strings["role_set"])

    @loader.command(ru_doc="Получить инфу о текущем чате")
    @loader.tag("no_pm")
    async def chatinfo(self, message):
        """Get the current chat info"""
        try:
            chat = await message.get_chat()
            chatinfo = await self.xdlib.chat.get_info(chat)
            photo = chatinfo.get("chat_photo")
            photo = photo if not isinstance(photo, types.PhotoEmpty) else None
            return await utils.answer(
                message,
                self.strings["chatinfo"].format(
                    id=chatinfo.get("id"),
                    title=chatinfo.get("title"),
                    about=chatinfo.get("about") or self.strings["no"],
                    admins_count=chatinfo.get("admins_count"),
                    online_count=chatinfo.get("online_count"),
                    participants_count=chatinfo.get("participants_count"),
                    kicked_count=chatinfo.get("kicked_count"),
                    slowmode_seconds=(
                        self.xdlib.format.time(chatinfo.get("slowmode_seconds"))
                        if chatinfo.get("slowmode_seconds")
                        else self.strings["no"]
                    ),
                    call=(
                        self.strings["yes"]
                        if chatinfo.get("call")
                        else self.strings["no"]
                    ),
                    ttl_period=(
                        self.xdlib.format.time(chatinfo.get("ttl_period"))
                        if chatinfo.get("ttl_period")
                        else self.strings["no"]
                    ),
                    requests_pending=chatinfo.get("requests_pending"),
                    recent_requesters=", ".join(
                        [
                            f"<code>{user}</code>"
                            for user in chatinfo.get("recent_requesters")
                        ]
                    )
                    or self.strings["no"],
                    linked_chat_id=chatinfo.get("linked_chat_id") or self.strings["no"],
                    antispam=(
                        self.strings["yes"]
                        if chatinfo.get("antispam")
                        else self.strings["no"]
                    ),
                    participants_hidden=(
                        self.strings["yes"]
                        if chatinfo.get("participants_hidden")
                        else self.strings["no"]
                    ),
                    link=chatinfo.get("link") or self.strings["no"],
                    is_forum=(
                        self.strings["yes"]
                        if chatinfo.get("is_forum")
                        else self.strings["no"]
                    ),
                    type_of=(
                        self.strings["type_group"]
                        if chatinfo.get("is_group")
                        else (
                            self.strings["type_channel"]
                            if chatinfo.get("is_channel")
                            else self.strings["type_unknown"]
                        )
                    ),
                ),
                media=(
                    types.InputMediaPhoto(
                        types.InputPhoto(
                            photo.id, photo.access_hash, photo.file_reference
                        )
                    )
                    if photo
                    else None
                ),
            )
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(message, self.strings["error"])

    @loader.command(ru_doc="[-a] - Принять заявки на вступление")
    @loader.tag("no_pm")
    async def approve(self, message):
        """[-a] - Accept join requests"""
        opts = self.xdlib.parse.opts(utils.get_args(message))
        if opts.get("a"):
            await self.xdlib.chat.join_requests(message.chat, True)
            return await utils.answer(message, self.strings["all_approved"])
        args = utils.get_args(message)
        for arg in args:
            if arg.isdigit():
                await self.xdlib.chat.join_request(message.chat, int(arg), True)
            else:
                await self.xdlib.chat.join_request(message.chat, arg, True)
        return await utils.answer(message, self.strings["all_approved"])

    @loader.command(ru_doc="[-a] - Отклонить заявки на вступление")
    @loader.tag("no_pm")
    async def dismiss(self, message):
        """[-a] - Decline join requests"""
        opts = self.xdlib.parse.opts(utils.get_args(message))
        if opts.get("a"):
            await self.xdlib.chat.join_requests(message.chat, False)
            return await utils.answer(message, self.strings["all_dismissed"])
        args = utils.get_args(message)
        for arg in args:
            if arg.isdigit():
                await self.xdlib.chat.join_request(message.chat, int(arg), False)
            else:
                await self.xdlib.chat.join_request(message.chat, arg, False)
        return await utils.answer(message, self.strings["all_dismissed"])
