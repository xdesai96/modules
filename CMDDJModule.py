# meta developer: @xdesai & @devjmodules

import asyncio, os, requests
from .. import loader, security, utils
from datetime import timedelta, datetime
from ..inline.types import InlineCall # type: ignore
from telethon import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import ExportChatInviteRequest, DeleteChatUserRequest, CreateChatRequest, DeleteChatRequest, GetHistoryRequest, AddChatUserRequest, ImportChatInviteRequest, ExportChatInviteRequest
from hikkatl.tl.types import Message, Channel
from telethon.tl.functions.channels import GetFullChannelRequest, CreateChannelRequest, EditBannedRequest, EditTitleRequest, EditAdminRequest, JoinChannelRequest, DeleteChannelRequest, GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import *
from telethon import Button
from telethon.errors import *
from telethon.errors.rpcerrorlist import YouBlockedUserError

def get_creation_date(user_id: int) -> str:
    url = "https://restore-access.indream.app/regdate"
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
        "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
        "accept-language": "en-US,en;q=0.9",
    }
    data = {"telegramId": user_id}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200 and "data" in response.json():
        return response.json()["data"]["date"]
    else:
        return "Ошибка получения данных"

@loader.tds
class CMDDJ(loader.Module):
    """Модуль для админов чатов
    Made by Desai"""
    
    strings = {
        "name": "ChatModule",
        "loading": "🕐 <b>Обработка данных...</b>",
        "unblock_bot": "❗ Разблокируйте @funstat для получения дополнительной информации.",
        "not_a_chat": "<emoji document_id=5312526098750252863>❌</emoji> <b>The command cannot be run in private messages.</b>",
        "no_rights": "<emoji document_id=5318764049121420145>🫤</emoji> <b>I have no administrator rights or cannot promote" \
                     " and demote administrators.</b>",
        "no_user": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>You should specify an user.</b>",
        "demoted": "<emoji document_id=5458403743835889060>😂</emoji> <b>{name} was demoted to an regular user.</b>",
        "promoted_full": "<emoji document_id=5271557007009128936>👑</emoji> <b>{name} was promoted to an administrator" \
                        " with full rights.</b>\n<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank:</b> {rank}",
        "promoted": "<emoji document_id=5451786809845491357>🫣</emoji> <b>{name} was promoted to an administrator.</b>\n" \
                    "<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank:</b> {rank}",
        "choose_rights": "<emoji document_id=5271557007009128936>👑</emoji> <b>Choose administrator rights for {name}</b>" \
                         "\n<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank</b>: {rank}",
        "right_change_info": "{emoji} Change info {channel_or_chat}",
        "of_channel": "of channel", "of_chat": "of chat",
        "right_post_messages": "{emoji} Post messages",
        "right_edit_messages": "{emoji} Edit posts",
        "right_delete_messages": "{emoji} Delete messages",
        "right_ban_users": "{emoji} Restrict users",
        "right_invite_users": "{emoji} Invite users",
        "right_pin_messages": "{emoji} Pin messages",
        "right_add_admins": "{emoji} Promote administrators",
        "right_anonymous": "{emoji} Anonymous",
        "right_manage_call": "{emoji} Manage calls",
        "confirm": "✅ Confirm",
    }

    @loader.owner
    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.owner
    async def fullrightscmd(self, message: Message):
        """<user> [role (aka [prefix])] — Promote an user to administrator with full rights."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        rank, user_id = "Admin", None
        chat = await message.get_chat()
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id != message._client.tg_id:
                user_id = reply.sender_id
            if args:
                rank = args
        else:
            user_id = await utils.get_target(message)
            if len(args.split()) > 1:
                rank = " ".join(args.split()[1:])

        if (not chat.admin_rights or not chat.admin_rights.add_admins) and not chat.creator:
            return await utils.answer(message, self.strings("no_rights", message))
        if not user_id:
            return await utils.answer(
                message, self.strings("no_user", message)
            )

        user = await message.client.get_entity(
            user_id
        )
        try:
            await message.client(
                EditAdminRequest(
                    message.chat_id, user.id,
                    ChatAdminRights(
                        other=True,
                        change_info=True,
                        post_messages=True if chat.broadcast else None,
                        edit_messages=True if chat.broadcast else None,
                        delete_messages=True,
                        ban_users=True,
                        invite_users=True,
                        add_admins=True,
                        anonymous=None,
                        pin_messages=True if not chat.broadcast else None,
                        manage_call=True if not chat.broadcast else None
                    ),
                    rank
                )
            )
        except ChatAdminRequiredError:
            return await utils.answer(message, self.strings("no_rights", message))

        await utils.answer(
            message,
            self.strings("promoted_full", message).format(
                name=user.first_name,
                rank=rank
            )
        )

    @loader.owner
    async def promotecmd(self, message: Message):
        """<user> [role (aka [prefix])] — Promote an user to administrator."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        rank, user_id = "", None
        chat = await message.get_chat()
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id != message._client.tg_id:
                user_id = reply.sender_id
            if args:
                rank = args
        else:
            user_id = await utils.get_target(message)
            if len(args.split()) > 1:
                rank = " ".join(args.split()[1:])

        if (not chat.admin_rights or not chat.admin_rights.add_admins) and not chat.creator:
            return await utils.answer(message, self.strings("no_rights", message))
        if not user_id:
            return await utils.answer(
                message, self.strings("no_user", message)
            )

        user = await message.client.get_entity(
            user_id
        )

        rights = {
            "change_info": False,
            "post_messages": False,
            "edit_messages": False,
            "delete_messages": False,
            "ban_users": False,
            "invite_users": False,
            "pin_messages": False,
            "add_admins": False,
            "anonymous": False,
            "manage_call": False,
            "": False
        }

        markup = []
        reply_markup = []

        markup.append(
            {
                "text": self.strings('right_change_info').format(
                    emoji='✏',
                    channel_or_chat=self.strings('of_channel') if chat.broadcast else self.strings('of_chat')
                ),
                "callback": self._ch_rights,
                "args": [["change_info", True], rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings('right_delete_messages').format(
                    emoji='🗑'
                ),
                "callback": self._ch_rights,
                "args": [["delete_messages", True], rights, chat, rank, user]
            },
        )
        if chat.broadcast:
            markup.append(
                {
                    "text": self.strings('right_post_messages').format(
                        emoji='✉',
                    ),
                    "callback": self._ch_rights,
                    "args": [["post_messages", True], rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings('right_edit_messages').format(
                        emoji='✏',
                    ),
                    "callback": self._ch_rights,
                    "args": [["edit_messages", True], rights, chat, rank, user]
                },
            )
        markup.append(
            {
                "text": self.strings('right_ban_users').format(
                    emoji='⛔',
                ),
                "callback": self._ch_rights,
                "args": [["ban_users", True], rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings('right_pin_messages').format(
                    emoji='📌',
                ),
                "callback": self._ch_rights,
                "args": [["pin_messages", True], rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings('right_add_admins').format(
                    emoji='👑',
                ),
                "callback": self._ch_rights,
                "args": [["add_admins", True], rights, chat, rank, user]
            },
        )
        if not chat.broadcast:
            markup.append(
                {
                    "text": self.strings('right_manage_call').format(
                        emoji='📞'
                    ),
                    "callback": self._ch_rights,
                    "args": [["manage_call", True], rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings('right_invite_users').format(
                        emoji='➕',
                    ),
                    "callback": self._ch_rights,
                    "args": [["invite_users", True], rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings('right_anonymous').format(
                        emoji='🎭',
                    ),
                    "callback": self._ch_rights,
                    "args": [["anonymous", True], rights, chat, rank, user]
                },
            )

        kb = []
        for i in markup:
            if len(kb) == 2:
                reply_markup.append(kb)
                kb = []
            kb.append(i)
        if kb != [] and kb not in reply_markup:
            reply_markup.append(kb)

        reply_markup.append([
            {
                "text": self.strings("confirm"),
                "callback": self._inline_promote,
                "args": [rights, chat, rank, user]
            }
        ])


        await self.inline.form(
            message=message,
            text=self.strings("choose_rights").format(
                name=user.first_name,
                rank=rank
            ),
            silent=True,
            reply_markup=reply_markup
        )

    async def _inline_promote(self, call: InlineCall, all_rights: dict, chat, rank: str, user):
        try:
            await self.client(
                EditAdminRequest(
                    chat.id, user.id,
                    ChatAdminRights(
                        other=True,
                        change_info=all_rights.get('change_info'),
                        post_messages=all_rights.get('post_messages') if chat.broadcast else None,
                        edit_messages=all_rights.get('edit_messages') if chat.broadcast else None,
                        delete_messages=all_rights.get('delete_messages'),
                        ban_users=all_rights.get('ban_users'),
                        invite_users=all_rights.get('invite_users'),
                        add_admins=all_rights.get('add_admins'),
                        anonymous=all_rights.get('anonymous'),
                        pin_messages=all_rights.get('pin_messages') if not chat.broadcast else None,
                        manage_call=all_rights.get('manage_call') if not chat.broadcast else None,
                        manage_topics=all_rights.get('manage_topics') if not chat.broadcast else None
                    ),
                    rank
                )
            )
        except ChatAdminRequiredError:
            return await call.edit(
                text=self.strings("no_rights")
            )

        await call.edit(
            text=self.strings("promoted").format(
                name=user.first_name,
                rank=rank
            )
    )

    async def _ch_rights(self, call: InlineCall, right: str, all_rights: dict, chat, rank: str, user):
        all_rights[right[0]] = right[1]

        markup = []
        reply_markup = []

        markup.append(
            {
                "text": self.strings("right_change_info").format(
                    emoji='✏' if not all_rights.get('change_info', False) else '✅',
                    channel_or_chat=self.strings('of_channel') if chat.broadcast else self.strings('of_chat')
                ),
                "callback": self._ch_rights,
                "args": [["change_info", not all_rights.get("change_info")], all_rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings("right_delete_messages").format(
                    emoji='🗑' if not all_rights.get('delete_messages', False) else '✅'
                ),
                "callback": self._ch_rights,
                "args": [["delete_messages", not all_rights.get("delete_messages", False)], all_rights, chat, rank, user]
            },
        )
        if chat.broadcast:
            markup.append(
                {
                    "text": self.strings("right_post_messages").format(
                        emoji='✉' if not all_rights.get('post_messages', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["post_messages", not all_rights.get("post_messages", False)], all_rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings("right_edit_messages").format(
                        emoji='✏' if not all_rights.get('edit_messages', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["edit_messages", not all_rights.get("edit_messages", False)], all_rights, chat, rank, user]
                },
            )
        markup.append(
            {
                "text": self.strings("right_ban_users").format(
                    emoji='⛔' if not all_rights.get('ban_users', False) else '✅'
                ),
                "callback": self._ch_rights,
                "args": [["ban_users", not all_rights.get("ban_users", False)], all_rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings("right_pin_messages").format(
                    emoji='📌' if not all_rights.get('pin_messages', False) else '✅'
                ),
                "callback": self._ch_rights,
                "args": [["pin_messages", not all_rights.get("pin_messages", False)], all_rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings("right_add_admins").format(
                    emoji='👑' if not all_rights.get('add_admins', False) else '✅'
                ),
                "callback": self._ch_rights,
                "args": [["add_admins", not all_rights.get("add_admins", False)], all_rights, chat, rank, user]
            },
        )
        if not chat.broadcast:
            markup.append(
                {
                    "text": self.strings("right_manage_call").format(
                        emoji='📞' if not all_rights.get('manage_call', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["manage_call", not all_rights.get("manage_call", False)], all_rights, chat, rank, user]
                }
            )
            markup.append(
                {
                    "text": self.strings("right_invite_users").format(
                        emoji='➕' if not all_rights.get('invite_users', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["invite_users", not all_rights.get("invite_users", False)], all_rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings("right_anonymous").format(
                        emoji='🎭' if not all_rights.get('anonymous', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["anonymous", not all_rights.get("anonymous", False)], all_rights, chat, rank, user]
                },
            )

        kb = []
        for i in markup:
            if len(kb) == 2:
                reply_markup.append(kb)
                kb = []
            kb.append(i)
        if kb != [] and kb not in reply_markup:
            reply_markup.append(kb)

        reply_markup.append([
            {
                "text": self.strings("confirm"),
                "callback": self._inline_promote,
                "args": [all_rights, chat, rank, user]
            }
        ])

        await call.edit(
            text=self.strings("choose_rights").format(
                name=user.first_name,
                rank=rank
            ),
            reply_markup=reply_markup
        )

    @loader.owner
    async def demotecmd(self, message: Message):
        """<user> — Demote an administrator to a user."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        user_id = None
        chat = await message.get_chat()
        rank = ""
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id != message._client.tg_id:
                user_id = reply.sender_id
        else:
            user_id = await utils.get_target(message)

        if (not chat.admin_rights or not chat.admin_rights.add_admins) and not chat.creator:
            return await utils.answer(message, self.strings("no_rights", message))
        if not user_id:
            return await utils.answer(
                message, self.strings("no_user", message)
            )

        user = await message.client.get_entity(
            user_id
        )
        try:
            await message.client(
                EditAdminRequest(
                    message.chat_id, user.id,
                    ChatAdminRights(
                        other=False,
                        change_info=None,
                        post_messages=None,
                        edit_messages=None,
                        delete_messages=None,
                        ban_users=None,
                        invite_users=None,
                        pin_messages=None,
                        add_admins=None,
                        anonymous=None,
                        manage_call=None,
                        manage_topics=None
                    ),
                    rank
                )
            )
        except ChatAdminRequiredError:
            return await utils.answer(message, self.strings("no_rights", message))

        await utils.answer(
            message, self.strings("demoted", message).format(
                name=user.first_name
            )
        )

    @loader.owner
    async def userinfocmd(self, message: Message):
        """Получить информацию о пользователе или канале. Использование: .userinfo <@юзернейм/ID> или ответ на сообщение"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        await utils.answer(message, self.strings("loading"))

        try:
            entity = (
                (await self._client.get_entity(args if not args.isdigit() else int(args)))
                if args
                else await self._client.get_entity(reply.sender_id)
            )
        except Exception:
            await utils.answer(message, "❗ Не удалось найти пользователя или канал. Проверьте правильность ID или юзернейма.")
            return

        if isinstance(entity, Channel):
            await self.process_channel_info(entity, message)
        else:
            await self.process_user_info(entity, message)

    async def process_user_info(self, user_ent, message):
        """Обработка информации о пользователе"""
        user = await self._client(GetFullUserRequest(user_ent.id))
        registration_date = get_creation_date(user_ent.id)
        funstat_info = await self.get_funstat_info(user_ent.id)

        user_info = (
            "<b>👤 Информация о пользователе:</b>\n\n"
            f"<b>Имя:</b> <code>{user_ent.first_name or '🚫'}</code>\n"
            f"<b>Фамилия:</b> <code>{user_ent.last_name or '🚫'}</code>\n"
            f"<b>Юзернейм:</b> @{user_ent.username or '🚫'}\n"
            f"<b>Описание:</b>\n{user.full_user.about or '🚫'}\n\n"
            f"<b>Дата регистрации:</b> <code>{registration_date}</code>\n"
            f"<b>Общие чаты:</b> <code>{user.full_user.common_chats_count}</code>\n"
            f"<b>ID:</b> <code>{user_ent.id}</code>\n"
        )

        if user_ent.username:
            user_info += f'<b><a href="tg://user?id={user_ent.id}">🌐 Вечная ссылка</a></b>\n\n'
        else:
            user_info += "Вечная ссылка отсутствует.\n\n"

        user_info += f"{funstat_info}"

        photo = await self._client.download_profile_photo(user_ent.id)

        if photo:
            await self._client.send_file(
                message.chat_id,
                file=photo,
                caption=user_info,
                buttons=[
                    [Button.inline("🔄 Обновить данные", data=f"refresh:{user_ent.id}")]
                ]
            )
        else:
            await self._client.send_message(message.chat_id, user_info)

        await message.delete()

    async def process_channel_info(self, channel_ent, message):
        """Обработка информации о канале"""
        channel = await self._client(GetFullChannelRequest(channel_ent))
        description = channel.full_chat.about or "🚫"
        creation_date = get_creation_date(channel_ent.id)
        subscriber_count = channel.full_chat.participants_count

        channel_info = (
            "<b>📣 Информация о канале:</b>\n\n"
            f"<b>Название:</b> <code>{channel_ent.title}</code>\n"
            f"<b>Юзернейм:</b> @{channel_ent.username or '🚫'}\n"
            f"<b>Описание:</b>\n{description}\n\n"
            f"<b>Дата создания:</b> <code>{creation_date}</code>\n"
            f"<b>Количество подписчиков:</b> <code>{subscriber_count}</code>\n"
            f"<b>ID:</b> <code>{channel_ent.id}</code>\n"
        )

        if channel_ent.username:
            channel_info += f'<b><a href="https://t.me/{channel_ent.username}">Ссылка на канал</a></b>\n\n'
        else:
            channel_info += "Ссылка на канал отсутствует.\n\n"

        photo = await self._client.download_profile_photo(channel_ent.id)

        if photo:
            await self._client.send_file(
                message.chat_id,
                file=photo,
                caption=channel_info,
                buttons=[
                    [Button.inline("🔄 Обновить данные", data=f"refresh:{channel_ent.id}")]
                ]
            )
        else:
            await self._client.send_message(message.chat_id, channel_info)

        await message.delete()

    async def get_funstat_info(self, user_id: int) -> str:
        """Отправка запроса в @funstat и получение информации"""
        chat = "@Suusbdj_bot"
        attempts = 3
        for attempt in range(attempts):
            try:
                await self._client.send_message(chat, str(user_id))

                await asyncio.sleep(5)

                messages = await self._client.get_messages(chat, limit=5)

                for message in messages:
                    if f"👤 {user_id}" in message.text or str(user_id) in message.text:
                        lines = message.text.split("\n")
                        filtered_lines = [
                            line for line in lines if "ID:" not in line and "Это" not in line
                        ]
                        return "\n".join(filtered_lines)

                await asyncio.sleep(1)

            except YouBlockedUserError:
                return self.strings("unblock_bot")
            except Exception as e:
                return f"Ошибка при получении данных: {e}"

        return "⚠️ Не удалось получить окончательный ответ от @funstat_obot."

    @loader.owner
    async def createcmd(self, message):
        """Используй .create <g|s|c> <название>, чтобы создать группу, супергруппу или канал."""
        args = utils.get_args_raw(message).split(" ")
        try:
            title = utils.get_args_raw(message).split(" ", 1)[1]
            if "g" in args[0]:
                r = await message.client(
                    CreateChatRequest(users=["missrose_bot"], title=title)
                )
                created_chat = r.chats[0].id
                await message.client(
                    DeleteChatUserRequest(chat_id=created_chat, user_id="@missrose_bot")
                )
            elif "s" in args[0]:
                r = await message.client(
                    CreateChannelRequest(title=title, about="", megagroup=True)
                )
            elif "c" in args[0]:
                r = await message.client(
                    CreateChannelRequest(title=title, about="", megagroup=False)
                )
            created_chat = r.chats[0].id
            result = await message.client(ExportChatInviteRequest(peer=created_chat))
            await message.edit(
                f'<b>Группа "{title}" создана.\nЛинк: {result.link}.</b>'
            )
        except IndexError:
            return await message.edit("<b>Неверно указаны аргументы.</b>")
        except UnboundLocalError:
            return await message.edit("<b>Неверно указаны аргументы.</b>")
        except UserRestrictedError:
            return await message.edit(
                "<b>У вас спамбан, вы не можете создавать каналы или группы.</b>"
            )

    @loader.owner
    async def useridcmd(self, message):
        """[reply] | Get User ID"""
        reply = await message.get_reply_message()
        if reply != None:
            await utils.answer(message, f"<emoji document_id=5436024756610546212>⚡</emoji> <b>User ID</b>: <code>{reply.sender_id}</code>")
        else:
            await utils.answer(message, self.strings["Error_reply"])

    @loader.owner
    async def idcmd(self, message):
        """| Get your ID"""
        await utils.answer(message, f"<emoji document_id=5436024756610546212>⚡</emoji> <b>Your ID</b>: <code>{message.sender_id}</code>")

    @loader.owner
    async def chatidcmd(self, message):
        """| Get chat ID"""
        await utils.answer(message, f"<emoji document_id=5436024756610546212>⚡</emoji> <b>Chat ID</b>: <code>{message.peer_id.channel_id}</code>")

    @loader.owner
    async def delcmd(self, event):
        """Удаляет сообщение. Использование: ?del <reply>"""
        reply = await event.get_reply_message()
        if not reply:
            await event.edit("Ответь на сообщение которое надо удалить.")
            return await event.delete()
        try:
            await reply.delete()
            await event.delete()
        except Exception:
            pass

    @loader.owner
    async def dgccmd(self, event):
        """Удаляет группу/канал по ссылке или ID. Использование: .dgc <ID или ссылка>"""
        args = utils.get_args(event)
        if not args:
            await event.edit("❌ Укажите ID или ссылку на группу/канал.")
            return
        
        link = args[0] if isinstance(args, list) else args
        try:
            if link.isdigit():
                chat_id = int(link)
            elif "t.me" in link or "tg://" in link:
                chat_id = await event.client.get_entity(link)
                chat_id = chat_id.id
            else:
                await event.edit("❌ Некорректный формат. Используйте ссылку или числовой ID.")
                return
            try:
                await event.client(DeleteChannelRequest(chat_id))
                chat_type = "Супергруппа/Канал"
            except Exception:
                await event.client(DeleteChatRequest(chat_id))
                chat_type = "Обычная группа"

            await event.edit(f"✅ Группа/канал ({chat_type}) успешно удалена.")
            await event.delete()

        except ChatAdminRequiredError:
            await event.edit("❌ У вас недостаточно прав для удаления этой группы/канала.")
        except ChannelPrivateError:
            await event.edit("❌ Чат недоступен или приватный.")
        except RpcError as e:
            await event.edit(f"❌ Ошибка RPC: {e}")
        except Exception as e:
            await event.edit(f"❌ Произошла ошибка: {e}")

    @loader.owner
    async def joincmd(self, event):
        """Вступает в группу или канал по ссылке."""

        link = utils.get_args_raw(event)
        if not link:
            await event.edit("Укажите ссылку на группу или канал.")
            return

        link = link.strip()
        try:
            if "joinchat" in link or "+" in link:
                invite_hash = link.split("/")[-1].replace("joinchat/", "").replace("+", "")
                await self.client(ImportChatInviteRequest(invite_hash))
                await event.edit(f"Успешно вступили в приватный чат по ссылке: {link}.")
            else:
                entity = await self.client.get_entity(link)
                await self.client(JoinChannelRequest(entity))
                title = entity.title if hasattr(entity, 'title') else "Нет названия"
                await event.edit(f"Успешно вступили в публичный чат: {title}.")
        except InviteHashExpiredError:
            await event.edit("Срок действия ссылки истек!")
        except ValueError:
            await event.edit("Неверная ссылка. Проверьте корректность.")
        except Exception as e:
            await event.edit(f"Ошибка: {str(e)}")

    @loader.owner
    async def whoisownercmd(self, event):
        """Определяет владельца группы или канала."""
        chat = await event.get_input_chat()

        try:
            participants = await self.client.get_participants(chat, filter=ChannelParticipantsAdmins, aggressive=True)
            for admin in participants:
                if isinstance(admin.participant, ChannelParticipantCreator):
                    owner_name = f"{admin.first_name} {admin.last_name or ''}".strip()
                    owner_id = admin.id
                    await event.edit(f"Владелец:\n<a href='tg://user?id={owner_id}'>{owner_name}</a>")
                    return
            await event.edit("Владелец не найден.")
        except Exception as e:
            await event.edit(f"Ошибка: {str(e)}")

    @loader.owner
    async def renamecmd(self, message):
        """.rename <new_name> — Меняет название группы/канала на <new_name>"""
        try:
            args = utils.get_args(message)
            if not args:
                await message.edit("Укажите новое название для группы/канала.")
                return

            new_name = " ".join(args)
            
            chat = await message.get_chat()

            if not chat.admin_rights and not chat.creator:
                await message.edit("Вы не являетесь администратором этой группы/канала.")
                return

            await self._client(EditTitleRequest(
                channel=chat,
                title=new_name
            ))

            await message.edit(f"Название изменено на: {new_name}")
            await message.delete()
        except Exception as e:
            await message.edit(f"Ошибка: {str(e)}")

    @loader.owner
    async def memberscmd(self, event):
        """Показывает кол-во участников канала/группы"""
        if not event.is_private:
            chat = await event.get_input_chat()
            try:
                members = await event.client.get_participants(chat)
                real_members = [member for member in members if not member.bot]
                count = len(real_members)
                await event.edit(f"Количество участников (без ботов) в чате: {count}")
            except Exception as e:
                await event.edit(f"Ошибка при подсчете участников: {e}")
        else:
            return await event.edit("<b>Братан, это не чат!</b>")

    @loader.owner
    async def chatinfocmd(self, chatinfo):
        """Используй .chatinfo <айди чата>; ничего"""
        if chatinfo.chat:
            await chatinfo.edit("<b>Загрузка информации...</b>")
            await chatinfo.delete()
            chat = await get_chatinfo(chatinfo)
            caption = await fetch_info(chat, chatinfo)
            try:
                await chatinfo.client.send_message(
                    chatinfo.to_id,
                    str(caption),
                    file=await chatinfo.client.download_profile_photo(
                        chat.full_chat.id, "chatphoto.jpg"
                    ),
                )
            except Exception:
                await chatinfo.edit(f"<b>Произошла непредвиденная ошибка.</b>")
                await chatinfo.delete()
        else:
            await chatinfo.edit("<b>Братан, это не чат!</b>")
            await chatinfo.delete()

    @loader.owner
    async def owncmd(self, message):
        """Выводит список чатов, каналов и групп где вы владелец."""
        await message.edit("<b>Считаем...</b>")
        
        count = 0
        msg = ""

        async for dialog in message.client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                chat = await message.client.get_entity(dialog.id)
                if chat.admin_rights or chat.creator:
                    count += 1
                    chat_type = "Группа" if dialog.is_group else "Канал"
                    msg += f'\n• {chat.title} <b>({chat_type})</b> | <code>{chat.id}</code>'

        if msg:
            await message.edit(f"<b>Мои владения: {count}</b>\n{msg}", parse_mode="html")
        else:
            await message.edit("<b>Нет владений, где вы являетесь администратором.</b>")

    @loader.owner
    async def unmutecmd(self, message):
        """Размучивает пользователя. Использование: .unmute <id>"""
        if not message.is_reply:
            try:
                args = message.raw_text.split(maxsplit=1)
                if len(args) < 2:
                    await message.edit("Укажите ID пользователя после команды.")
                    return
                
                user_id = int(args[1])
                user = await message.client.get_entity(user_id)
                first_name = user.first_name or "Неизвестный"
                
                await message.client.edit_permissions(
                    entity=message.chat_id,
                    user=user_id,
                    send_messages=True,
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    send_polls=True
                )
                
                await message.edit(
                    f"Пользователь <a href='tg://user?id={user_id}'>{first_name}</a> был размучен. Он может снова отправлять сообщения.",
                    parse_mode="html"
                )
            except ValueError:
                await message.edit("Укажите корректный ID пользователя.")
            except Exception as e:
                await message.edit(f"Произошла ошибка: {e}")
        reply_message = await message.get_reply_message()
        user_id = reply_message.sender_id
        first_name = reply_message.sender.first_name
        try:
            await message.client.edit_permissions(
                entity = message.chat_id,
                user = user_id,
                send_messages = True,
                send_media = True,
                send_stickers = True,
                send_gifs = True,
                send_games = True,
                send_inline = True,
                send_polls = True
            )
            await message.client.send_message(
                    message.chat_id,
                    f"Пользователь <a href='tg://user?id={user_id}'>{first_name}</a> был размучен. Он может снова отправлять сообщения.",
                    reply_to=reply_message.id
                )
            await message.delete()
        except UserAdminInvalidError:
            await message.edit("Я не могу замутить администратора.")
            await message.delete()
        except ChatAdminRequiredError:
            await message.edit("У меня нет прав администратора для выполнения этой команды.")
            await message.delete()
        except Exception as e:
            await message.edit(f"Ошибка: {e}")
            await message.delete()

    @loader.owner
    async def mutecmd(self, message):
        """Мут пользователя. Использование: .mute <reply | ID | username> <time> - мутит на определенное время (в минутах)."""
        args = message.raw_text.split(maxsplit=2)

        if len(args) < 2:
            await message.edit("Использование: .mute <reply | ID | username> <time> - мутит на определенное время (в минутах).")
            await message.delete()
            return
        try:
            mute_time = int(args[-1])
            duration = timedelta(minutes=mute_time)
        except ValueError:
            await message.edit("Укажите корректное время мута (в минутах).")
            await message.delete()
            return

        user_id = None
        first_name = "пользователь"

        if message.is_reply:
            reply_message = await message.get_reply_message()
            user_id = reply_message.sender_id
            first_name = reply_message.sender.first_name
        elif len(args) == 3:
            user_identifier = args[1]
            try:
                user = await message.client.get_entity(user_identifier)
                user_id = user.id
                first_name = user.first_name
            except Exception:
                await message.edit("Не удалось найти пользователя по ID или username.")
                await message.delete()
                return
        else:
            await message.edit("Ответьте на сообщение пользователя или укажите его ID/username.")
            await message.delete()
            return

        try:
            await message.client.edit_permissions(
                entity=message.chat_id,
                user=user_id,
                send_messages=False,
                send_media=False,
                send_stickers=False,
                send_gifs=False,
                send_games=False,
                send_inline=False,
                send_polls=False,
                until_date=duration
            )

            await message.edit(
                f"Пользователь <a href='tg://user?id={user_id}'>{first_name}</a> замучен на {mute_time} минут.",
                parse_mode="html"
            )

            await asyncio.sleep(duration.total_seconds())

            await message.client.send_message(
                message.chat_id,
                f"Время мута пользователя <a href='tg://user?id={user_id}'>{first_name}</a> завершилось. Он может снова отправлять сообщения.",
                parse_mode="html"
            )

        except UserAdminInvalidError:
            await message.edit("Я не могу замутить администратора.")
            await message.delete()
        except ChatAdminRequiredError:
            await message.edit("У меня нет прав администратора для выполнения этой команды.")
            await message.delete()
        except Exception as e:
            await message.edit(f"Ошибка: {e}")
            await message.delete()

    @loader.owner
    async def kickallcmd(self, event):
        """Удаляет всех пользователей из чата."""
        user = [i async for i in event.client.iter_participants(event.to_id.channel_id)]
        await event.edit(
            f"<b>{len(user)} пользователей будет кикнуто из чата"
            f" {event.to_id.channel_id}</b>"
        )
        await event.delete()
        for u in user:
            try:
                try:
                    if u.is_self != True:
                        await event.client.kick_participant(event.chat_id, u.id)
                    else:
                        pass
                except:
                    pass
            except FloodWaitError as e:
                print("Flood for", e.seconds)

    @loader.owner
    async def stealcmd(self, event):
        """Добавляет людей и ботов с чата в чат. Если дописать аргумент nobot то без ботов"""
        if len(event.text.split()) >= 2:
            print("Started!")
            idschannelgroup = int(event.text.split(" ", maxsplit=2)[1])
            arg = event.text.split(" ", maxsplit=2)[2] if len(event.text.split()) > 2 else None
            entity = await event.client.get_entity(idschannelgroup)
            participants = await event.client(GetParticipantsRequest(
                                        channel=idschannelgroup,
                                        filter=ChannelParticipantsSearch(''),
                                        offset=0,
                                        limit=0,
                                        hash=0
                                    ))
            existing_users = {p.id for p in participants.users}
            if arg and arg == "nobot":
                user = [
                    i async for i in event.client.iter_participants(event.to_id.channel_id)
                    if not i.bot
                ]
            else:
                user = [
                    i async for i in event.client.iter_participants(event.to_id.channel_id)
                ]
            await event.edit(
                f"<b>({len(user)})просто прикол)</b>"
            )
            await event.delete()
            try:
                if entity.broadcast or entity.megagroup:
                    for u in user:
                        try:
                            if isinstance(u, PeerUser):
                                u = await event.client.get_entity(u.user_id)
                            if u.id not in existing_users:
                                await event.client(functions.channels.InviteToChannelRequest(
                                    channel=idschannelgroup,
                                    users=[u.id]
                                ))
                        except FloodWaitError as e:
                            await asyncio.sleep(e.seconds)
                        except Exception as e:
                            if "Too many requests" in str(e):
                                print("Stopped!")
                                return
                            print(f"{str(e)}")
                        await asyncio.sleep(2)
                else:
                    for u in user:
                        try:
                            if isinstance(u, PeerUser):
                                u = await event.client.get_entity(u.user_id)
                            if u.id not in existing_users:
                                await event.client(functions.channels.AddChatUserRequest(
                                    chat_id=idschannelgroup, 
                                    users=[u.id],
                                    fwd_limit=0
                                ))
                        except FloodWaitError as e:
                            await asyncio.sleep(e.seconds)
                        except Exception as e:
                            if "Too many requests" in str(e):
                                print("Stopped!")
                                return
                            print(f"{str(e)}")
                        await asyncio.sleep(2)
            except UsersTooMuchError:
                print("The maximum number of users has been exceeded")
                print("Stopped!")
                return
        else:
            await event.edit(f"<b>Куда приглашать будем?</b>")
        print("Stopped!")

    @loader.owner
    async def userscmd(self, message):
        """Выводит список участников."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "этом чате"
            users = await message.client.get_participants(message.chat_id)
            mentions = ""
            user_mentions = []
            for user in users:
                if not user.bot:
                    if not user.deleted:
                        user_mentions.append(f"\n• <a href =\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>")
                    else:
                        user_mentions.append(f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>")

            if user_mentions:
                mentions += ''.join(user_mentions)
            else:
                mentions += "\n<b>Пользователи не найдены.</b>"

            try:
                await message.edit(mentions)
                return
            except MessageTooLongError:
                await message.edit("<b>Черт, слишком большой чат. Загружаю список пользователей в файл...</b>")
                file = open("userslist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "userslist.md",
                                               caption="<b>Пользователей в {}:</b>".format(title),
                                               reply_to=message.id)
                os.remove("userslist.md")
                await message.delete()
                return
        else:
            return await message.edit("<b>Братан, это не чат!</b>")

    @loader.owner
    async def adminscmd(self, message):
        """Выводит список всех админов в чате (без учёта ботов)."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "this chat"

            admins = await message.client.get_participants(message.chat_id, filter=ChannelParticipantsAdmins)
            real_members = [member for member in admins if not member.bot]
            mentions = f"<b>Админов в \"{title}\": {len(real_members)}</b>\n"

            for user in real_members:
                if not user.deleted:
                    mentions += f"\n• <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>"
                else:
                    mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>"

            try:
                await message.edit(mentions)
            except MessageTooLongError:
                await message.edit("Черт, слишком много админов здесь. Загружаю список админов в файл...")
                with open("adminlist.md", "w+") as file:
                    file.write(mentions)
                await message.client.send_file(message.chat_id,
                                            "adminlist.md",
                                            caption="<b>Админов в \"{}\":</b>".format(title),
                                            reply_to=message.id)
                os.remove("adminlist.md")
                await message.delete()
        else:
            return await message.edit("<b>Братан, это не чат!</b>")

    @loader.owner
    async def botscmd(self, message):
        """Выводит список всех ботов в чате."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")

            info = await message.client.get_entity(message.chat_id)
            title = info.title if info.title else "this chat"

            bots = await message.client.get_participants(message.to_id, filter=ChannelParticipantsBots)
            mentions = f"<b>Ботов в \"{title}\": {len(bots)}</b>\n"

            for user in bots:
                if not user.deleted:
                    mentions += f"\n• <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>"
                else:
                    mentions += f"\n• Удалённый бот <b>|</b> <code>{user.id}</code>"

            try:
                await message.edit(mentions, parse_mode="html")
            except MessageTooLongError:
                await message.edit("Черт, слишком много ботов здесь. Загружаю список ботов в файл...")
                file = open("botlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "botlist.md",
                                               caption="<b>Ботов в \"{}\":</b>".format(title),
                                               reply_to=message.id)
                os.remove("botlist.md")
                await message.delete()
        else:
            return await message.edit("<b>Братан, это не чат!</b>")

    @loader.owner
    async def unbancmd(self, message):
        """Разбанить участника. Использование: .ban <reply/id>"""
        if not isinstance(message.to_id, PeerChannel):
            return await utils.answer(message, "Братан, это не чат!")
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, "Никто не разбанен")
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, "Кого разбанить?")
        try:
            await self.client(EditBannedRequest(message.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=False)))
            await message.delete()
            return
        except BadRequestError:
            await utils.answer(message, "Я не админ...")
            await message.delete()
            return

    @loader.owner
    async def bancmd(self, message):
        """Забанить участника. Использование: .ban <reply/id>"""
        if not isinstance(message.to_id, PeerChannel):
            return await utils.answer(message, "Братан, это не чат!")
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, "Никто не забанен")
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, "Кого банить?")
        try:
            await self.client(EditBannedRequest(message.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=True)))
            await message.delete()
            return
        except BadRequestError:
            await utils.answer(message, "Я не админ...")
            await message.delete()
            return

    @loader.owner
    async def kickcmd(self, message):
        """Кикнуть участника из чата. Использование: .kick <reply/id>"""
        if isinstance(message.to_id, PeerUser):
            return await utils.answer(message, "Это не группа!")
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, "Никто не кикнут")
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, "Кого кикать?")
        if user.is_self:
            if not (await message.client.is_bot()
                    or await self.allmodules.check_security(message, security.OWNER | security.SUDO)):
                return
        try:
            await self.client.kick_participant(message.chat_id, user.id)
            await message.delete()
            return
        except BadRequestError:
            await utils.answer(message, "Я не админ...")
            await message.delete()
            return

    @loader.owner
    async def invitecmd(self, message):
        """Пригласить пользователя/бота в чат. Использование: .invite <id/reply>."""
        if message.is_private:
            return await message.edit("<b>Братан, это не чат!</b>")

        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        if not args and not reply:
            await message.edit("<b>Нет аргументов или реплая.</b>")
            await message.delete()
            return

        try:
            entity = await message.client.get_entity(message.chat_id)
            if args:
                user = args if not args.isdigit() else int(args)
            else:
                user = reply.sender_id
            
            user = await message.client.get_entity(user)

            if message.is_group and not entity.megagroup:
                await message.client(AddChatUserRequest(chat_id=message.chat_id,
                                                        user_id=user.id,
                                                        fwd_limit=1000000))
            elif entity.broadcast or entity.megagroup:
                await message.client(functions.channels.InviteToChannelRequest(
                                channel=message.chat_id,
                                users=[user.id]
                            ))
            else:
                await message.edit("Не удалось определить тип чата.")
            await message.edit("<b>Пользователь приглашён успешно!</b>")
            await message.delete()
            return

        except ValueError:
            m = "<b>Неверный @ или ID.</b>"
        except UserIdInvalidError:
            m = "<b>Неверный @ или ID.</b>"
        except UserPrivacyRestrictedError:
            m = "<b>Настройки приватности пользователя не позволяют пригласить его.</b>"
        except UserNotMutualContactError:
            m = "<b>Настройки приватности пользователя не позволяют пригласить его.</b>"
        except ChatAdminRequiredError:
            m = "<b>У меня нет прав.</b>"
        except UserBotError:
            group = await message.client.get_entity(message.chat_id)
            if args:
                user = args if not args.isdigit() else int(args)
            else:
                user = reply.sender_id
            user = await message.client.get_entity(user)
            admin_rights = ChatAdminRights(
                change_info=True,
                delete_messages=True,
                ban_users=True,
                invite_users=True,
                pin_messages=True,
                add_admins=False
            )
            await self.client(EditAdminRequest(
                channel=group,
                user_id=user,
                admin_rights=admin_rights,
                rank='admin'
            ))
        except ChatWriteForbiddenError:
            m = "<b>У меня нет прав.</b>"
        except ChannelPrivateError:
            m = "<b>У меня нет прав.</b>"
        except UserKickedError:
            m = "<b>Пользователь кикнут из чата, обратитесь к администраторам.</b>"
        except BotGroupsBlockedError:
            m = "<b>Бот заблокирован в чате, обратитесь к администраторам.</b>"
        except UserBlockedError:
            m = "<b>Пользователь заблокирован в чате, обратитесь к администраторам.</b>"
        except InputUserDeactivatedError:
            m = "<b>Аккаунт пользователя удалён.</b>"
        except UserAlreadyParticipantError:
            m = "<b>Пользователь уже в группе.</b>"
        except YouBlockedUserError:
            m = "<b>Вы заблокировали этого пользователя.</b>"
        await message.edit(m)
        await message.delete()
        return

    @loader.owner
    async def flushcmd(self, message: Message):
        """Удаляет удалённые аккаунты из чата"""
        chat = await message.get_chat()

        if isinstance(chat, User):
            await utils.answer(message, "<emoji document_id=5787313834012184077>😀</emoji> <b>Эта команда предназначена только для групп</b>")
            await message.delete()
            return

        if not chat.admin_rights and not chat.creator:
            await utils.answer(message, "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Недостаточно прав для выполнения этой команды.</b>")
            await message.delete()
            return

        removed_count = 0
        
        edit_message = await utils.answer(message, "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск удалённых аккаунтов</b>")
        if not edit_message:
            edit_message = message

        async for user in self._client.iter_participants(chat):
            if user.deleted:
                try:
                    await self._client.kick_participant(chat, user)
                    removed_count += 1
                except ChatAdminRequiredError:
                    await utils.answer(message, "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Для выполнения команды необходимы права администратора</b>")
                    await message.delete()
                    return
                except Exception as e:
                    await utils.answer(message, f"<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Ошибка при удалении аккаунта {user.id}: {str(e)}</b>")
                    await message.delete()

        if removed_count == 0:
            await edit_message.edit("<emoji document_id=5341509066344637610>😎</emoji> <b>Здесь нет ни одного удалённого аккаунта</b>")
            await message.delete()
        else:
            await edit_message.edit(f"<emoji document_id=5328302454226298081>🫥</emoji> <b>Удалено {removed_count} удалённых аккаунтов</b>")

    @loader.owner
    async def wipecmd(self, message):
        """Удаляет все сообщения от тебя без вопросов"""
        chat = message.chat
        if chat:
            async for msg in message.client.iter_messages(chat, from_user="me"):
                await msg.delete()
        else:
            await message.edit("<b>В лс не чищу!</b>")

    @loader.owner
    async def _is_owner(self, chat_id):
        """Проверяет, является ли пользователь владельцем группы."""
        permissions = await self.client.get_permissions(chat_id, 'me')
        return permissions.is_creator

async def get_chatinfo(event):
    chat = utils.get_args_raw(event)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChannelRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            return None
        except ChannelPrivateError:
            return None
        except ChannelPublicGroupNaError:
            return None
        except:
            chat = event.input_chat
            chat_info = await event.client(GetFullChannelRequest(chat))
            return chat_info
    return chat_info


async def fetch_info(chat, event):
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    chat_title = chat_obj_info.title
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception:
        msg_info = None
        await event.edit("<b>Произошла непредвиденная ошибка.</b>")
        await event.delete()
    first_msg_valid = (
        True
        if msg_info and msg_info.messages and msg_info.messages[0].id == 1
        else False
    )
    creator_valid = True if first_msg_valid and msg_info.users else False
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Удалённый аккаунт"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and type(msg_info.messages[0].action) is MessageActionChannelMigrateFrom
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    users_online = 0
    async for i in event.client.iter_participants(event.chat_id):
        if isinstance(i.status, UserStatusOnline):
            users_online = users_online + 1
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info
    bots = 0
    slowmode = (
        "Да"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "Нет"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "Да"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "Нет"
    )
    verified = (
        "Да" if hasattr(chat_obj_info, "verified") and chat_obj_info.verified else "Нет"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None

    if admins is None:
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception:
            await event.edit("<b>Произошла непредвиденная ошибка.</b>")
            await event.delete()
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "<b>ИНФОРМАЦИЯ О ЧАТЕ:</b>\n\n"
    caption += f"<b>ID:</b> {chat_obj_info.id}\n"
    if chat_title is not None:
        caption += f"<b>Название группы:</b> {chat_title}\n"
    if former_title is not None:
        caption += f"<b>Предыдущее название:</b> {former_title}\n"
    if username is not None:
        caption += f"<b>Тип группы:</b> Публичный\n"
        caption += f"<b>Линк:</b> {username}\n"
    else:
        caption += f"<b>Тип группы:</b> Приватный\n"
    if creator_username is not None:
        caption += f"<b>Создатель:</b> <code>{creator_username}</code>\n"
    elif creator_valid:
        caption += (
            "<b>Создатель:</b> <code><a"
            f' href="tg://user?id={creator_id}">{creator_firstname}</a></code>\n'
        )
    if created is not None:
        caption += (
            f"<b>Создан:</b> {created.date().strftime('%b %d, %Y')} -"
            f" {created.time()}\n"
        )
    else:
        caption += (
            f"<b>Создан:</b> {chat_obj_info.date.date().strftime('%b %d, %Y')} -"
            f" {chat_obj_info.date.time()}\n"
        )
    if messages_viewable is not None:
        caption += f"<b>Видимые сообщения:</b> {messages_viewable}\n"
    if messages_sent:
        caption += f"<b>Всего сообщений:</b> {messages_sent}\n"
    elif messages_sent_alt:
        caption += f"<b>Всего сообщений:</b> {messages_sent_alt}\n"
    if members is not None:
        caption += f"<b>Участников:</b> {members}\n"
    if admins is not None:
        caption += f"<b>Админов:</b> {admins}\n"
    if bots_list:
        caption += f"<b>Ботов:</b> {bots}\n"
    if users_online:
        caption += f"<b>Сейчас онлайн:</b> {users_online}\n"
    if restrcited_users is not None:
        caption += f"<b>Ограниченных пользователей:</b> {restrcited_users}\n"
    if banned_users is not None:
        caption += f"<b>Забаненных пользователей:</b> {banned_users}\n"
    if group_stickers is not None:
        caption += (
            "<b>Стикеры группы:</b> <a"
            f' href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>\n'
        )
    caption += "\n"
    caption += f"<b>Слоумод:</b> {slowmode}"
    if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled:
        caption += f", {slowmode_time} секунд\n"
    else:
        caption += "\n"
    caption += f"<b>Ограничен:</b> {restricted}\n"
    if chat_obj_info.restricted:
        caption += f"> Платформа: {chat_obj_info.restriction_reason[0].platform}\n"
        caption += f"> Причина: {chat_obj_info.restriction_reason[0].reason}\n"
        caption += f"> Текст: {chat_obj_info.restriction_reason[0].text}\n\n"
    else:
        caption += ""
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "<b>Скам</b>: да\n\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"<b>Верифицирован:</b> {verified}\n\n"
    if description:
        caption += f"<b>Описание:</b> \n\n<code>{description}</code>\n"
    return caption
