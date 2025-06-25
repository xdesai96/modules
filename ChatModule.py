# meta developer: @xdesai

from datetime import timedelta, datetime, timezone
import os
import re
from .. import loader, utils
from telethon.tl.functions.channels import (
    GetParticipantRequest,
    LeaveChannelRequest,
    DeleteChannelRequest,
    EditTitleRequest,
    EditPhotoRequest,
    CreateChannelRequest
)
from telethon.errors import (
    UserNotParticipantError,
    UserIdInvalidError,
    MessageTooLongError,
)
from telethon.tl.types import (
    Channel,
    Chat,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChatBannedRights
)
from telethon.tl.functions.messages import (
    DeleteChatRequest,
    EditChatDefaultBannedRightsRequest,
    EditChatTitleRequest,
    ExportChatInviteRequest
)


@loader.tds
class ChatModuleMod(loader.Module):
    strings = {
        "name": "ChatModule",
        "my_id": "<emoji document_id=5208454037531280484>💜</emoji> <b>My ID:</b> <code>{my_id}</code>",
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>Chat ID:</b> <code>{chat_id}</code>",
        "user_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>User's ID:</b> <code>{user_id}</code>",
        "user_not_participant": "<emoji document_id=5019523782004441717>❌</emoji> <b>User is not in this group.</b>",
        "rights_header": '<b><a href="tg://user?id={id}">{name}</a>\'s rights in this chat\n\n',
        "not_an_admin": "<emoji document_id=5019523782004441717>❌</emoji> {user} is not an admin.",
        "no_rights": "<emoji document_id=5019523782004441717>❌</emoji> <b>I don't have enough rights :(</b>",
        "no_user": "<emoji document_id=5019523782004441717>❌</emoji> <b>User not found.</b>",
        "change_info": "Change Info",
        "delete_messages": "Delete Messages",
        "ban_users": "Ban users",
        "invite_users": "Invite Users",
        "pin_messages": "Pin Messages",
        "add_admins": "Add Admins",
        "manage_call": "Manage Call",
        "post_stories": "Post Stories",
        "edit_stories": "Edit Stories",
        "delete_stories": "Delete Stories",
        "anonymous": "Anonymous",
        "manage_topics": "Manage Topics",
        "post_messages": "Post messages",
        "edit_messages": "Edit messages",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>Invalid args.</b>",
        "error": "<b>Error:</b> <code>{error}</code>",
        "of_chat": "Chat",
        "of_channel": "Channel",
        "loading": "<emoji document_id=5021712394259268143>🟡</emoji> <b>Loading data ...</b>",
        "own_list": "<b>My possessions ({count}):</b>\n\n{msg}",
        "no_ownerships": "<emoji document_id=5019523782004441717>❌</emoji> <b>No possessions.</b>",
        "not_a_chat": "<emoji document_id=5276240711795107620>⚠️</emoji> <b>It works only in groups!</b>",
        "successful_delete": "<emoji document_id=5021905410089550576>✅</emoji> {chat_type} successfully deleted",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>No deleted accounts found here</b>",
        "kicked_deleted_accounts": "<emoji document_id=5328302454226298081>🫥</emoji> <b>Removed {count} deleted accounts</b>",
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b>Admins in <code>{title}</code> ({count}):</b>\n\n",
        "admins_in_chat_caption": '<b>Admins in "{}":</b>',
        "too_many_admins": "Damn, too many admins here. Loading the list of admins into a file...",
        "no_admins_in_chat": "<b>No admins in this chat.</b>",
        "bots_in_chat": "<emoji document_id=5276127848644503161>🤖</emoji> <b>Bots in <code>{title}</code> ({count}):</b>\n\n",
        "bots_in_chat_caption": "<b>Bots in <code>{}</code>:</b>",
        "too_many_bots": "Damn, too many bots here. Loading the list of bots into a file...",
        "no_bots_in_chat": "<b>No bots in this chat.</b>",
        "users_in_chat": "<emoji document_id=5275979556308674886>👤</emoji> <b>Users in <code>{title}</code> ({count}):</b>\n\n",
        "users_in_chat_caption": "<b>Users in <code>{}</code>:</b>",
        "no_user_in_chat": "<b>No users in this chat.</b>",
        "user_is_banned": "⛔️ <b>{name} [<code>{id}</code>] has been banned for {time_info}.</b>",
        "user_is_banned_with_reason": "⛔️ <b>{name} [<code>{id}</code>] has been banned for {time_info}.</b>\n<i>Reason: {reason}</i>",
        "user_is_banned_forever": "⛔️ <b>{name} [<code>{id}</code>] has been banned forever.</b>",
        "user_is_banned_forever_with_reason": "⛔️ <b>{name} [<code>{id}</code>] has been banned forever.</b>\n<i>Reason: {reason}</i>",
        "user_is_unbanned": "👋🏻 <b>{name} [<code>{id}</code>] has been unbanned.</b>",
        "user_is_kicked": "🍃 <b><code>{name}</code> [<code>{id}</code>] has been kicked.</b>",
        "user_is_kicked_with_reason": "🍃 <b><code>{name}</code> [<code>{id}</code>] has been kicked.</b>\n<i>Reason: {reason}</i>",
        "user_is_muted_with_reason": "🔇 <b>{name} [<code>{id}</code>] has been muted for {time_info}.</b>\n<i>Reason: {reason}</i>",
        "user_is_muted": "🔇 <b>{name} [<code>{id}</code>] has been muted for {time_info}.</b>",
        "user_is_muted_with_reason_forever": "🔇 <b>{name} [<code>{id}</code>] has been muted forever.</b>\n<i>Reason: {reason}</i>",
        "user_is_muted_forever": "🔇 <b>{name} [<code>{id}</code>] has been muted forever.</b>",
        "user_is_unmuted": "🔊 <b>{name} [<code>{id}</code>] has been unmuted.</b>",
        "chat_muted": "🔇 <b>The chat is now muted for participants.</b>",
        "chat_unmuted": "✅ <b>The chat is now open to all participants.</b>",
        "title_changed": "<b>The {type_of} title was successfully changed from <code>{old_title}</code> to <code>{new_title}</code>.</b>",
        "channel_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>The channel <code>{title}</code> is created.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Invite link: {link}</b>",
        "group_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>The group <code>{title}</code> is created.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Invite link: {link}</b>"
    }

    strings_ru = {
        "my_id": "💜 <b>Мой ID:</b> <code>{my_id}</code>",
        "chat_id": "💬 <b>ID чата:</b> <code>{chat_id}</code>",
        "user_id": "👤 <b>ID пользователя:</b> <code>{user_id}</code>",
        "user_not_participant": "❌ <b>Пользователь не состоит в этой группе.</b>",
        "rights_header": '<b><a href="tg://user?id={id}">{name}</a> — права в этом чате\n\n',
        "not_an_admin": "❌ {user} не является админом.",
        "no_rights": "❌ <b>У меня нет достаточных прав :(</b>",
        "no_user": "❌ <b>Пользователь не найден.</b>",
        "change_info": "Изменение информации",
        "delete_messages": "Удаление сообщений",
        "ban_users": "Бан пользователей",
        "invite_users": "Приглашение пользователей",
        "pin_messages": "Закрепление сообщений",
        "add_admins": "Добавление админов",
        "manage_call": "Управление звонками",
        "post_stories": "Публикация историй",
        "edit_stories": "Редактирование историй",
        "delete_stories": "Удаление историй",
        "anonymous": "Анонимность",
        "manage_topics": "Управление темами",
        "post_messages": "Публикация сообщений",
        "edit_messages": "Редактирование сообщений",
        "invalid_args": "❌ <b>Неверные аргументы.</b>",
        "error": "<b>Ошибка:</b> <code>{error}</code>",
        "of_chat": "Чат",
        "of_channel": "Канал",
        "loading": "🟡 <b>Загрузка данных ...</b>",
        "own_list": "<b>Мои владения ({count}):</b>\n\n{msg}",
        "no_ownerships": "❌ <b>Нет владений.</b>",
        "not_a_chat": "⚠️ <b>Работает только в группах!</b>",
        "successful_delete": "✅ {chat_type} успешно удален",
        "no_deleted_accounts": "😎 <b>Удаленных аккаунтов не найдено</b>",
        "kicked_deleted_accounts": "🫥 <b>Удалено {count} удалённых аккаунтов</b>",
        "admins_in_chat": "👑 <b>Админы в <code>{title}</code> ({count}):</b>\n\n",
        "admins_in_chat_caption": '<b>Админы в «{}»:</b>',
        "too_many_admins": "Слишком много админов. Загружаю список в файл...",
        "no_admins_in_chat": "<b>Нет админов в этом чате.</b>",
        "bots_in_chat": "🤖 <b>Боты в <code>{title}</code> ({count}):</b>\n\n",
        "bots_in_chat_caption": "<b>Боты в <code>{}</code>:</b>",
        "too_many_bots": "Слишком много ботов. Загружаю список в файл...",
        "no_bots_in_chat": "<b>Нет ботов в этом чате.</b>",
        "users_in_chat": "👤 <b>Пользователи в <code>{title}</code> ({count}):</b>\n\n",
        "users_in_chat_caption": "<b>Пользователи в <code>{}</code>:</b>",
        "no_user_in_chat": "<b>Нет пользователей в этом чате.</b>",
        "user_is_banned": "⛔️ <b>{name} [<code>{id}</code>] забанен на {time_info}.</b>",
        "user_is_banned_with_reason": "⛔️ <b>{name} [<code>{id}</code>] забанен на {time_info}.</b>\n<i>Причина: {reason}</i>",
        "user_is_banned_forever": "⛔️ <b>{name} [<code>{id}</code>] забанен навсегда.</b>",
        "user_is_banned_forever_with_reason": "⛔️ <b>{name} [<code>{id}</code>] забанен навсегда.</b>\n<i>Причина: {reason}</i>",
        "user_is_unbanned": "👋🏻 <b>{name} [<code>{id}</code>] разбанен.</b>",
        "user_is_kicked": "🍃 <b><code>{name}</code> [<code>{id}</code>] был кикнут.</b>",
        "user_is_kicked_with_reason": "🍃 <b><code>{name}</code> [<code>{id}</code>] был кикнут.</b>\n<i>Причина: {reason}</i>",
        "user_is_muted_with_reason": "🔇 <b>{name} [<code>{id}</code>] замьючен на {time_info}.</b>\n<i>Причина: {reason}</i>",
        "user_is_muted": "🔇 <b>{name} [<code>{id}</code>] замьючен на {time_info}.</b>",
        "user_is_muted_with_reason_forever": "🔇 <b>{name} [<code>{id}</code>] замьючен навсегда.</b>\n<i>Причина: {reason}</i>",
        "user_is_muted_forever": "🔇 <b>{name} [<code>{id}</code>] замьючен навсегда.</b>",
        "user_is_unmuted": "🔊 <b>{name} [<code>{id}</code>] размьючен.</b>",
        "chat_muted": "🔇 <b>Чат теперь заглушен для участников.</b>",
        "chat_unmuted": "✅ <b>Чат снова открыт для участников.</b>",
        "title_changed": "<b>{type_of} успешно переименован с <code>{old_title}</code> на <code>{new_title}</code>.</b>",
        "channel_created": "✅ <b>Канал <code>{title}</code> создан.\n</b>🔗<b> Ссылка для приглашения: {link}</b>",
        "group_created": "✅ <b>Группа <code>{title}</code> создана.\n</b>🔗<b> Ссылка для приглашения: {link}</b>"
    }

    strings_jp = {
        "my_id": "💜 <b>私のID:</b> <code>{my_id}</code>",
        "chat_id": "💬 <b>チャットID:</b> <code>{chat_id}</code>",
        "user_id": "👤 <b>ユーザーID:</b> <code>{user_id}</code>",
        "user_not_participant": "❌ <b>ユーザーはこのグループに参加していません。</b>",
        "rights_header": '<b><a href="tg://user?id={id}">{name}</a> のこのチャットでの権限\n\n',
        "not_an_admin": "❌ {user} は管理者ではありません。",
        "no_rights": "❌ <b>必要な権限がありません :(</b>",
        "no_user": "❌ <b>ユーザーが見つかりません。</b>",
        "change_info": "Change Info",
        "delete_messages": "Delete Messages",
        "ban_users": "Ban users",
        "invite_users": "Invite Users",
        "pin_messages": "Pin Messages",
        "add_admins": "Add Admins",
        "manage_call": "Manage Call",
        "post_stories": "Post Stories",
        "edit_stories": "Edit Stories",
        "delete_stories": "Delete Stories",
        "anonymous": "Anonymous",
        "manage_topics": "Manage Topics",
        "post_messages": "Post messages",
        "edit_messages": "Edit messages",
        "invalid_args": "❌ <b>無効な引数です。</b>",
        "error": "<b>エラー:</b> <code>{error}</code>",
        "of_chat": "チャット",
        "of_channel": "チャンネル",
        "loading": "🟡 <b>データを読み込み中...</b>",
        "own_list": "<b>私の所有物 ({count}):</b>\n\n{msg}",
        "no_ownerships": "❌ <b>所有しているものがありません。</b>",
        "not_a_chat": "⚠️ <b>これはグループでのみ機能します！</b>",
        "successful_delete": "✅ {chat_type} が正常に削除されました",
        "no_deleted_accounts": "😎 <b>削除されたアカウントは見つかりませんでした</b>",
        "kicked_deleted_accounts": "🫥 <b>{count} 件の削除されたアカウントを削除しました</b>",
        "admins_in_chat": "👑 <b><code>{title}</code> の管理者 ({count}):</b>\n\n",
        "admins_in_chat_caption": '<b>「{}」の管理者:</b>',
        "too_many_admins": "管理者が多すぎます。ファイルにエクスポートしています...",
        "no_admins_in_chat": "<b>このチャットには管理者がいません。</b>",
        "bots_in_chat": "🤖 <b><code>{title}</code> のボット ({count}):</b>\n\n",
        "bots_in_chat_caption": "<b><code>{}</code> のボット:</b>",
        "too_many_bots": "ボットが多すぎます。ファイルにエクスポートしています...",
        "no_bots_in_chat": "<b>このチャットにボットはいません。</b>",
        "users_in_chat": "👤 <b><code>{title}</code> のユーザー ({count}):</b>\n\n",
        "users_in_chat_caption": "<b><code>{}</code> のユーザー:</b>",
        "no_user_in_chat": "<b>このチャットにはユーザーがいません。</b>",
        "user_is_banned": "⛔️ <b>{name} [<code>{id}</code>] は {time_info} の間、禁止されました。</b>",
        "user_is_banned_with_reason": "⛔️ <b>{name} [<code>{id}</code>] は {time_info} の間、禁止されました。</b>\n<i>理由: {reason}</i>",
        "user_is_banned_forever": "⛔️ <b>{name} [<code>{id}</code>] は永久に禁止されました。</b>",
        "user_is_banned_forever_with_reason": "⛔️ <b>{name} [<code>{id}</code>] は永久に禁止されました。</b>\n<i>理由: {reason}</i>",
        "user_is_unbanned": "👋🏻 <b>{name} [<code>{id}</code>] の禁止が解除されました。</b>",
        "user_is_kicked": "🍃 <b><code>{name}</code> [<code>{id}</code>] はキックされました。</b>",
        "user_is_kicked_with_reason": "🍃 <b><code>{name}</code> [<code>{id}</code>] はキックされました。</b>\n<i>理由: {reason}</i>",
        "user_is_muted_with_reason": "🔇 <b>{name} [<code>{id}</code>] は {time_info} の間、ミュートされました。</b>\n<i>理由: {reason}</i>",
        "user_is_muted": "🔇 <b>{name} [<code>{id}</code>] は {time_info} の間、ミュートされました。</b>",
        "user_is_muted_with_reason_forever": "🔇 <b>{name} [<code>{id}</code>] は永久にミュートされました。</b>\n<i>理由: {reason}</i>",
        "user_is_muted_forever": "🔇 <b>{name} [<code>{id}</code>] は永久にミュートされました。</b>",
        "user_is_unmuted": "🔊 <b>{name} [<code>{id}</code>] のミュートが解除されました。</b>",
        "chat_muted": "🔇 <b>チャットは参加者に対してミュートされました。</b>",
        "chat_unmuted": "✅ <b>チャットはすべての参加者に開放されました。</b>",
        "title_changed": "<b>{type_of} のタイトルが <code>{old_title}</code> から <code>{new_title}</code> に変更されました。</b>",
        "channel_created": "✅ <b>チャンネル <code>{title}</code> が作成されました。\n</b>🔗<b> 招待リンク: {link}</b>",
        "group_created": "✅ <b>グループ <code>{title}</code> が作成されました。\n</b>🔗<b> 招待リンク: {link}</b>"
    }


    @loader.command(ru_doc="[reply] - Узнать ID")
    async def id(self, message):
        """[reply] - Get the ID"""
        my_id = (await self._client.get_me()).id
        chat = await message.get_chat()
        chat_id = chat.id
        reply = await message.get_reply_message()
        user_id = None
        if reply and not message.is_private:
            user_id = reply.sender_id
        output = f"{self.strings('my_id').format(my_id=my_id)}\n{self.strings('chat_id').format(chat_id=chat_id)}"
        if user_id:
            output += f"\n{self.strings('user_id').format(user_id=user_id)}"
        return await utils.answer(message, output)

    @loader.command(
        ru_doc="[reply/username/id] - Посмотреть права администратора пользователя"
    )
    async def rights(self, message):
        """[reply/username/id] - Check user's admin rights"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if message.is_group and message.is_channel:
            rights = [
                "change_info",
                "delete_messages",
                "ban_users",
                "invite_users",
                "pin_messages",
                "add_admins",
                "manage_call",
                "post_stories",
                "edit_stories",
                "delete_stories",
                "anonymous",
                "manage_topics",
                "post_messages",
                "edit_messages",
            ]
            if reply:
                participant_id = reply.sender_id
            else:
                if args:
                    participant_id = (
                        args[0] if not args[0].strip().isdigit() else int(args[0])
                    )
                else:
                    return await utils.answer(message, self.strings("no_user"))
            try:
                result = await self._client(
                    GetParticipantRequest(channel=chat, participant=participant_id)
                )
            except UserNotParticipantError:
                return await utils.answer(
                    message,
                    self.strings("user_not_participant").format(user=participant_id),
                )
            except (UserIdInvalidError, ValueError):
                return await utils.answer(
                    message, self.strings("no_user").format(user=participant_id)
                )
            user = await self._client.get_entity(participant_id)
            participant = result.participant
            output = f"{self.strings('not_an_admin').format(user=user.first_name)}"
            if hasattr(participant, "admin_rights") and participant.admin_rights:
                output = self.strings("rights_header").format(
                    name=user.first_name, id=user.id
                )
                can_do = ""
                for right in rights:
                    if getattr(participant.admin_rights, right):
                        can_do += f"<emoji document_id=6296367896398399651>✅</emoji> {self.strings(right)}\n"
                if not can_do:
                    can_do += "No rights"
                output += can_do

            return await utils.answer(
                message, f"<blockquote expandable><b>{output}</b></blockquote>"
            )

    @loader.command(ru_doc="Покинуть чат")
    async def leave(self, message):
        """Leave chat"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        await message.delete()
        await self._client(LeaveChannelRequest((await message.get_chat()).id))

    @loader.command(ru_doc="[a[1-100] b[1-100]] | [reply] Удалить сообщения")
    async def d(self, message):
        """[a[1-100] b[1-100]] | [reply] - Delete messages"""
        args = utils.get_args(message)
        reply = await message.get_reply_message()
        await message.delete()
        if args:
            direction = args[0][0]
            try:
                count = int(args[0][1:])
                if count < 1 or count > 99:
                    return await utils.answer(message, self.strings("invalid_args"))
            except:
                count = 99
            if reply:
                ids = [reply.id]
                if direction == "a":
                    messages = await self._client.get_messages(
                        reply.chat_id, min_id=reply.id, limit=count, reverse=True
                    )
                    ids.extend([msg.id for msg in messages])
                elif direction == "b":
                    messages = await self._client.get_messages(
                        reply.chat_id, max_id=reply.id, limit=count - 1
                    )
                    ids.extend([msg.id for msg in messages])
                else:
                    return await utils.answer(message, self.strings("invalid_args"))
                try:
                    await self._client.delete_messages(reply.chat_id, ids)
                except Exception as e:
                    await utils.answer(message, self.strings("error").format(error=e))
        else:
            if reply:
                try:
                    await reply.delete()
                except:
                    return
            else:
                return

    @loader.command(
        ru_doc="Показывает список чатов, каналов и групп где вы админ/владелец"
    )
    async def own(self, message):
        """Shows the list of chats, channels and groups where you are an admin/owner"""
        count = 0
        msg = ""
        await utils.answer(message, self.strings("loading"))
        async for dialog in self._client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                chat = await self._client.get_entity(dialog.id)
                if chat.admin_rights or chat.creator:
                    count += 1
                    chat_type = (
                        self.strings("of_chat")
                        if dialog.is_group
                        else self.strings("of_channel")
                    )
                    msg += f"• {chat.title} <b>({chat_type})</b> | <code>{chat.id}</code>\n"

        if msg:
            await utils.answer(
                message,
                f"<blockquote expandable><b>{self.strings('own_list').format(count=count, msg=msg)}</b></blockquote>",
                parse_mode="html",
            )
        else:
            await utils.answer(message, self.strings("no_ownerships", message))

    @loader.command(ru_doc="[link/id] Удаляет группу/канал")
    async def dgc(self, message):
        """[link/id] Delete chat/channel"""
        args = utils.get_args(message)
        if not args:
            if message.is_private:
                return await utils.answer(message, self.strings("not_a_chat"))
            chat = await self._client.get_entity(message.chat_id)
            if message.is_channel:
                chat_type = self.strings("of_channel")
                await self._client(DeleteChannelRequest(chat.id))
            else:
                chat_type = self.strings("of_chat")
                await self._client(DeleteChatRequest(chat.id))
            return
        else:
            link = (
                await self._client.get_entity(int(args[0]))
                if args[0].isdigit()
                else await self._client.get_entity(args[0])
            )
            if isinstance(link, Channel):
                chat_type = self.strings("of_channel")
                await self._client(DeleteChannelRequest(link.id))
            elif isinstance(link, Chat):
                chat_type = self.strings("of_chat")
                await self._client(DeleteChatRequest(link.id))
            else:
                return await utils.answer(message, self.strings("invalid_args"))
        return await utils.answer(
            message, self.strings("successful_delete").format(chat_type=chat_type)
        )

    @loader.command(ru_doc="Очищает группу/канал от удаленных аккаунтов")
    async def flush(self, message):
        """Removes deleted accounts from the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))

        chat = await message.get_chat()

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings("no_rights"))

        removed_count = 0

        async for user in self._client.iter_participants(chat):
            if user.deleted:
                try:
                    await self._client.kick_participant(chat, user)
                    removed_count += 1
                except ChatAdminRequiredError:
                    return await utils.answer(message, self.strings("no_rights"))
                except Exception as e:
                    return await utils.answer(
                        message, self.strings("error").format(error=str(e))
                    )

        if removed_count == 0:
            await utils.answer(message, self.strings("no_deleted_accounts"))
        else:
            await utils.answer(
                message,
                self.strings("kicked_deleted_accounts").format(count=removed_count),
            )

    @loader.command(ru_doc="Показывает админов в группе/канале")
    async def admins(self, message):
        """Shows the admins in the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        title = chat.title
        admins = await self._client.get_participants(
            message.chat_id, filter=ChannelParticipantsAdmins()
        )
        real_members = [
            member for member in admins if not member.bot and not member.deleted
        ]
        admins_header = self.strings("admins_in_chat").format(
            title=title, count=len(real_members)
        )
        if len(real_members) == 0:
            return await utils.answer(message, "no_admins_in_chat")
        for user in real_members:
            if not user.deleted:
                admins_header += f'<emoji document_id=5316712579467321913>🔴</emoji> <a href="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
            try:
                await utils.answer(
                    message,
                    f"<blockquote expandable><b>{admins_header}</b></blockquote>",
                )
            except MessageTooLongError:
                await utils.answer(message, self.strings("too_many_admins"))
                with open("adminlist.md", "w+") as file:
                    file.write(admins_header)
                await message.client.send_file(
                    message.chat_id,
                    "adminlist.md",
                    caption=self.strings("admins_in_chat_caption").format(title),
                    reply_to=message.id,
                )
                os.remove("adminlist.md")
                await message.delete()

    @loader.command(ru_doc="Показывает ботов в группе/канале")
    async def bots(self, message):
        """Shows the bots in the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        title = chat.title
        bots = await self._client.get_participants(
            message.chat_id, filter=ChannelParticipantsBots()
        )
        bots_header = self.strings("bots_in_chat").format(title=title, count=len(bots))
        if len(bots) == 0:
            return await utils.answer(message, self.strings("no_bots_in_chat"))
        for user in bots:
            if not user.deleted:
                bots_header += f'<emoji document_id=5316712579467321913>🔴</emoji> <a href="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
            try:
                await utils.answer(
                    message, f"<blockquote expandable><b>{bots_header}</b></blockquote>"
                )
            except MessageTooLongError:
                await utils.answer(message, self.strings("too_many_bots"))
                with open("botlist.md", "w+") as file:
                    file.write(bots_header)
                await message.client.send_file(
                    message.chat_id,
                    "adminlist.md",
                    caption=self.strings("bots_in_chat_caption").format(title),
                    reply_to=message.id,
                )
                os.remove("botlist.md")
                await message.delete()

    @loader.command(ru_doc="Показывает простых участников чата/канала")
    async def users(self, message):
        """Shows the users in the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        title = chat.title
        users = await self._client.get_participants(message.chat_id)
        real_users = [
            member for member in users if not member.bot and not member.deleted
        ]
        users_header = self.strings("users_in_chat").format(
            title=title, count=len(real_users)
        )
        if len(real_users) == 0:
            return await utils.answer(message, self.strings("no_user_in_chat"))
        for user in users:
            if not user.bot and not user.deleted:
                users_header += f'<emoji document_id=5314378500965145730>🔵</emoji> <a href ="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
        try:
            await utils.answer(
                message, f"<blockquote expandable><b>{users_header}</b></blockquote>"
            )
            return
        except MessageTooLongError:
            await utils.answer(message, self.strings("large_chat_loading"))
            file = open("userslist.md", "w+")
            file.write(users_header)
            file.close()
            await message.client.send_file(
                message.chat_id,
                "userslist.md",
                caption=self.strings("users_in_chat_caption").format(title),
                reply_to=message.id,
            )
            os.remove("userslist.md")
            await message.delete()
            return

    @loader.command(ru_doc="Забанить участника")
    async def ban(self, message):
        """Ban a participant temporarily or permanently"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))

        text = message.text.split("\n", 1)
        first_line = text[0]
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            user = await self._client.get_entity(await utils.get_target(message))
        if not user:
            return await utils.answer(message, self.strings("invalid_args"))

        time_match = re.search(r"(\d+)\s*(mo|y|w|d|h|m)", first_line)
        chat = await message.get_chat()
        if time_match:
            duration_str = time_match.group(0)
            until_date = self.parse_time(duration_str)
            time_info = self.parse_time_info(duration_str)

            await self._client.edit_permissions(chat, user, until_date=until_date, view_messages=False)

            if reason:
                return await utils.answer(
                    message,
                    self.strings("user_is_banned_with_reason").format(
                        id=user.id, name=user.first_name, reason=reason, time_info=time_info[0],
                    ),
                )
            return await utils.answer(
                message,
                self.strings("user_is_banned").format(id=user.id, name=user.first_name, time_info=time_info[0])
            )

        await self._client.edit_permissions(chat, user, view_messages=False)

        if reason:
            return await utils.answer(
                message,
                self.strings("user_is_banned_with_reason_forever").format(
                    id=user.id, name=user.first_name, reason=reason,
                ),
            )
        return await utils.answer(
            message,
            self.strings("user_is_banned_forever").format(id=user.id, name=user.first_name),
        )

    @loader.command(ru_doc="Разбанить пользователя")
    async def unban(self, message):
        """Unban a user"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        reply = await message.get_reply_message()
        user = Noneп
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            user = await self._client.get_entity(await utils.get_target(message))
        if not user:
            return await utils.answer(message, self.strings("no_user"))
        chat = await message.get_chat()
        await self._client.edit_permissions(chat, user, view_messages=True)
        return await utils.answer(
            message,
            self.strings("user_is_unbanned").format(id=user.id, name=user.first_name),
        )

    @loader.command(ru_doc="Кикнуть участника")
    async def kick(self, message):
        """Kick a participant"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        reply = await message.get_reply_message()
        reason = ""
        user = None
        if "\n" in message.text:
            reason = message.text.split("\n", 1)[1]
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            user = await self._client.get_entity(await utils.get_target(message))
        if not user:
            return await utils.answer(message, self.strings("no_user"))
        chat = await message.get_chat()
        await self._client.kick_participant(chat, user)
        return (
            await utils.answer(
                message,
                self.strings("user_is_kicked").format(id=user.id, name=user.first_name),
            )
            if not reason
            else await utils.answer(
                message,
                self.strings("user_is_kicked_with_reason").format(
                    id=user.id, name=user.first_name, reason=reason
                ),
            )
        )

    @loader.command(ru_doc="Замутить участника")
    async def mute(self, message):
        """Mute a participant temporarily or permanently"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        text = message.text.split("\n", 1)
        first_line = text[0]
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            user = await self._client.get_entity(await utils.get_target(message))
        if not user:
            return await utils.answer(message, self.strings("invalid_args"))

        time_match = re.search(r"(\d+)\s*(mo|y|w|d|h|m)", first_line)
        chat = await message.get_chat()
        if time_match:
            duration_str = time_match.group(0)
            until_date = self.parse_time(duration_str)
            time_info = self.parse_time_info(duration_str)

            await self._client.edit_permissions(chat, user, until_date=until_date, send_messages=False)

            if reason:
                return await utils.answer(
                    message,
                    self.strings("user_is_muted_with_reason").format(
                        id=user.id, name=user.first_name, reason=reason, time_info=time_info[0],
                    ),
                )
            return await utils.answer(
                message,
                self.strings("user_is_muted").format(id=user.id, name=user.first_name, time_info=time_info[0])
            )

        await self._client.edit_permissions(chat, user, send_messages=False)

        if reason:
            return await utils.answer(
                message,
                self.strings("user_is_muted_with_reason_forever").format(
                    id=user.id, name=user.first_name, reason=reason,
                ),
            )
        return await utils.answer(
            message,
            self.strings("user_is_muted_forever").format(id=user.id, name=user.first_name),
        )

    @loader.command(ru_doc="Размутить участника")
    async def unmute(self, message):
        """Unmute a participant"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        reply = await message.get_reply_message()
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            user = await self._client.get_entity(await utils.get_target(message))
        if not user:
            return await utils.answer(message, "no_user")

        chat = await message.get_chat()

        await self._client.edit_permissions(chat, user, send_messages=True)
        return await utils.answer(
            message,
            self.strings("user_is_unmuted").format(id=user.id, name=user.first_name),
        )

    @loader.command(ru_doc="Закрыть чат для всех кроме админов")
    async def mc(self, message):
        """Mute the chat for everyone except admins"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        current = chat.default_banned_rights
        is_muted = current.send_messages is True
        await self._client(
            EditChatDefaultBannedRightsRequest(
                chat,
                ChatBannedRights(
                    until_date=0,
                    send_messages=not is_muted
                ),
            )
        )
        if is_muted:
            return await utils.answer(message, self.strings("chat_unmuted"))
        else:
            return await utils.answer(message, self.strings("chat_muted"))

    @loader.command(ru_doc="Переименовать группу/канал")
    async def rename(self, message):
        """Rename the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        old_title = chat.title
        new_title = utils.get_args_raw(message)
        if message.is_channel:
            if message.is_group:
                type_of = self.strings("of_chat")
            else:
                type_of = self.strings("of_channel")
            await self._client(EditTitleRequest(channel=chat, title=new_title))
        else:
            type_of = self.strings("of_chat")
            await self._client(EditChatTitleRequest(chat_id=chat.id, title=new_title))
        return await utils.answer(
            message,
            self.strings("title_changed").format(
                old_title=old_title, new_title=new_title, type_of=type_of
            ),
        )

    @loader.command(ru_doc="[g/c] [title] - Создать группу/канал")
    async def create(self, message):
        """[g/c] [title] - Create group/channel"""
        args = utils.get_args(message)
        type_of = args[0]
        if type_of == "g":
            result = await self._client(CreateChannelRequest(title=args[1], megagroup=True, about=""))
            chat = result.chats[0]
            invite_link = await self._client(ExportChatInviteRequest(peer=chat.id, title="Invite link"))
            return await utils.answer(message, self.strings("group_created").format(link=invite_link.link, title=args[1]))
        elif type_of == "c":
            result = await self._client(CreateChannelRequest(title=args[1], broadcast=True, about=""))
            chat = result.chats[0]
            invite_link = await self._client(ExportChatInviteRequest(peer=chat.id, title="Invite link"))
            return await utils.answer(message, self.strings("channel_created").format(link=invite_link.link, title=args[1]))
        else:
            return await utils.answer(message, self.strings("invalid_args"))

    def parse_time(self, time: str) -> timedelta:
        unit_to_days = {
            "m": 1/1440,
            "h": 1/24,
            "d": 1,
            "w": 7,
            "mo": 30,
            "y": 365,
        }

        pattern = r"(\d+)\s*(mo|y|w|d|h|m)"
        matches = re.findall(pattern, time)
        total_days = 0
        for value, unit in matches:
            val = int(value)
            total_days += val * unit_to_days[unit]

        return timedelta(days=total_days)

    def parse_time_info(self, time: str):
        unit_names = {
            "y": ("year", "years"),
            "mo": ("month", "months"),
            "w": ("week", "weeks"),
            "d": ("day", "days"),
            "h": ("hour", "hours"),
            "m": ("minute", "minutes"),
        }
        units_order = ["y", "mo", "w", "d", "h", "m"]
        pattern = r"(\d+)\s*(mo|y|w|d|h|m)"
        matches = re.findall(pattern, time)
        time_parts = {}
        for value, unit in matches:
            value = int(value)
            if unit in time_parts:
                time_parts[unit] += value
            else:
                time_parts[unit] = value
        result = []
        for unit in units_order:
            if unit in time_parts:
                val = time_parts[unit]
                name = unit_names[unit][1 if val != 1 else 0]
                result.append(f"{val} {name}")
        return result
