# meta developer: @xdesai
# scope: disable_onload_docs

from datetime import timedelta, datetime, timezone
from .. import loader, utils
from telethon.tl.functions import channels
from telethon.tl import types
from telethon.tl.functions import messages


@loader.tds
class ChatModuleMod(loader.Module):
    strings = {
        "name": "ChatModule",
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>Chat ID:</b> <code>{chat_id}</code>",
        "user_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>User's ID:</b> <code>{user_id}</code>",
        "user_not_participant": "<emoji document_id=5019523782004441717>❌</emoji> <b>User is not in this group.</b>",
        "_": '<a href="tg://user?id={id}">{name}</a>\'s rights in this chat',
        "not_an_admin": "<emoji document_id=5019523782004441717>❌</emoji> {user} is not an admin.",
        "no_rights": "<emoji document_id=5019523782004441717>❌</emoji> <b>I don't have enough rights :(</b>",
        "no_user": "<emoji document_id=5019523782004441717>❌</emoji> <b>User not found.</b>",
        "change_info": "<emoji document_id=6296367896398399651>✅</emoji> Change Info",
        "delete_messages": "<emoji document_id=6296367896398399651>✅</emoji> Delete Messages",
        "other": "<emoji document_id=6296367896398399651>✅</emoji> Other",
        "ban_users": "<emoji document_id=6296367896398399651>✅</emoji> Ban users",
        "invite_users": "<emoji document_id=6296367896398399651>✅</emoji> Invite Users",
        "pin_messages": "<emoji document_id=6296367896398399651>✅</emoji> Pin Messages",
        "add_admins": "<emoji document_id=6296367896398399651>✅</emoji> Add Admins",
        "manage_call": "<emoji document_id=6296367896398399651>✅</emoji> Manage Call",
        "post_stories": "<emoji document_id=6296367896398399651>✅</emoji> Post Stories",
        "edit_stories": "<emoji document_id=6296367896398399651>✅</emoji> Edit Stories",
        "delete_stories": "<emoji document_id=6296367896398399651>✅</emoji> Delete Stories",
        "anonymous": "<emoji document_id=6296367896398399651>✅</emoji> Anonymous",
        "manage_topics": "<emoji document_id=6296367896398399651>✅</emoji> Manage Topics",
        "post_messages": "<emoji document_id=6296367896398399651>✅</emoji> Post messages",
        "edit_messages": "<emoji document_id=6296367896398399651>✅</emoji> Edit messages",
        "promoted_by": "<emoji document_id=5287734473775918473>🔼</emoji> Promoted by <a href='tg://user?id={id}'>{name}</a> [<code>{id}</code>]",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>Invalid args.</b>",
        "error": "<b>Error:</b> <code>{error}</code>",
        "of_chat": "Chat",
        "of_channel": "Channel",
        "loading": "<emoji document_id=5021712394259268143>🟡</emoji> <b>Loading data ...</b>",
        "own_list": "<b>My possessions ({count}):</b>\n\n{msg}",
        "no_ownerships": "<emoji document_id=5019523782004441717>❌</emoji> <b>No possessions.</b>",
        "successful_delete": "<emoji document_id=5021905410089550576>✅</emoji> {chat_type} successfully deleted",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>No deleted accounts found here</b>",
        "kicked_deleted_accounts": "<emoji document_id=5328302454226298081>🫥</emoji> <b>Removed {count} deleted accounts</b>",
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b>Admins in <code>{title}</code> ({count}):</b>\n",
        "no_admins_in_chat": "<b>No admins in this chat.</b>",
        "bots_in_chat": "<emoji document_id=5276127848644503161>🤖</emoji> <b>Bots in <code>{title}</code> ({count}):</b>\n\n",
        "no_bots_in_chat": "<b>No bots in this chat.</b>",
        "users_in_chat": "<emoji document_id=5275979556308674886>👤</emoji> <b>Users in <code>{title}</code> ({count}):</b>\n\n",
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
        "group_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>The group <code>{title}</code> is created.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Invite link: {link}</b>",
        "user_blocked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> is blocked.</b>',
        "user_privacy_restricted": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a>\'s privacy settings restrict this action.</b>',
        "user_not_mutual_contact": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> is not a mutual contact.</b>',
        "user_kicked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> is kicked from the chat.</b>',
        "user_invited": "<emoji document_id=6296367896398399651>✅</emoji> <b>User <a href='tg://user?id={id}'>{user}</a> is invited to the chat.</b>",
        "user_not_invited": "<emoji document_id=5019523782004441717>❌</emoji> <b>User could not be invited to the chat.</b>",
        "creator": "<emoji document_id=5433758796289685818>👑</emoji> <b>The creator is <a href='tg://user?id={id}'>{creator}</a>.</b>",
        "no_creator": "<emoji document_id=5019523782004441717>❌</emoji> <b>No creator found.</b>",
        "promoted": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> is promoted</b>',
        "demoted": "<emoji document_id=5447183459602669338>🔽</emoji> <b><a href='tg://user?id={id}'>{name}</a> is demoted</b>",
        "dnd": "<emoji document_id=5384262794306669858>🔕</emoji> <b>Chat muted and archived</b>",
        "dnd_failed": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Failed to mute and archive chat</b>",
        "msg_link": "<emoji document_id=5271604874419647061>🔗</emoji> <b>The message link: {link}</b>",
        "msg_link_failed": "<emoji document_id=5019523782004441717>❌</emoji> <b>Failed to get the link</b>",
        "pinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Pinned the message</b>",
        "unpinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Unpinned the message</b>",
        "banned_in_chat": "<emoji document_id=5019523782004441717>❌</emoji> <b>Banned users in <code>{title}</code> ({count}):</b>\n\n",
        "no_banned_in_chat": "<emoji document_id=5251741320690551495>👎</emoji> <b>No banned users in this chat.</b>",
        "type_group": "Group",
        "type_channel": "Channel",
        "type_unknown": "Unknown",
        "yes": "<emoji document_id=5408909562919007848>✅</emoji> Yes",
        "no": "<emoji document_id=5361566877149578396>✖️</emoji> No",
        "chatinfo": "<emoji document_id=5983036958274752500>🔒</emoji><b> Type: {type_of}\n</b><emoji document_id=5985457743576698865>#️⃣</emoji><b> Chat ID: </b><code>{id}</code><b>\n</b><emoji document_id=5408849420491962048>🔥</emoji><b> Title: {title}\n\n</b><emoji document_id=5870676941614354370>🖋</emoji><b> About: {about}\n\n</b><emoji document_id=5805553606635559688>👑</emoji><b> Admin count: {admins_count}\n</b><emoji document_id=5433648711982921307>✅</emoji><b> Online count: {online_count}\n</b><emoji document_id=6024039683904772353>👤</emoji><b> Participants count: {participants_count}\n</b><emoji document_id=5816617137447376501>🚫</emoji><b> Kicked сount: {kicked_count}\n</b><emoji document_id=5431560533243346887>🔀</emoji><b> Requests pending: {requests_pending}\n\n</b><emoji document_id=5408910404732595664>🕐</emoji><b> Slowmode period: {slowmode_seconds}\n</b><emoji document_id=6019279794988915337>📞</emoji><b> Call: {call}\n</b><emoji document_id=5408832111773757273>🗑</emoji><b> TTL period: {ttl_period}\n</b><emoji document_id=5408846628763217930>👤</emoji><b> Recent requesters: {recent_requesters}\n\n</b><emoji document_id=6021690418398239007>👥</emoji><b> Linked Chat ID: {linked_chat_id}\n</b><emoji document_id=6019328362479097179>🛡</emoji><b> Antispam: {antispam}\n</b><emoji document_id=6024008227564296298>👁</emoji><b> Participants hidden: {participants_hidden}\n\n</b><emoji document_id=6028171274939797252>🔗</emoji><b> Link: {link}</b>",
        "all_approved": "<emoji document_id=5409029658794537988>✅</emoji> <b>Users are approved</b>",
        "all_dismissed": "<emoji document_id=5458610095539645297>✖️</emoji> <b>Requests are dismissed</b>",
    }

    strings_ru = {
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>ID чата:</b> <code>{chat_id}</code>",
        "user_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>ID пользователя:</b> <code>{user_id}</code>",
        "user_not_participant": "<emoji document_id=5019523782004441717>❌</emoji> <b>Пользователь не состоит в этой группе.</b>",
        "_": '<b><a href="tg://user?id={id}">{name}</a> — права в этом чате',
        "not_an_admin": "<emoji document_id=5019523782004441717>❌</emoji> {user} не является админом.",
        "no_rights": "<emoji document_id=5019523782004441717>❌</emoji> <b>У меня недостаточно прав :(</b>",
        "no_user": "<emoji document_id=5019523782004441717>❌</emoji> <b>Пользователь не найден.</b>",
        "change_info": "<emoji document_id=6296367896398399651>✅</emoji> Изменение информации",
        "post_messages": "<emoji document_id=6296367896398399651>✅</emoji> Публикация сообщений",
        "edit_messages": "<emoji document_id=6296367896398399651>✅</emoji> Редактирование сообщений",
        "delete_messages": "<emoji document_id=6296367896398399651>✅</emoji> Удаление сообщений",
        "ban_users": "<emoji document_id=6296367896398399651>✅</emoji> Бан пользователей",
        "invite_users": "<emoji document_id=6296367896398399651>✅</emoji> Приглашение пользователей",
        "pin_messages": "<emoji document_id=6296367896398399651>✅</emoji> Закрепление сообщений",
        "add_admins": "<emoji document_id=6296367896398399651>✅</emoji> Назначение админов",
        "anonymous": "<emoji document_id=6296367896398399651>✅</emoji> Анонимность",
        "manage_call": "<emoji document_id=6296367896398399651>✅</emoji> Управление звонками",
        "other": "<emoji document_id=6296367896398399651>✅</emoji> Другое",
        "post_stories": "<emoji document_id=6296367896398399651>✅</emoji> Публикация историй",
        "edit_stories": "<emoji document_id=6296367896398399651>✅</emoji> Редактирование историй",
        "delete_stories": "<emoji document_id=6296367896398399651>✅</emoji> Удаление историй",
        "manage_topics": "<emoji document_id=6296367896398399651>✅</emoji> Управление темами",
        "promoted_by": "<emoji document_id=5287734473775918473>🔼</emoji> Назначил <a href='tg://user?id={id}'>{name}</a> [<code>{id}</code>]",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>Неверные аргументы.</b>",
        "error": "<b>Ошибка:</b> <code>{error}</code>",
        "of_chat": "Чат",
        "of_channel": "Канал",
        "loading": "<emoji document_id=5021712394259268143>🟡</emoji> <b>Загрузка данных ...</b>",
        "own_list": "<b>Мои владения ({count}):</b>\n\n{msg}",
        "no_ownerships": "<emoji document_id=5019523782004441717>❌</emoji> <b>Нет владений.</b>",
        "successful_delete": "<emoji document_id=5021905410089550576>✅</emoji> {chat_type} успешно удалён",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>Удалённые аккаунты не найдены</b>",
        "kicked_deleted_accounts": "<emoji document_id=5328302454226298081>🫥</emoji> <b>Удалено {count} удалённых аккаунтов</b>",
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b>Админы в <code>{title}</code> ({count}):</b>\n",
        "no_admins_in_chat": "<b>В чате нет админов.</b>",
        "bots_in_chat": "<emoji document_id=5276127848644503161>🤖</emoji> <b>Боты в <code>{title}</code> ({count}):</b>\n\n",
        "no_bots_in_chat": "<b>В чате нет ботов.</b>",
        "users_in_chat": "<emoji document_id=5275979556308674886>👤</emoji> <b>Пользователи в <code>{title}</code> ({count}):</b>\n\n",
        "no_user_in_chat": "<b>В чате нет пользователей.</b>",
        "user_is_banned": "⛔️ <b>{name} [<code>{id}</code>] забанен на {time_info}.</b>",
        "user_is_banned_with_reason": "⛔️ <b>{name} [<code>{id}</code>] забанен на {time_info}.</b>\n<i>Причина: {reason}</i>",
        "user_is_banned_forever": "⛔️ <b>{name} [<code>{id}</code>] забанен навсегда.</b>",
        "user_is_banned_forever_with_reason": "⛔️ <b>{name} [<code>{id}</code>] забанен навсегда.</b>\n<i>Причина: {reason}</i>",
        "user_is_unbanned": "👋🏻 <b>{name} [<code>{id}</code>] разбанен.</b>",
        "user_is_kicked": "🍃 <b><code>{name}</code> [<code>{id}</code>] был кикнут.</b>",
        "user_is_kicked_with_reason": "🍃 <b><code>{name}</code> [<code>{id}</code>] был кикнут.</b>\n<i>Причина: {reason}</i>",
        "user_is_muted_with_reason": "🔇 <b>{name} [<code>{id}</code>] замучен на {time_info}.</b>\n<i>Причина: {reason}</i>",
        "user_is_muted": "🔇 <b>{name} [<code>{id}</code>] замучен на {time_info}.</b>",
        "user_is_muted_with_reason_forever": "🔇 <b>{name} [<code>{id}</code>] замучен навсегда.</b>\n<i>Причина: {reason}</i>",
        "user_is_muted_forever": "🔇 <b>{name} [<code>{id}</code>] замучен навсегда.</b>",
        "user_is_unmuted": "🔊 <b>{name} [<code>{id}</code>] размучен.</b>",
        "chat_muted": "🔇 <b>Чат теперь заглушён для участников.</b>",
        "chat_unmuted": "✅ <b>Чат снова открыт для участников.</b>",
        "title_changed": "<b>{type_of} успешно переименован с <code>{old_title}</code> на <code>{new_title}</code>.</b>",
        "channel_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>Канал <code>{title}</code> создан.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Ссылка: {link}</b>",
        "group_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>Группа <code>{title}</code> создана.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Ссылка: {link}</b>",
        "user_blocked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> заблокирован.</b>',
        "user_privacy_restricted": '<emoji document_id=5019523782004441717>❌</emoji> <b>Настройки конфиденциальности <a href="tg://user?id={user_id}">{user}</a> ограничивают это действие.</b>',
        "user_not_mutual_contact": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> не является взаимным контактом.</b>',
        "user_kicked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> кикнут из чата.</b>',
        "user_invited": "<emoji document_id=6296367896398399651>✅</emoji> <b>Пользователь <a href='tg://user?id={id}'>{user}</a> приглашён в чат.</b>",
        "user_not_invited": "<emoji document_id=5019523782004441717>❌</emoji> <b>Пользователя не удалось пригласить в чат.</b>",
        "creator": "<emoji document_id=5433758796289685818>👑</emoji> <b>Создатель: <a href='tg://user?id={id}'>{creator}</a>.</b>",
        "no_creator": "<emoji document_id=5019523782004441717>❌</emoji> <b>Создатель не найден.</b>",
        "promoted": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> назначен администратором</b>',
        "demoted": "<emoji document_id=5447183459602669338>🔽</emoji> <b><a href='tg://user?id={id}'>{name}</a> снят с роли администратора</b>",
        "dnd": "<emoji document_id=5384262794306669858>🔕</emoji> <b>Чат отключён и архивирован</b>",
        "dnd_failed": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Не удалось отключить и архивировать чат</b>",
        "msg_link": "<emoji document_id=5271604874419647061>🔗</emoji> <b>Ссылка на сообщение: {link}</b>",
        "msg_link_failed": "<emoji document_id=5019523782004441717>❌</emoji> <b>Не удалось получить ссылку</b>",
        "pinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Сообщение закреплено</b>",
        "unpinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Сообщение откреплено</b>",
        "banned_in_chat": "<emoji document_id=5019523782004441717>❌</emoji> <b>Забаненные пользователи в <code>{title}</code> ({count}):</b>\n\n",
        "no_banned_in_chat": "<emoji document_id=5251741320690551495>👎</emoji> <b>В этом чате нет забаненных пользователей.</b>",
        "type_group": "Группа",
        "type_channel": "Канал",
        "type_unknown": "Неизвестно",
        "yes": "<emoji document_id=5408909562919007848>✅</emoji> Есть",
        "no": "<emoji document_id=5361566877149578396>✖️</emoji> Нет",
        "chatinfo": "<emoji document_id=5983036958274752500>🔒</emoji><b> Тип: {type_of}\n</b><emoji document_id=5985457743576698865>#️⃣</emoji><b> ID чата: </b><code>{id}</code><b>\n</b><emoji document_id=5408849420491962048>🔥</emoji><b> Название: {title}\n\n</b><emoji document_id=5870676941614354370>🖋</emoji><b> Описание: {about}\n\n</b><emoji document_id=5805553606635559688>👑</emoji><b> Кол-во админов: {admins_count}\n</b><emoji document_id=5433648711982921307>✅</emoji><b> Онлайн: {online_count}\n</b><emoji document_id=6024039683904772353>👤</emoji><b> Участников: {participants_count}\n</b><emoji document_id=5816617137447376501>🚫</emoji><b> Заблокировано: {kicked_count}\n</b><emoji document_id=5431560533243346887>🔀</emoji><b> Ожидающие запросы: {requests_pending}\n\n</b><emoji document_id=5408910404732595664>🕐</emoji><b> Период замедления: {slowmode_seconds}\n</b><emoji document_id=6019279794988915337>📞</emoji><b> Звонок: {call}\n</b><emoji document_id=5408832111773757273>🗑</emoji><b> Период TTL: {ttl_period}\n</b><emoji document_id=5408846628763217930>👤</emoji><b> Последние запросы: {recent_requesters}\n\n</b><emoji document_id=6021690418398239007>👥</emoji><b> Связанный ID чата: {linked_chat_id}\n</b><emoji document_id=6019328362479097179>🛡</emoji><b> Антиспам: {antispam}\n</b><emoji document_id=6024008227564296298>👁</emoji><b> Участники скрыты: {participants_hidden}\n\n</b><emoji document_id=6028171274939797252>🔗</emoji><b> Ссылка: {link}</b>",
        "all_approved": "<emoji document_id=5409029658794537988>✅</emoji> <b>Пользователи одобрены</b>",
        "all_dismissed": "<emoji document_id=5458610095539645297>✖️</emoji> <b>Запросы отклонены</b>",
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self.xdlib = await self.import_lib(
            "https://mods.xdesai.top/xdlib.py",
            suspend_on_error=True,
        )
        await self.request_join(
            "@xdesai_modules", self.xdlib.strings["request_join_reason"]
        )

    @loader.command(ru_doc="[reply] - Узнать ID")
    async def id(self, message):
        """[reply] - Get the ID"""
        reply = await message.get_reply_message()
        if reply:
            return await utils.answer(
                message, self.strings["user_id"].format(user_id=reply.sender_id)
            )
        return await utils.answer(
            message, self.strings["chat_id"].format(chat_id=message.chat_id)
        )

    @loader.command(
        ru_doc="[reply/username/id] - Посмотреть права администратора пользователя",
    )
    @loader.tag("no_pm")
    async def rights(self, message):
        """[reply/username/id] - Check user's admin rights"""
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        args = utils.get_args(message)

        if reply:
            participant_id = reply.sender_id
        else:
            if args:
                participant_id = next(iter(self.xdlib.parse.mentions(message)))
            else:
                return await utils.answer(message, self.strings["no_user"])
        try:
            result = await self._client.get_perms_cached(chat, participant_id)
        except Exception as e:
            return await utils.answer(
                message, self.strings["error"].format(error=str(e))
            )
        participant = result.participant
        user = await self._client.get_entity(participant.user_id)
        output = f"{self.strings['not_an_admin'].format(user=user.first_name)}"
        if hasattr(participant, "admin_rights") and participant.admin_rights:
            can_do = ""
            rights = participant.to_dict().get("admin_rights")
            for right, is_permitted in rights.items():
                if right == "_":
                    output = f"{self.strings[right].format(name=user.first_name, id=user.id)}\n\n"
                    continue
                if is_permitted:
                    can_do += f"{self.strings[right]}\n"
            output += can_do
            if hasattr(participant, "promoted_by") and participant.promoted_by:
                promoter = await self._client.get_entity(participant.promoted_by)
                output += f"\n{self.strings['promoted_by'].format(id=participant.promoted_by, name=promoter.first_name)}"

        return await utils.answer(
            message, f"<blockquote expandable><b>{output}</b></blockquote>"
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

    @loader.command(
        ru_doc="Показывает список чатов, каналов и групп где вы админ/владелец",
    )
    async def own(self, message):
        """Shows the list of chats, channels and groups where you are an admin/owner"""
        count = 0
        msg = ""
        await utils.answer(message, self.strings["loading"])
        async for dialog in self._client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                chat = await self._client.get_entity(dialog.id)
                if chat.admin_rights or chat.creator:
                    count += 1
                    chat_type = (
                        self.strings["of_chat"]
                        if dialog.is_group
                        else self.strings["of_channel"]
                    )
                    msg += f"• {chat.title} <b>({chat_type})</b> | <code>{chat.id}</code>\n"

        if msg:
            await utils.answer(
                message,
                f"<blockquote expandable><b>{self.strings['own_list'].format(count=count, msg=msg)}</b></blockquote>",
                parse_mode="html",
            )
        else:
            await utils.answer(message, self.strings["no_ownerships"])

    @loader.command(ru_doc="[reply] - Закрепить сообщение")
    @loader.tag("only_reply")
    async def pin(self, message):
        """[reply] - Pin a message"""
        reply = await message.get_reply_message()
        try:
            await reply.pin(notify=True, pm_oneside=False)
        except Exception as e:
            return await utils.answer(
                message, self.strings["error"].format(error=str(e))
            )
        await utils.answer(message, self.strings["pinned"])

    @loader.command(ru_doc="Открепить сообщение")
    @loader.tag("only_reply")
    async def unpin(self, message):
        """Unpin a message"""
        reply = await message.get_reply_message()
        try:
            await reply.unpin()
        except Exception as e:
            return await utils.answer(
                message, self.strings["error"].format(error=str(e))
            )
        await utils.answer(message, self.strings["unpinned"])

    @loader.command(ru_doc="[link/id] Удаляет группу/канал")
    async def dgc(self, message):
        """[link/id] Delete chat/channel"""
        args = utils.get_args(message)
        if not args:
            chat = await self._client.get_entity(message.chat_id)
            if message.is_channel:
                chat_type = self.strings["of_channel"]
                await self._client(channels.DeleteChannelRequest(chat.id))
            else:
                try:
                    chat_type = self.strings["of_chat"]
                    await self._client(messages.DeleteChatRequest(chat.id))
                except Exception as e:
                    return await utils.answer(
                        message, self.strings["error"].format(error=e)
                    )
            return
        else:
            link = (
                await self._client.get_entity(int(args[0]))
                if args[0].isdigit()
                else await self._client.get_entity(args[0])
            )
            if isinstance(link, types.Channel):
                chat_type = self.strings["of_channel"]
                await self._client(channels.DeleteChannelRequest(link.id))
            elif isinstance(link, types.Chat):
                chat_type = self.strings["of_chat"]
                await self._client(messages.DeleteChatRequest(link.id))
            else:
                return await utils.answer(message, self.strings["invalid_args"])
        return await utils.answer(
            message, self.strings["successful_delete"].format(chat_type=chat_type)
        )

    @loader.command(ru_doc="Очищает группу/канал от удаленных аккаунтов")
    @loader.tag("no_pm")
    async def flush(self, message):
        """Removes deleted accounts from the chat/channel"""
        chat = await message.get_chat()

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings["no_rights"])

        removed_count = 0

        async for user in self._client.iter_participants(chat):
            if user.deleted:
                try:
                    await self._client.kick_participant(chat, user)
                    removed_count += 1
                except Exception as e:
                    return await utils.answer(
                        message, self.strings["error"].format(error=str(e))
                    )

        if removed_count == 0:
            await utils.answer(message, self.strings["no_deleted_accounts"])
        else:
            await utils.answer(
                message,
                self.strings["kicked_deleted_accounts"].format(count=removed_count),
            )

    @loader.command(ru_doc="Показывает админов в группе/канале")
    @loader.tag("no_pm")
    async def admins(self, message):
        """Shows the admins in the chat/channel"""
        chat = await message.get_chat()
        title = chat.title
        admins = await self._client.get_participants(
            message.chat_id, filter=types.ChannelParticipantsAdmins()
        )
        real_members = [
            member for member in admins if not member.bot and not member.deleted
        ]
        admins_list = ""
        creator = ""
        num_of_admins = len(real_members)
        for user in real_members:
            if hasattr(user, "participant") and isinstance(
                user.participant, types.ChannelParticipantCreator
            ):
                creator += (
                    self.strings["creator"].format(id=user.id, creator=user.first_name)
                    + "\n"
                )
                num_of_admins -= 1
                continue
            else:
                admins_list += f'<emoji document_id=5316712579467321913>🔴</emoji> <a href="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
        if num_of_admins == 0:
            return await utils.answer(
                message,
                f"<blockquote expandable><b>{creator}</b>\n{self.strings['no_admins_in_chat']}</blockquote>",
            )
        return await utils.answer(
            message,
            f"<blockquote expandable><b>{creator}</b>\n<b>{self.strings['admins_in_chat'].format(title=title, count=num_of_admins)}{admins_list}</b></blockquote>",
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
        chat = await message.get_chat()
        title = chat.title
        bots = await self._client.get_participants(
            message.chat_id, filter=types.ChannelParticipantsBots()
        )
        bots_header = self.strings["bots_in_chat"].format(title=title, count=len(bots))
        if len(bots) == 0:
            return await utils.answer(message, self.strings["no_bots_in_chat"])
        for user in bots:
            if not user.deleted:
                bots_header += f'<emoji document_id=5316712579467321913>🔴</emoji> <a href="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'

        await utils.answer(
            message, f"<blockquote expandable><b>{bots_header}</b></blockquote>"
        )

    @loader.command(ru_doc="Показывает простых участников чата/канала")
    @loader.tag("no_pm")
    async def users(self, message):
        """Shows the users in the chat/channel"""
        chat = await message.get_chat()
        title = chat.title
        users = await self._client.get_participants(message.chat_id)
        real_users = [
            member for member in users if not member.bot and not member.deleted
        ]
        users_header = self.strings["users_in_chat"].format(
            title=title, count=len(real_users)
        )
        if len(real_users) == 0:
            return await utils.answer(message, self.strings["no_user_in_chat"])
        for user in users:
            if not user.bot and not user.deleted:
                users_header += f'<emoji document_id=5314378500965145730>🔵</emoji> <a href ="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
        return await utils.answer(
            message, f"<blockquote expandable><b>{users_header}</b></blockquote>"
        )

    @loader.command(ru_doc="Забанить участника")
    @loader.tag("no_pm")
    async def ban(self, message):
        """Ban a participant temporarily or permanently"""
        text = message.text.split("\n", 1)
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        user = None
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            try:
                users = self.xdlib.parse.mentions(message)
                user = next(iter(users), None)
                user = await self._client.get_entity(user) if user else None
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )
        if not user:
            return await utils.answer(message, self.strings["invalid_args"])

        seconds = self.xdlib.parse.time(args)
        chat = await message.get_chat()
        if seconds:
            until_date = datetime.now(timezone.utc) + timedelta(seconds=seconds)
            time_info = self.xdlib.format.time(seconds)
            try:
                await self._client.edit_permissions(
                    chat, user, until_date=until_date, view_messages=False
                )
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )

            if reason:
                return await utils.answer(
                    message,
                    self.strings["user_is_banned_with_reason"].format(
                        id=user.id,
                        name=(
                            user.first_name
                            if hasattr(user, "first_name")
                            else user.title
                        ),
                        reason=reason,
                        time_info=time_info,
                    ),
                )
            return await utils.answer(
                message,
                self.strings["user_is_banned"].format(
                    id=user.id,
                    name=user.first_name if hasattr(user, "first_name") else user.title,
                    time_info=time_info,
                ),
            )

        await self._client.edit_permissions(chat, user, view_messages=False)

        if reason:
            return await utils.answer(
                message,
                self.strings["user_is_banned_forever_with_reason"].format(
                    id=user.id,
                    name=user.first_name if hasattr(user, "first_name") else user.title,
                    reason=reason,
                ),
            )
        return await utils.answer(
            message,
            self.strings["user_is_banned_forever"].format(
                id=user.id,
                name=user.first_name if hasattr(user, "first_name") else user.title,
            ),
        )

    @loader.command(ru_doc="Разбанить пользователя")
    @loader.tag("no_pm")
    async def unban(self, message):
        """Unban a user"""
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self.xdlib.messages.get_sender(reply)
        else:
            try:
                users = self.xdlib.parse.mentions(message)
                user = next(iter(users), None)
                user = await self._client.get_entity(user) if user else None
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        chat = await message.get_chat()
        try:
            await self._client.edit_permissions(chat, user, view_messages=True)
        except Exception as e:
            return await utils.answer(
                message, self.strings["error"].format(error=str(e))
            )
        return await utils.answer(
            message,
            self.strings["user_is_unbanned"].format(
                id=user.id,
                name=user.first_name if hasattr(user, "first_name") else user.title,
            ),
        )

    @loader.command(ru_doc="Кикнуть участника")
    @loader.tag("no_pm")
    async def kick(self, message):
        """Kick a participant"""
        reply = await message.get_reply_message()
        reason = ""
        user = None
        if "\n" in message.text:
            reason = message.text.split("\n", 1)[1]
        if reply:
            user = await self.xdlib.messages.get_sender(reply)
        else:
            try:
                users = self.xdlib.parse.mentions(message)
                user = next(iter(users), None)
                user = await self._client.get_entity(user) if user else None
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        chat = await message.get_chat()
        try:
            await self._client.kick_participant(chat, user)
        except Exception as e:
            return await utils.answer(
                message, self.strings["error"].format(error=str(e))
            )
        return (
            await utils.answer(
                message,
                self.strings["user_is_kicked"].format(
                    id=user.id,
                    name=user.first_name if hasattr(user, "first_name") else user.title,
                ),
            )
            if not reason
            else await utils.answer(
                message,
                self.strings["user_is_kicked_with_reason"].format(
                    id=user.id,
                    name=user.first_name if hasattr(user, "first_name") else user.title,
                    reason=reason,
                ),
            )
        )

    @loader.command(ru_doc="Замутить участника")
    @loader.tag("no_pm")
    async def mute(self, message):
        """Mute a participant temporarily or permanently"""
        text = message.text.split("\n", 1)
        args = utils.get_args_raw(message)
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self.xdlib.messages.get_sender(reply)
        else:
            try:
                users = self.xdlib.parse.mentions(message)
                user = next(iter(users), None)
                user = await self._client.get_entity(user) if user else None
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )
        if not user:
            return await utils.answer(message, self.strings["invalid_args"])

        seconds = self.xdlib.parse.time(args)
        chat = await message.get_chat()
        if seconds:
            until_date = datetime.now(timezone.utc) + timedelta(seconds=seconds)
            time_info = self.xdlib.format.time(seconds)

            try:
                await self._client.edit_permissions(
                    chat, user, until_date=until_date, send_messages=False
                )
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )

            if reason:
                return await utils.answer(
                    message,
                    self.strings["user_is_muted_with_reason"].format(
                        id=user.id,
                        name=(
                            user.first_name
                            if hasattr(user, "first_name")
                            else user.title
                        ),
                        reason=reason,
                        time_info=time_info,
                    ),
                )
            return await utils.answer(
                message,
                self.strings["user_is_muted"].format(
                    id=user.id,
                    name=user.first_name if hasattr(user, "first_name") else user.title,
                    time_info=time_info,
                ),
            )

        await self._client.edit_permissions(chat, user, send_messages=False)

        if reason:
            return await utils.answer(
                message,
                self.strings["user_is_muted_with_reason_forever"].format(
                    id=user.id,
                    name=user.first_name if hasattr(user, "first_name") else user.title,
                    reason=reason,
                ),
            )
        return await utils.answer(
            message,
            self.strings["user_is_muted_forever"].format(
                id=user.id,
                name=user.first_name if hasattr(user, "first_name") else user.title,
            ),
        )

    @loader.command(ru_doc="Размутить участника")
    @loader.tag("no_pm")
    async def unmute(self, message):
        """Unmute a participant"""
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self.xdlib.messages.get_sender(reply)
        else:
            try:
                users = self.xdlib.parse.mentions(message)
                user = next(iter(users), None)
                user = await self._client.get_entity(user) if user else None
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )
        if not user:
            return await utils.answer(message, "no_user")

        chat = await message.get_chat()

        try:
            await self._client.edit_permissions(chat, user, send_messages=True)
        except Exception as e:
            return await utils.answer(
                message, self.strings["error"].format(error=str(e))
            )
        return await utils.answer(
            message,
            self.strings["user_is_unmuted"].format(
                id=user.id,
                name=user.first_name if hasattr(user, "first_name") else user.title,
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
                type_of = self.strings["of_chat"]
            else:
                type_of = self.strings["of_channel"]
            try:
                await self._client(
                    channels.EditTitleRequest(channel=chat, title=new_title)
                )
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )
        else:
            type_of = self.strings["of_chat"]
            try:
                await self._client(
                    messages.EditChatTitleRequest(chat_id=chat.id, title=new_title)
                )
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=e)
                )
        return await utils.answer(
            message,
            self.strings["title_changed"].format(
                old_title=old_title, new_title=new_title, type_of=type_of
            ),
        )

    @loader.command(ru_doc="[g/c] [title] - Создать группу/канал")
    async def create(self, message):
        """[g/c] [title] - Create group/channel"""
        args = utils.get_args(message)
        type_of = args[0]
        if type_of == "g":
            result = await self._client(
                channels.CreateChannelRequest(
                    title=" ".join(args[1:]), megagroup=True, about=""
                )
            )
            chat = result.chats[0]
            invite_link = await self._client(
                messages.ExportChatInviteRequest(peer=chat.id, title="Invite link")
            )
            return await utils.answer(
                message,
                self.strings["group_created"].format(
                    link=invite_link.link, title=" ".join(args[1:])
                ),
            )
        elif type_of == "c":
            result = await self._client(
                channels.CreateChannelRequest(
                    title=" ".join(args[1:]), broadcast=True, about=""
                )
            )
            chat = result.chats[0]
            invite_link = await self._client(
                messages.ExportChatInviteRequest(peer=chat.id, title="Invite link")
            )
            return await utils.answer(
                message,
                self.strings["channel_created"].format(
                    link=invite_link.link, title=" ".join(args[1:])
                ),
            )
        else:
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
        reply = await message.get_reply_message()
        chat = await message.get_chat()
        if reply := await message.get_reply_message():
            link = await utils.get_message_link(reply, chat)
            return await utils.answer(
                message, self.strings["msg_link"].format(link=link)
            )
        return await utils.answer(message, self.strings["msg_link_failed"])

    @loader.command(ru_doc="Пригласить пользователя в чат")
    async def invite(self, message):
        """Invite a user to the chat (use -b to invite the inline bot)"""
        opts = self.xdlib.parse.opts(utils.get_args(message))
        chat = await message.get_chat()
        if opts.get("b"):
            await self.xdlib.chat.invite_bot(self._client, chat)
            entity = await self._client.get_entity(self.inline.bot_id)
            return await utils.answer(
                message,
                self.strings["user_invited"].format(
                    user=entity.first_name, id=entity.id
                ),
            )
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if reply:
            entity = await self.xdlib.messages.get_sender(reply)
            result = await self.xdlib.chat.invite_user(chat, entity)
            if result:
                return await utils.answer(
                    message,
                    self.strings["user_invited"].format(
                        user=entity.first_name, id=entity.id
                    ),
                )
            else:
                return await utils.answer(message, self.strings["user_not_invited"])
        elif args:
            for user in args:
                entity = await self._client.get_entity(
                    int(user) if user.isdigit() else user
                )
                result = await self.xdlib.chat.invite_user(chat, entity)
                if result:
                    return await utils.answer(
                        message,
                        self.strings["user_invited"].format(
                            user=entity.first_name, id=entity.id
                        ),
                    )
        else:
            return await utils.answer(message, self.strings["no_user"])

    @loader.command(
        ru_doc="<username/mention> [-h|--help] [-f|--fullrights] [-r|--rank rank] <right> - Назначить пользователя администратором"
    )
    @loader.tag("no_pm")
    async def setrights(self, message):
        """<username/mention> [-h|--help] [-f|--fullrights] [-r|--rank rank] <right> - Promote a participant"""
        opts = self.xdlib.parse.opts(utils.get_args(message))
        if not utils.get_args(message):
            return await utils.answer(message, self.strings["invalid_args"])
        reply = await message.get_reply_message()
        user = opts.get("u") or opts.get("user") or (reply.sender_id if reply else None)
        if not user:
            return await utils.answer(message, self.strings["invalid_args"])
        help = opts.get("h") or opts.get("help")
        if help:
            return await utils.answer(
                message, f"{await self.xdlib.admin.get_rights_table()}"
            )
        chat = await message.get_chat()
        user = await self._client.get_entity(user)
        rank = opts.get("r") or opts.get("rank") or ("Admin" if not user.bot else "Bot")
        if opts.get("f") or opts.get("fullrights"):
            await self.xdlib.admin.set_fullrights(chat, user, rank=rank)
            return await utils.answer(
                message,
                self.strings["promoted"].format(id=user.id, name=user.first_name),
            )
        perms = opts.get("p") or opts.get("perms")
        try:
            if not perms:
                await self.xdlib.admin.demote(chat, user)
            else:
                await self.xdlib.admin.set_rights(chat, user, perms, rank)
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

    @loader.command(ru_doc="Получить инфу о текущем чате")
    @loader.tag("no_pm")
    async def chatinfo(self, message):
        """Get the current chat info"""
        try:
            chat = await message.get_chat()
            chatinfo = await self.xdlib.chat.get_info(chat)
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
            )
        except Exception as e:
            return await utils.answer(
                message, self.strings["error"].format(error=str(e))
            )

    @loader.command(ru_doc="[-a] - Принять заявки на вступление")
    @loader.tag("no_pm")
    async def approve(self, message):
        """[-a] - Accept join requests"""
        opts = self.xdlib.parse.opts(utils.get_args(message))
        if opts.get("a"):
            await self.xdlib.chat.join_requests(message, True)
            return await utils.answer(message, self.strings["all_approved"])
        args = utils.get_args(message)
        for arg in args:
            if arg.isdigit():
                await self.xdlib.chat.join_request(message, int(arg), True)
            else:
                await self.xdlib.chat.join_request(message, arg, True)
        return await utils.answer(message, self.strings["all_approved"])

    @loader.command(ru_doc="[-a] - Отклонить заявки на вступление")
    @loader.tag("no_pm")
    async def dismiss(self, message):
        """[-a] - Decline join requests"""
        opts = self.xdlib.parse.opts(utils.get_args(message))
        if opts.get("a"):
            await self.xdlib.chat.join_requests(message, False)
            return await utils.answer(message, self.strings["all_dismissed"])
        args = utils.get_args(message)
        for arg in args:
            if arg.isdigit():
                await self.xdlib.chat.join_request(message, int(arg), False)
            else:
                await self.xdlib.chat.join_request(message, arg, False)
        return await utils.answer(message, self.strings["all_dismissed"])
