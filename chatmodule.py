# meta developer: @xdesai
# scope: disable_onload_docs

import logging
from datetime import timedelta, datetime, timezone
from .. import loader, utils
from telethon.tl.functions import channels
from telethon.tl import types
from telethon.tl.functions import messages

logger = logging.getLogger("ChatModule")

@loader.tds
class ChatModuleMod(loader.Module):
    strings = {
        "my_id": "<emoji document_id=5361912768045792571>👑</emoji><b> My ID: </b><code>{id}</code>",
        "name": "ChatModule",
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>Chat ID:</b> <code>{id}</code>",
        "user_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>User's ID:</b> <code>{id}</code>",
        "user_not_participant": "<emoji document_id=5019523782004441717>❌</emoji> <b>User is not in this group.</b>",
        "admin_rights": "<blockquote expandable><emoji document_id=6023985764885338464>📜</emoji> {name} <b>Rights in this chat:\n\n{rights}</b>\n\n<emoji document_id=5287734473775918473>🔼</emoji><b> Promoted by: {promoter_name}</b> [{promoter_id}]</blockquote>",
        "not_an_admin": "<emoji document_id=5019523782004441717>❌</emoji><b> {user} is not an admin.</b>",
        "no_rights": "<emoji document_id=5019523782004441717>❌</emoji> <b>I don't have enough rights :(</b>",
        "no_user": "<emoji document_id=5019523782004441717>❌</emoji> <b>User not found.</b>",
        "change_info": "Change Info",
        "delete_messages": "Delete Messages",
        "other": "Other",
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
        "error": "<emoji document_id=5458497936763676259>😖</emoji><b> Something went wrong. Check the logs.</b>",
        "successful_delete": "<emoji document_id=5021905410089550576>✅</emoji> {chat_type} successfully deleted",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>No deleted accounts found here</b>",
        "kicked_deleted_accounts": "<emoji document_id=5408832111773757273>🗑</emoji> <b>Removed deleted accounts from the chat</b>",
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b>Admins in <code>{title}</code> ({count}):</b>\n",
        "no_admins_in_chat": "<emoji document_id=5458610095539645297>✖️</emoji> <b>No admins in this chat.</b>",
        "bot_list": "<blockquote expandable><emoji document_id=5355051922862653659>🤖</emoji><b> Bots ({count}):\n\n</b>{bots}</blockquote>",
        "no_bots_in_chat": "<emoji document_id=5458610095539645297>✖️</emoji> <b>No bots in this chat.</b>",
        "user_list": "<blockquote expandable><emoji document_id=5408846628763217930>👤</emoji><b> Users ({count}):\n\n{users}</b></blockquote>",
        "no_user_in_chat": "<emoji document_id=5458610095539645297>✖️</emoji> <b>No users in this chat.</b>",
        "user_is_banned": "<emoji document_id=5348402067947929537>🚫</emoji> <b>{name} [<code>{id}</code>] has been banned for{time_info}.</b>",
        "user_is_unbanned": "<emoji document_id=5355277430120523169>👋</emoji> <b>{name} [<code>{id}</code>] has been unbanned.</b>",
        "user_is_kicked": "<emoji document_id=5983033346207256798>🚪</emoji> <b><code>{name}</code> [<code>{id}</code>] has been kicked.</b>",
        "user_is_muted": "<emoji document_id=5409380965644514142>🔕</emoji> <b>{name} [<code>{id}</code>] has been muted for{time_info}.</b>",
        "reason": "<i>Reason: {reason}</i>",
        "forever": "ever",
        "user_is_unmuted": "<emoji document_id=5409331062419502443>🔉</emoji> <b>{name} [<code>{id}</code>] has been unmuted.</b>",
        "title_changed": "<b>The {type_of} title was successfully changed from <code>{old_title}</code> to <code>{new_title}</code>.</b>",
        "channel_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>The channel <code>{title}</code> is created.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Invite link: {link}</b>",
        "group_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>The group <code>{title}</code> is created.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Invite link: {link}</b>",
        "user_blocked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> is blocked.</b>',
        "user_privacy_restricted": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a>\'s privacy settings restrict this action.</b>',
        "user_not_mutual_contact": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> is not a mutual contact.</b>',
        "user_kicked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> is kicked from the chat.</b>',
        "user_invited": "<emoji document_id=5409029658794537988>✅</emoji> <b>User <a href='tg://user?id={id}'>{user}</a> is invited to the chat.</b>",
        "user_not_invited": "<emoji document_id=5019523782004441717>❌</emoji> <b>User could not be invited to the chat.</b>",
        "admin_list": "<blockquote expandable><emoji document_id=5361912768045792571>👑</emoji> <b>The creator is <a href='tg://user?id={id}'>{name}</a>\n\nAdmins ({admins_count}):</b>{admins}</blockquote>",
        "dnd": "<emoji document_id=5384262794306669858>🔕</emoji> <b>Chat muted and archived</b>",
        "dnd_failed": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Failed to mute and archive chat</b>",
        "msg_link": "<emoji document_id=5271604874419647061>🔗</emoji> <b>The message link: {link}</b>",
        "msg_link_failed": "<emoji document_id=5019523782004441717>❌</emoji> <b>Failed to get the link</b>",
        "pinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Pinned the message</b>",
        "pin_failed": "<emoji document_id=5458610095539645297>✖️</emoji><b> Failed to pin the message</b>",
        "unpinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Unpinned the message</b>",
        "unpin_failed": "<emoji document_id=5458610095539645297>✖️</emoji><b> Failed to unpin the message</b>",
        "banned_in_chat": "<emoji document_id=5019523782004441717>❌</emoji> <b>Banned users in <code>{title}</code> ({count}):</b>\n\n",
        "no_banned_in_chat": "<emoji document_id=5251741320690551495>👎</emoji> <b>No banned users in this chat.</b>",
        "type_group": "Group",
        "type_channel": "Channel",
        "type_unknown": "Unknown",
        "yes": "<emoji document_id=5408909562919007848>✅</emoji> Yes",
        "no": "<emoji document_id=5361566877149578396>✖️</emoji> No",
        "chatinfo": "<emoji document_id=5983036958274752500>🔒</emoji><b> Type: {type_of}\n</b><emoji document_id=5985457743576698865>#️⃣</emoji><b> Chat ID: </b><code>{id}</code><b>\n</b><emoji document_id=5408849420491962048>🔥</emoji><b> Title: {title}\n<emoji document_id=5258328383183396223>📖</emoji><b> Forum:</b> {is_forum}\n\n</b><emoji document_id=5870676941614354370>🖋</emoji><b> About: {about}\n\n</b><emoji document_id=5805553606635559688>👑</emoji><b> Admin count: {admins_count}\n</b><emoji document_id=5433648711982921307>✅</emoji><b> Online count: {online_count}\n</b><emoji document_id=6024039683904772353>👤</emoji><b> Participants count: {participants_count}\n</b><emoji document_id=5816617137447376501>🚫</emoji><b> Kicked сount: {kicked_count}\n</b><emoji document_id=5431560533243346887>🔀</emoji><b> Requests pending: {requests_pending}\n\n</b><emoji document_id=5408910404732595664>🕐</emoji><b> Slowmode period: {slowmode_seconds}\n</b><emoji document_id=6019279794988915337>📞</emoji><b> Call: {call}\n</b><emoji document_id=5408832111773757273>🗑</emoji><b> TTL period: {ttl_period}\n</b><emoji document_id=5408846628763217930>👤</emoji><b> Recent requesters: {recent_requesters}\n\n</b><emoji document_id=6021690418398239007>👥</emoji><b> Linked Chat ID: {linked_chat_id}\n</b><emoji document_id=6019328362479097179>🛡</emoji><b> Antispam: {antispam}\n</b><emoji document_id=6024008227564296298>👁</emoji><b> Participants hidden: {participants_hidden}\n\n</b><emoji document_id=6028171274939797252>🔗</emoji><b> Link: {link}</b>",
        "all_approved": "<emoji document_id=5409029658794537988>✅</emoji> <b>Users are approved</b>",
        "all_dismissed": "<emoji document_id=5458610095539645297>✖️</emoji> <b>Requests are dismissed</b>",
        "role_created": "<emoji document_id=5409029658794537988>✅</emoji> <b>The role was successfully created</b>",
        "role_removed": "<emoji document_id=5409029658794537988>✅</emoji> <b>The role was successfully removed</b>",
        "role_not_removed": "<emoji document_id=5458610095539645297>✖️</emoji><b> Failed to remove role</b>",
        "role_set": "<emoji document_id=5409029658794537988>✅</emoji><b> Role successfully assigned to the user</b>",
        "role_not_set": "<emoji document_id=5458610095539645297>✖️</emoji><b> Failed to assign role</b>",
        "all_roles": "<blockquote expandable><emoji document_id=6023985764885338464>📜</emoji><b> All roles:</b>\n\n{roles}</blockquote>",
        "role_info": "<blockquote expandable><emoji document_id=6023985764885338464>📜</emoji> <code>{name}</code> <b>role rights:</b>\n\n{rights}</blockquote>",
        "no_roles": "<emoji document_id=5458610095539645297>✖️</emoji> <b>The roles haven't been created yet</b>",
        "no_role_rights": "<emoji document_id=5458610095539645297>✖️</emoji><b> No rights for this role</b>",
        "promoted": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> is promoted</b>',
        "demoted": "<emoji document_id=5447183459602669338>🔽</emoji> <b><a href='tg://user?id={id}'>{name}</a> is demoted</b>",
    }

    strings_ru = {
        "my_id": "<emoji document_id=5361912768045792571>👑</emoji><b> Мой ID: </b><code>{id}</code>",
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>ID чата:</b> <code>{id}</code>",
        "user_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>ID пользователя:</b> <code>{id}</code>",
        "user_not_participant": "<emoji document_id=5019523782004441717>❌</emoji> <b>Пользователь не состоит в этой группе.</b>",
        "admin_rights": "<blockquote expandable><emoji document_id=6023985764885338464>📜</emoji> <b>Права</b> {name}<b> в этом чате:\n\n{rights}</b>\n\n<emoji document_id=5287734473775918473>🔼</emoji><b> Назначил: {promoter_name}</b> [{promoter_id}]</blockquote>",
        "not_an_admin": "<emoji document_id=5019523782004441717>❌</emoji><b> {user} не является админом.</b>",
        "no_rights": "<emoji document_id=5019523782004441717>❌</emoji> <b>У меня недостаточно прав :(</b>",
        "no_user": "<emoji document_id=5019523782004441717>❌</emoji> <b>Пользователь не найден.</b>",
        "change_info": "Изменение информации",
        "post_messages": "Публикация сообщений",
        "edit_messages": "Редактирование сообщений",
        "delete_messages": "Удаление сообщений",
        "ban_users": "Бан пользователей",
        "invite_users": "Приглашение пользователей",
        "pin_messages": "Закрепление сообщений",
        "add_admins": "Назначение админов",
        "anonymous": "Анонимность",
        "manage_call": "Управление звонками",
        "other": "Другое",
        "post_stories": "Публикация историй",
        "edit_stories": "Редактирование историй",
        "delete_stories": "Удаление историй",
        "manage_topics": "Управление темами",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>Неверные аргументы.</b>",
        "error": "<emoji document_id=5458497936763676259>😖</emoji><b> Что-то пошло не так. Проверьте логи.</b>",
        "successful_delete": "<emoji document_id=5021905410089550576>✅</emoji> {chat_type} успешно удалён",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>Удалённые аккаунты не найдены</b>",
        "kicked_deleted_accounts": "<emoji document_id=5408832111773757273>🗑</emoji> <b>Удаленные аккаунты исключены из чата</b>",
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b>Админы в <code>{title}</code> ({count}):</b>\n",
        "no_admins_in_chat": "<emoji document_id=5458610095539645297>✖️</emoji> <b>В чате нет админов.</b>",
        "bot_list": "<blockquote expandable><emoji document_id=5355051922862653659>🤖</emoji><b> Боты ({count}):\n\n</b>{bots}</blockquote>",
        "no_bots_in_chat": "<emoji document_id=5458610095539645297>✖️</emoji> <b>В чате нет ботов</b>",
        "user_list": "<blockquote expandable><emoji document_id=5408846628763217930>👤</emoji><b> Участники ({count}):\n\n{users}</b></blockquote>",
        "no_user_in_chat": "<emoji document_id=5458610095539645297>✖️</emoji> <b>В чате нет пользователей.</b>",
        "user_is_banned": "<emoji document_id=5348402067947929537>🚫</emoji> <b>{name} [<code>{id}</code>] забанен на{time_info}.</b>",
        "user_is_unbanned": "<emoji document_id=5355277430120523169>👋</emoji> <b>{name} [<code>{id}</code>] разбанен.</b>",
        "user_is_kicked": "<emoji document_id=5983033346207256798>🚪</emoji> <b><code>{name}</code> [<code>{id}</code>] был кикнут.</b>",
        "user_is_muted": "<emoji document_id=5409380965644514142>🔕</emoji> <b>{name} [<code>{id}</code>] замучен на{time_info}.</b>",
        "reason": "<i>Причина: {reason}</i>",
        "forever": "всегда",
        "user_is_unmuted": "<emoji document_id=5409331062419502443>🔉</emoji> <b>{name} [<code>{id}</code>] размучен.</b>",
        "title_changed": "<b>{type_of} успешно переименован с <code>{old_title}</code> на <code>{new_title}</code>.</b>",
        "channel_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>Канал <code>{title}</code> создан.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Ссылка: {link}</b>",
        "group_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>Группа <code>{title}</code> создана.\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> Ссылка: {link}</b>",
        "user_blocked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> заблокирован.</b>',
        "user_privacy_restricted": '<emoji document_id=5019523782004441717>❌</emoji> <b>Настройки конфиденциальности <a href="tg://user?id={user_id}">{user}</a> ограничивают это действие.</b>',
        "user_not_mutual_contact": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> не является взаимным контактом.</b>',
        "user_kicked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> кикнут из чата.</b>',
        "user_invited": "<emoji document_id=6296367896398399651>✅</emoji> <b>Пользователь <a href='tg://user?id={id}'>{user}</a> приглашён в чат.</b>",
        "user_not_invited": "<emoji document_id=5019523782004441717>❌</emoji> <b>Пользователя не удалось пригласить в чат.</b>",
        "admin_list": "<blockquote expandable><emoji document_id=5361912768045792571>👑</emoji> <b>Создатель чата <a href='tg://user?id={id}'>{name}</a>\n\nАдмины ({admins_count}):\n</b>{admins}</blockquote>",
        "dnd": "<emoji document_id=5384262794306669858>🔕</emoji> <b>Чат отключён и архивирован</b>",
        "dnd_failed": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Не удалось отключить и архивировать чат</b>",
        "msg_link": "<emoji document_id=5271604874419647061>🔗</emoji> <b>Ссылка на сообщение: {link}</b>",
        "msg_link_failed": "<emoji document_id=5019523782004441717>❌</emoji> <b>Не удалось получить ссылку</b>",
        "pinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Сообщение закреплено</b>",
        "pin_failed": "<emoji document_id=5458610095539645297>✖️</emoji><b> Не удалось закрепить сообщение</b>",
        "unpinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Сообщение откреплено</b>",
        "unpin_failed": "<emoji document_id=5458610095539645297>✖️</emoji><b> Не удалось открепить сообщение</b>",
        "banned_in_chat": "<emoji document_id=5019523782004441717>❌</emoji> <b>Забаненные пользователи в <code>{title}</code> ({count}):</b>\n\n",
        "no_banned_in_chat": "<emoji document_id=5251741320690551495>👎</emoji> <b>В этом чате нет забаненных пользователей.</b>",
        "type_group": "Группа",
        "type_channel": "Канал",
        "type_unknown": "Неизвестно",
        "yes": "<emoji document_id=5408909562919007848>✅</emoji> Есть",
        "no": "<emoji document_id=5361566877149578396>✖️</emoji> Нет",
        "chatinfo": "<emoji document_id=5983036958274752500>🔒</emoji><b> Тип: {type_of}\n</b><emoji document_id=5985457743576698865>#️⃣</emoji><b> ID чата: </b><code>{id}</code><b>\n</b><emoji document_id=5408849420491962048>🔥</emoji><b> Название: {title}\n<emoji document_id=5258328383183396223>📖</emoji><b> Форум:</b> {is_forum}\n\n</b><emoji document_id=5870676941614354370>🖋</emoji><b> Описание: {about}\n\n</b><emoji document_id=5805553606635559688>👑</emoji><b> Кол-во админов: {admins_count}\n</b><emoji document_id=5433648711982921307>✅</emoji><b> Онлайн: {online_count}\n</b><emoji document_id=6024039683904772353>👤</emoji><b> Участников: {participants_count}\n</b><emoji document_id=5816617137447376501>🚫</emoji><b> Заблокировано: {kicked_count}\n</b><emoji document_id=5431560533243346887>🔀</emoji><b> Ожидающие запросы: {requests_pending}\n\n</b><emoji document_id=5408910404732595664>🕐</emoji><b> Период замедления: {slowmode_seconds}\n</b><emoji document_id=6019279794988915337>📞</emoji><b> Звонок: {call}\n</b><emoji document_id=5408832111773757273>🗑</emoji><b> Период TTL: {ttl_period}\n</b><emoji document_id=5408846628763217930>👤</emoji><b> Последние запросы: {recent_requesters}\n\n</b><emoji document_id=6021690418398239007>👥</emoji><b> Связанный ID чата: {linked_chat_id}\n</b><emoji document_id=6019328362479097179>🛡</emoji><b> Антиспам: {antispam}\n</b><emoji document_id=6024008227564296298>👁</emoji><b> Участники скрыты: {participants_hidden}\n\n</b><emoji document_id=6028171274939797252>🔗</emoji><b> Ссылка: {link}</b>",
        "all_approved": "<emoji document_id=5409029658794537988>✅</emoji> <b>Пользователи одобрены</b>",
        "all_dismissed": "<emoji document_id=5458610095539645297>✖️</emoji> <b>Запросы отклонены</b>",
        "role_created": "<emoji document_id=5409029658794537988>✅</emoji> <b>Роль успешно создана</b>",
        "role_removed": "<emoji document_id=5409029658794537988>✅</emoji> <b>Роль была успешно удалена</b>",
        "role_not_removed": "<emoji document_id=5458610095539645297>✖️</emoji><b> Не удалось удалить роль</b>",
        "role_set": "<emoji document_id=5409029658794537988>✅</emoji><b> Роль успешно назначена пользователю</b>",
        "role_not_set": "<emoji document_id=5458610095539645297>✖️</emoji><b> Не удалось назначить роль</b>",
        "all_roles": "<emoji document_id=6023985764885338464>📜</emoji><b> Все роли:</b>\n\n{roles}",
        "role_info": "<emoji document_id=6023985764885338464>📜</emoji><b> Права роли <code>{name}</code>:</b>\n\n{rights}",
        "no_roles": "<emoji document_id=5458610095539645297>✖️</emoji> <b>Роли еще не созданы</b>",
        "no_role_rights": "<emoji document_id=5458610095539645297>✖️</emoji><b> Нет прав для этой роли</b>",
        "promoted": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> назначен администратором</b>',
        "demoted": "<emoji document_id=5447183459602669338>🔽</emoji> <b><a href='tg://user?id={id}'>{name}</a> снят с роли администратора</b>",

    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self.xdlib = await self.import_lib(
            "https://mods.xdesai.top/xdlib.py",
            suspend_on_error=True,
        )
        self._roles = self.xdlib._db.pointer(self.__class__.__name__, "ChatModule_Roles", {})
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
        if reply and not getattr(reply, "is_private") and not getattr(reply, "sender_id") == self.tg_id:
            user_id = (await reply.get_sender()).id
            ids.append(self.strings["user_id"].format(id=user_id))
        return await utils.answer(
            message, "\n".join(ids)
        )

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
            return await utils.answer(message, self.strings["not_an_admin"].format(user=user.first_name))
        if participant.admin_rights:
            can_do = []
            rights = participant.to_dict().get("admin_rights")
            for right, is_permitted in rights.items():
                if right == "_":
                    continue
                if is_permitted:
                    can_do.append(right)
            promoter = await self._client.get_entity(participant.promoted_by)
            return await utils.answer(message, self.strings["admin_rights"].format(rights="\n".join([f"<emoji document_id=5409029658794537988>✅</emoji> {self.strings[right]}" for right in can_do]), promoter_id=promoter.id, promoter_name=promoter.first_name, name=user.first_name))
        return await utils.answer(message, self.strings["not_an_admin"].format(user=user.first_name))

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
            return await utils.answer(
                message, self.strings["successful_delete"]
            )
        if isinstance(message.chat, types.Channel):
            await self._client(channels.DeleteChannelRequest(message.chat))
        elif isinstance(message.chat, types.Chat):
            await self._client(messages.DeleteChatRequest(message.chat))
        else:
            return await utils.answer(message, self.strings["failed_to_delete"])
        return await utils.answer(message, self.strings["successful_delete"])

    @loader.command(ru_doc="Очищает группу/канал от удаленных аккаунтов")
    @loader.tag("no_pm")
    async def flush(self, message):
        """Removes deleted accounts from the chat/channel"""
        chat = await message.get_chat()

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings["no_rights"])

        deleted = self.xdlib.chat.get_deleted(chat)
        if not deleted:
            return await utils.answer(message, self.strings["no_deleted_accounts"])
        for to_delete in deleted:
            try:
                await self.kick_participant(chat, to_delete)
            except Exception:
                logger.error(f"Couldn't kick {to_delete.id} from the chat {chat.id}")
        return await utils.answer(message, self.strings["kicked_deleted_accounts"])


    @loader.command(ru_doc="Показывает админов в группе/канале")
    @loader.tag("no_pm")
    async def admins(self, message):
        """Shows the admins in the chat/channel"""
        admins = await self.xdlib.chat.get_admins(message.chat, True)
        creator = await self.xdlib.chat.get_creator(message.chat)
        return await utils.answer(message, self.strings["admin_list"].format(
            id=creator.id if creator else 0,
            name=creator.first_name if creator else self.strings["no"],
            admins_count=len(admins) or 0,
            admins="\n".join(f"<emoji document_id=5774022692642492953>✅</emoji> <a href='tg://user?id={admin.id}'>{admin.first_name}</a> [<code>{admin.id}</code>] / <code>{admin.participant.rank}</code>" for admin in admins) if admins else f"\n{self.strings['no_admins_in_chat']}"
        ))

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
        await utils.answer(message, self.strings["bot_list"].format(
            count=len(bots),
            bots="\n".join([f"<emoji document_id=5774022692642492953>✅</emoji> <a href='tg://user?id={bot.id}'>{bot.first_name}</a> [<code>{bot.id}</code>]" for bot in bots])
        ))

    @loader.command(ru_doc="Показывает простых участников чата/канала")
    @loader.tag("no_pm")
    async def users(self, message):
        """Shows the users in the chat/channel"""
        users = await self.xdlib.chat.get_members(message.chat)
        if not users:
            return await utils.answer(message, self.strings["no_user_in_chat"])
        await utils.answer(message, self.strings["user_list"].format(
            count=len(users),
            users="\n".join([f"<emoji document_id=5774022692642492953>✅</emoji> <a href='tg://user?id={user.id}'>{user.first_name}</a> [<code>{user.id}</code>]" for user in users])
        ))

    @loader.command(ru_doc="Забанить участника")
    @loader.tag("no_pm")
    async def ban(self, message):
        """Ban a participant temporarily or permanently"""
        text = message.text.split("\n", 1)
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        user = next(iter(self.xdlib.parse.mentions(message)), None) or reply.sender_id or None
        strings = []
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
        if not user:
            return await utils.answer(message, self.strings["no_user"])

        seconds = self.xdlib.parse.time(utils.get_args_raw(message))
        until_date = datetime.now(timezone.utc) + timedelta(seconds=seconds)
        time_info = f" {self.xdlib.format.time(seconds)}" if seconds else None
        try:
            await self._client.edit_permissions(
                message.chat, user, until_date=until_date if seconds else None, view_messages=False
            )
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
        strings.append(self.strings["user_is_banned"].format(id=user.id, name=getattr(user, "first_name") or getattr(user, "title"), time_info=time_info or self.strings["forever"]))

        if reason:
            strings.append(self.strings["reason"].format(reason=reason))
        return await utils.answer(
                message,
                "\n".join(strings)
            )

    @loader.command(ru_doc="Разбанить пользователя")
    @loader.tag("no_pm")
    async def unban(self, message):
        """Unban a user"""
        reply = await message.get_reply_message()
        user = next(iter(self.xdlib.parse.mentions(message)), None) or reply.sender_id or None
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        try:
            await self._client.edit_permissions(message.chat, user, view_messages=True)
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
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
        user = next(iter(self.xdlib.parse.mentions(message)), None) or reply.sender_id or None
        strings = []
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
        if not user:
            return await utils.answer(message, self.strings["no_user"])
        try:
            await self._client.kick_participant(message.chat, user)
        except Exception as e:
            logging.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
        strings.append(self.strings["user_is_kicked"].format(
                    id=user.id,
                    name=getattr(user, "first_name") or getattr(user, "title"),
                ))
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
        user = next(iter(self.xdlib.parse.mentions(message)), None) or reply.sender_id or None
        strings = []
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
        if not user:
            return await utils.answer(message, self.strings["no_user"])

        seconds = self.xdlib.parse.time(utils.get_args_raw(message))
        until_date = datetime.now(timezone.utc) + timedelta(seconds=seconds)
        time_info = f" {self.xdlib.format.time(seconds)}" if seconds else None
        try:
            await self._client.edit_permissions(
                message.chat, user, until_date=until_date if seconds else None, send_messages=False
            )
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
        strings.append(self.strings["user_is_muted"].format(id=user.id, name=getattr(user, "first_name") or getattr(user, "title"), time_info=time_info or self.strings["forever"]))

        if reason:
            strings.append(self.strings["reason"].format(reason=reason))
        return await utils.answer(
                message,
                "\n".join(strings)
            )

    @loader.command(ru_doc="Размутить участника")
    @loader.tag("no_pm")
    async def unmute(self, message):
        """Unmute a participant"""
        reply = await message.get_reply_message()
        user = next(iter(self.xdlib.parse.mentions(message)), None) or reply.sender_id or None
        try:
            user = await self._client.get_entity(user) if user else None
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
        if not user:
            return await utils.answer(message, self.strings["no_user"])

        try:
            await self._client.edit_permissions(message.chat, user, send_messages=True)
        except Exception as e:
            logger.error(str(e))
            return await utils.answer(
                message, self.strings["error"]
            )
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

    @loader.command(ru_doc="[-g|--group name] [-c|--channel name] - Создать группу/канал")
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
            chat = self.xdlib.chat.get_info(result.chats[0])
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
            link = await reply.link if __package__.startswith("legacy") else await reply.link()
            return await utils.answer(
                message, self.strings["msg_link"].format(link=link)
            )
        return await utils.answer(message, self.strings["msg_link_failed"])

    @loader.command(ru_doc="-u username/id - Пригласить пользователя в чат (-b пригласить инлайн бота)")
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
        invited = self.xdlib.chat.invite_user(message.chat, user)
        if invited:
            return await utils.answer(message, self.strings["user_invited"].format(
                        user=entity.first_name, id=entity.id
                    ))
        return await utils.answer(message, self.strings["user_not_invited"])

    @loader.command(
        ru_doc="-n название_роли -p число - Создать роль"
    )
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
                message, f"{await self.xdlib.admin.get_rights_table()}"
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
            await self.xdlib.admin.set_rights(message.chat, user, rights.to_int(), rank=rank)
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
            return await utils.answer(message, self.strings["all_roles"].format(roles="\n".join([f"<emoji document_id=5807829874877930085>➡️</emoji> <code>{role}</code>" for role in roles.keys()])))
        rights = []
        for right, permitted in self.xdlib.rights.from_int(roles[selected_role]).to_dict().items():
            if permitted:
                rights.append(right)
                continue

        return await utils.answer(message, self.strings["role_info"].format(name=selected_role, rights=(
            "\n".join([f"<emoji document_id=5409029658794537988>✅</emoji> <code>{self.strings[right]}</code>" for right in rights]) if rights else self.strings["no_role_rights"]
        )))

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
        role_set = await self.xdlib.admin.set_rights(message.chat, user, self._roles[role], rank=rank)
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
                    is_forum=self.strings["yes"] if chatinfo.get("is_forum") else self.strings["no"],
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
