# meta developer: @xdesai

from datetime import timedelta
import asyncio
import re
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
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b>Admins in <code>{title}</code> ({count}):</b>\n\n",
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
        "creator": "<emoji document_id=5433758796289685818>👑</emoji> <b>The creator is <a href='tg://user?id={id}'>{creator}</a>.</b>",
        "no_creator": "<emoji document_id=5019523782004441717>❌</emoji> <b>No creator found.</b>",
        "promoted_fullrights": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> is promoted with fullrights</b>',
        "demoted": "<emoji document_id=5447183459602669338>🔽</emoji> <b><a href='tg://user?id={id}'>{name}</a> is demoted</b>",
        "dnd": "<emoji document_id=5384262794306669858>🔕</emoji> <b>Chat muted and archived</b>",
        "dnd_failed": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Failed to mute and archive chat</b>",
        "msg_link": "<emoji document_id=5271604874419647061>🔗</emoji> <b>The message link: {link}</b>",
        "msg_link_failed": "<emoji document_id=5019523782004441717>❌</emoji> <b>Failed to get the link</b>",
        "pinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Pinned the message</b>",
        "unpinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Unpinned the message</b>",
        "promoted_moder": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> has been promoted without rights</b>',
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
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b>Админы в <code>{title}</code> ({count}):</b>\n\n",
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
        "creator": "<emoji document_id=5433758796289685818>👑</emoji> <b>Создатель: <a href='tg://user?id={id}'>{creator}</a>.</b>",
        "no_creator": "<emoji document_id=5019523782004441717>❌</emoji> <b>Создатель не найден.</b>",
        "promoted_fullrights": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> повышен с полными правами</b>',
        "demoted": "<emoji document_id=5447183459602669338>🔽</emoji> <b><a href='tg://user?id={id}'>{name}</a> снят с роли администратора</b>",
        "dnd": "<emoji document_id=5384262794306669858>🔕</emoji> <b>Чат отключён и архивирован</b>",
        "dnd_failed": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Не удалось отключить и архивировать чат</b>",
        "msg_link": "<emoji document_id=5271604874419647061>🔗</emoji> <b>Ссылка на сообщение: {link}</b>",
        "msg_link_failed": "<emoji document_id=5019523782004441717>❌</emoji> <b>Не удалось получить ссылку</b>",
        "pinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Сообщение закреплено</b>",
        "unpinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>Сообщение откреплено</b>",
        "promoted_moder": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> повышен без прав</b>',
    }

    strings_jp = {
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>チャットID:</b> <code>{chat_id}</code>",
        "user_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>ユーザーID:</b> <code>{user_id}</code>",
        "user_not_participant": "<emoji document_id=5019523782004441717>❌</emoji> <b>このグループにユーザーはいません。</b>",
        "_": '<b><a href="tg://user?id={id}">{name}</a>のこのチャットでの権限',
        "not_an_admin": "<emoji document_id=5019523782004441717>❌</emoji> {user} は管理者ではありません。",
        "no_rights": "<emoji document_id=5019523782004441717>❌</emoji> <b>私の権限が十分ではありません :(</b>",
        "no_user": "<emoji document_id=5019523782004441717>❌</emoji> <b>ユーザーが見つかりません。</b>",
        "change_info": "<emoji document_id=6296367896398399651>✅</emoji> Change Info",
        "delete_messages": "<emoji document_id=6296367896398399651>✅</emoji> Delete Messages",
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
        "other": "<emoji document_id=6296367896398399651>✅</emoji> Other",
        "promoted_by": "<emoji document_id=5287734473775918473>🔼</emoji> 昇進させた人: <a href='tg://user?id={id}'>{name}</a> [<code>{id}</code>]",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>無効な引数です。</b>",
        "error": "<b>エラー:</b> <code>{error}</code>",
        "of_chat": "チャット",
        "of_channel": "チャンネル",
        "loading": "<emoji document_id=5021712394259268143>🟡</emoji> <b>データを読み込み中...</b>",
        "own_list": "<b>私の所有物 ({count}):</b>\n\n{msg}",
        "no_ownerships": "<emoji document_id=5019523782004441717>❌</emoji> <b>所有物がありません。</b>",
        "successful_delete": "<emoji document_id=5021905410089550576>✅</emoji> {chat_type} を正常に削除しました",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>削除されたアカウントは見つかりません</b>",
        "kicked_deleted_accounts": "<emoji document_id=5328302454226298081>🫥</emoji> <b>{count} 件の削除されたアカウントを削除しました</b>",
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b><code>{title}</code> の管理者 ({count}):</b>\n\n",
        "no_admins_in_chat": "<b>このチャットに管理者がいません。</b>",
        "bots_in_chat": "<emoji document_id=5276127848644503161>🤖</emoji> <b><code>{title}</code> のボット ({count}):</b>\n\n",
        "no_bots_in_chat": "<b>このチャットにボットはいません。</b>",
        "users_in_chat": "<emoji document_id=5275979556308674886>👤</emoji> <b><code>{title}</code> のユーザー ({count}):</b>\n\n",
        "no_user_in_chat": "<b>このチャットにユーザーはいません。</b>",
        "user_is_banned": "⛔️ <b>{name} [<code>{id}</code>] は {time_info} の間禁止されました。</b>",
        "user_is_banned_with_reason": "⛔️ <b>{name} [<code>{id}</code>] は {time_info} の間禁止されました。</b>\n<i>理由: {reason}</i>",
        "user_is_banned_forever": "⛔️ <b>{name} [<code>{id}</code>] は永久に禁止されました。</b>",
        "user_is_banned_forever_with_reason": "⛔️ <b>{name} [<code>{id}</code>] は永久に禁止されました。</b>\n<i>理由: {reason}</i>",
        "user_is_unbanned": "👋🏻 <b>{name} [<code>{id}</code>] の禁止を解除しました。</b>",
        "user_is_kicked": "🍃 <b><code>{name}</code> [<code>{id}</code>] をキックしました。</b>",
        "user_is_kicked_with_reason": "🍃 <b><code>{name}</code> [<code>{id}</code>] をキックしました。</b>\n<i>理由: {reason}</i>",
        "user_is_muted_with_reason": "🔇 <b>{name} [<code>{id}</code>] は {time_info} の間ミュートされました。</b>\n<i>理由: {reason}</i>",
        "user_is_muted": "🔇 <b>{name} [<code>{id}</code>] は {time_info} の間ミュートされました。</b>",
        "user_is_muted_with_reason_forever": "🔇 <b>{name} [<code>{id}</code>] は永久にミュートされました。</b>\n<i>理由: {reason}</i>",
        "user_is_muted_forever": "🔇 <b>{name} [<code>{id}</code>] は永久にミュートされました。</b>",
        "user_is_unmuted": "🔊 <b>{name} [<code>{id}</code>] のミュートを解除しました。</b>",
        "chat_muted": "🔇 <b>このチャットは参加者にミュートされました。</b>",
        "chat_unmuted": "✅ <b>このチャットは再び開かれました。</b>",
        "title_changed": "<b>{type_of} のタイトルを <code>{old_title}</code> から <code>{new_title}</code> に変更しました。</b>",
        "channel_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>チャンネル <code>{title}</code> が作成されました。\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> 招待リンク: {link}</b>",
        "group_created": "<emoji document_id=6296367896398399651>✅</emoji> <b>グループ <code>{title}</code> が作成されました。\n</b><emoji document_id=5237918475254526196>🔗</emoji><b> 招待リンク: {link}</b>",
        "user_blocked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> はブロックされています。</b>',
        "user_privacy_restricted": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> のプライバシー設定により、このアクションが制限されています。</b>',
        "user_not_mutual_contact": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> は相互連絡先ではありません。</b>',
        "user_kicked": '<emoji document_id=5019523782004441717>❌</emoji> <b><a href="tg://user?id={user_id}">{user}</a> をキックしました。</b>',
        "user_invited": "<emoji document_id=6296367896398399651>✅</emoji> <b>ユーザー <a href='tg://user?id={id}'>{user}</a> がチャットに招待されました。</b>",
        "creator": "<emoji document_id=5433758796289685818>👑</emoji> <b>クリエイター: <a href='tg://user?id={id}'>{creator}</a>.</b>",
        "no_creator": "<emoji document_id=5019523782004441717>❌</emoji> <b>クリエイターが見つかりません。</b>",
        "promoted_fullrights": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> がフル権限で昇進しました</b>',
        "demoted": "<emoji document_id=5447183459602669338>🔽</emoji> <b><a href='tg://user?id={id}'>{name}</a>が降格されました",
        "dnd": "<emoji document_id=5384262794306669858>🔕</emoji> <b>チャットをミュートしてアーカイブしました</b>",
        "dnd_failed": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>チャットのミュートとアーカイブに失敗しました</b>",
        "msg_link": "<emoji document_id=5271604874419647061>🔗</emoji> <b>メッセージリンク: {link}</b>",
        "msg_link_failed": "<emoji document_id=5019523782004441717>❌</emoji> <b>リンクの取得に失敗しました</b>",
        "pinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>メッセージを固定しました</b>",
        "unpinned": "<emoji document_id=6296367896398399651>✅</emoji> <b>メッセージの固定を解除しました</b>",
        "promoted_moder": '<emoji document_id=5433758796289685818>👑</emoji> <b><a href="tg://user?id={id}">{name}</a> は権限なしで昇進しました</b>',
    }

    @loader.command(ru_doc="[reply] - Узнать ID", jp_doc="[reply] - IDを知る")
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
        jp_doc="[reply/username/id] - ユーザーの管理者権限を確認する",
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
                participant_id = await utils.get_target(message)
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

    @loader.command(ru_doc="Покинуть чат", jp_doc="チャットから離脱する")
    @loader.tag("no_pm")
    async def leave(self, message):
        """Leave chat"""
        await message.delete()
        await self._client(channels.LeaveChannelRequest((await message.get_chat()).id))

    @loader.command(
        ru_doc="[a[1-100] b[1-100]] | [reply] Удалить сообщения",
        jp_doc="[a[1-100] b[1-100]] | [reply] メッセージを削除する",
    )
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
                    return await utils.answer(message, self.strings["invalid_args"])
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
                        reply.chat_id, max_id=reply.id, limit=count
                    )
                    ids.extend([msg.id for msg in messages])
                else:
                    return await utils.answer(message, self.strings["invalid_args"])
                try:
                    await self._client.delete_messages(reply.chat_id, ids)
                except Exception as e:
                    await utils.answer(
                        message, self.strings["error"].format(error=str(e))
                    )
        else:
            if reply:
                try:
                    await reply.delete()
                except:
                    return
            else:
                return

    @loader.command(
        ru_doc="Показывает список чатов, каналов и групп где вы админ/владелец",
        jp_doc="管理者であるかオーナーであるかのチャット、チャンネル、グループの一覧を表示する",
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

    @loader.command(
        ru_doc="[reply] - Закрепить сообщение",
        jp_doc="[reply] - メッセージを固定する",
    )
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

    @loader.command(
        ru_doc="Открепить сообщение",
        jp_doc="メッセージの固定を解除する",
    )
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

    @loader.command(
        ru_doc="[link/id] Удаляет группу/канал",
        jp_doc="[link/id] グループ・チャンネルを削除する",
    )
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

    @loader.command(
        ru_doc="Очищает группу/канал от удаленных аккаунтов",
        jp_doc="グループ・チャンネルから削除されたアカウントを削除する",
    )
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

    @loader.command(
        ru_doc="Показывает админов в группе/канале",
        jp_doc="グループ・チャンネルの管理者を表示する",
    )
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
        creator = ""
        admins_header = self.strings["admins_in_chat"].format(
            title=title, count=len(real_members)
        )
        if len(real_members) == 0:
            return await utils.answer(message, "no_admins_in_chat")
        for user in real_members:
            if hasattr(user, "participant") and isinstance(
                user.participant, types.ChannelParticipantCreator
            ):
                creator += self.strings["creator"].format(
                    id=user.id, creator=user.first_name
                ) + "\n"
                continue
            else:
                admins_header += f'<emoji document_id=5316712579467321913>🔴</emoji> <a href="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
        return await utils.answer(
            message,
            f"<blockquote expandable><b>{creator}</b>\n<b>{admins_header}</b></blockquote>",
        )

    @loader.command(
        ru_doc="Показывает ботов в группе/канале",
        jp_doc="グループ・チャンネルのボットを表示する",
    )
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

    @loader.command(
        ru_doc="Показывает простых участников чата/канала",
        jp_doc="グループ・チャンネルのユーザーを表示する",
    )
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

    @loader.command(
        ru_doc="Забанить участника", jp_doc="ユーザーを一時的または永久に禁止する"
    )
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
                user = await self._client.get_entity(await utils.get_target(message))
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )
        if not user:
            return await utils.answer(message, self.strings["invalid_args"])

        time_match = re.search(r"(\d+)\s*(mo|y|w|d|h|m)", args)
        chat = await message.get_chat()
        if time_match:
            duration_str = time_match.group(0)
            until_date = self.parse_time(duration_str)
            time_info = self.parse_time_info(duration_str)

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
                        name=user.first_name,
                        reason=reason,
                        time_info=time_info[0],
                    ),
                )
            return await utils.answer(
                message,
                self.strings["user_is_banned"].format(
                    id=user.id, name=user.first_name, time_info=time_info[0]
                ),
            )

        await self._client.edit_permissions(chat, user, view_messages=False)

        if reason:
            return await utils.answer(
                message,
                self.strings["user_is_banned_forever_with_reason"].format(
                    id=user.id,
                    name=user.first_name,
                    reason=reason,
                ),
            )
        return await utils.answer(
            message,
            self.strings["user_is_banned_forever"].format(
                id=user.id, name=user.first_name
            ),
        )

    @loader.command(ru_doc="Разбанить пользователя", jp_doc="ユーザーを解除する")
    @loader.tag("no_pm")
    async def unban(self, message):
        """Unban a user"""
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            try:
                user = await self._client.get_entity(await utils.get_target(message))
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
            self.strings["user_is_unbanned"].format(id=user.id, name=user.first_name),
        )

    @loader.command(ru_doc="Кикнуть участника", jp_doc="ユーザーをキックする")
    @loader.tag("no_pm")
    async def kick(self, message):
        """Kick a participant"""
        reply = await message.get_reply_message()
        reason = ""
        user = None
        if "\n" in message.text:
            reason = message.text.split("\n", 1)[1]
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            try:
                user = await self._client.get_entity(await utils.get_target(message))
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
                self.strings["user_is_kicked"].format(id=user.id, name=user.first_name),
            )
            if not reason
            else await utils.answer(
                message,
                self.strings["user_is_kicked_with_reason"].format(
                    id=user.id, name=user.first_name, reason=reason
                ),
            )
        )

    @loader.command(
        ru_doc="Замутить участника", jp_doc="ユーザーを一時的または永久にミュートする"
    )
    @loader.tag("no_pm")
    async def mute(self, message):
        """Mute a participant temporarily or permanently"""
        text = message.text.split("\n", 1)
        args = utils.get_args_raw(message)
        reason = text[1] if len(text) > 1 else ""
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            try:
                user = await self._client.get_entity(await utils.get_target(message))
            except Exception as e:
                return await utils.answer(
                    message, self.strings["error"].format(error=str(e))
                )
        if not user:
            return await utils.answer(message, self.strings["invalid_args"])

        time_match = re.search(r"(\d+)\s*(mo|y|w|d|h|m)", args)
        chat = await message.get_chat()
        if time_match:
            duration_str = time_match.group(0)
            until_date = self.parse_time(duration_str)
            time_info = self.parse_time_info(duration_str)

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
                        name=user.first_name,
                        reason=reason,
                        time_info=time_info[0],
                    ),
                )
            return await utils.answer(
                message,
                self.strings["user_is_muted"].format(
                    id=user.id, name=user.first_name, time_info=time_info[0]
                ),
            )

        await self._client.edit_permissions(chat, user, send_messages=False)

        if reason:
            return await utils.answer(
                message,
                self.strings["user_is_muted_with_reason_forever"].format(
                    id=user.id,
                    name=user.first_name,
                    reason=reason,
                ),
            )
        return await utils.answer(
            message,
            self.strings["user_is_muted_forever"].format(
                id=user.id, name=user.first_name
            ),
        )

    @loader.command(ru_doc="Размутить участника", jp_doc="ユーザーをミュートを解除する")
    @loader.tag("no_pm")
    async def unmute(self, message):
        """Unmute a participant"""
        reply = await message.get_reply_message()
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        else:
            try:
                user = await self._client.get_entity(await utils.get_target(message))
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
            self.strings["user_is_unmuted"].format(id=user.id, name=user.first_name),
        )

    @loader.command(
        ru_doc="Закрыть чат для всех кроме админов",
        jp_doc="チャットを管理者以外のユーザーに限定して閉じる",
    )
    @loader.tag("no_pm")
    async def mc(self, message):
        """Mute the chat for everyone except admins"""
        chat = await message.get_chat()
        current = chat.default_banned_rights
        is_muted = current.send_messages is True
        try:
            await self._client(
                messages.EditChatDefaultBannedRightsRequest(
                    chat,
                    types.ChatBannedRights(until_date=0, send_messages=not is_muted),
                )
            )
        except Exception as e:
            return await utils.answer(
                message, self.strings["error"].format(error=str(e))
            )
        if is_muted:
            return await utils.answer(message, self.strings["chat_unmuted"])
        else:
            return await utils.answer(message, self.strings["chat_muted"])

    @loader.command(
        ru_doc="Переименовать группу/канал",
        jp_doc="グループ・チャンネルの名前を変更する",
    )
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

    @loader.command(
        ru_doc="[g/c] [title] - Создать группу/канал",
        jp_doc="[g/c] [title] - グループ・チャンネルを作成する",
    )
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
        jp_doc="チャットをミュートしてアーカイブします",
    )
    async def dnd(self, message):
        """Mutes and archives the current chat"""
        dnd = await utils.dnd(self._client, await message.get_chat())
        if dnd:
            return await utils.answer(message, self.strings["dnd"])
        else:
            return await utils.answer(message, self.strings["dnd_failed"])

    @loader.command(
        ru_doc="Получить ссылку на сообщение", jp_doc="メッセージへのリンクを取得する"
    )
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

    @loader.command(
        ru_doc="Пригласить пользователя в чат", jp_doc="ユーザーをチャットに招待する"
    )
    async def invite(self, message):
        """Invite a user to the chat"""
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if reply:
            user = await self._client.get_entity(reply.sender_id)
            result = await self.invite_user(message, chat, user)
            if result:
                return result
        elif args:
            for user in args:
                entity = await self._client.get_entity(
                    int(user) if user.isdigit() else user
                )
                result = await self.invite_user(message, chat, entity)
                if result:
                    return result
        else:
            return await utils.answer(message, self.strings["no_user"])

    @loader.command(
        ru_doc="[reply/username/id] - Выдать админку без прав",
        jp_doc="[reply/username/id] - 権限なしで参加者を昇格させる",
    )
    @loader.tag("no_pm")
    async def moder(self, message):
        """Promote a participant without rights"""
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if reply and args:
            user = await self._client.get_entity(reply.sender_id)
            rank = " ".join(args)
        elif reply:
            user = await self._client.get_entity(reply.sender_id)
            rank = "admin" if not user.bot else "bot"
        elif args:
            user = await self._client.get_entity(await utils.get_target(message))
            if len(args) >= 2:
                rank = " ".join(args[1:])
            else:
                rank = "admin" if not user.bot else "bot"
        else:
            return await utils.answer(message, self.strings["no_user"])
        try:
            await self._client(
                channels.EditAdminRequest(
                    channel=chat,
                    user_id=user.id,
                    admin_rights=types.ChatAdminRights(
                        other=True,
                        change_info=False,
                        post_messages=False if chat.broadcast else None,
                        edit_messages=False if chat.broadcast else None,
                        delete_messages=False,
                        ban_users=False,
                        invite_users=False,
                        add_admins=False,
                        anonymous=None,
                        pin_messages=False if not chat.broadcast else None,
                        manage_call=False if not chat.broadcast else None,
                        manage_topics=False if not chat.broadcast else None,
                    ),
                    rank=rank,
                )
            )
            return await utils.answer(
                message,
                self.strings["promoted_moder"].format(
                    id=user.id, name=user.first_name
                ),
            )
        except Exception as e:
            return await utils.answer(message, self.strings["error"].format(error=e))

    @loader.command(
        ru_doc="Выдать полные права", jp_doc="完全な権限を持つ参加者を昇格させる"
    )
    @loader.tag("no_pm")
    async def fullrights(self, message):
        """Promote a participant with full rights"""
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if reply and args:
            user = await self._client.get_entity(reply.sender_id)
            rank = " ".join(args)
        elif reply:
            user = await self._client.get_entity(reply.sender_id)
            rank = "admin" if not user.bot else "bot"
        elif args:
            user = await self._client.get_entity(await utils.get_target(message))
            if len(args) >= 2:
                rank = " ".join(args[1:])
            else:
                rank = "admin" if not user.bot else "bot"
        else:
            return await utils.answer(message, self.strings["no_user"])
        try:
            await self._client(
                channels.EditAdminRequest(
                    channel=chat,
                    user_id=user.id,
                    admin_rights=types.ChatAdminRights(
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
                        manage_call=True if not chat.broadcast else None,
                        manage_topics=True if not chat.broadcast else None,
                    ),
                    rank=rank,
                )
            )
            return await utils.answer(
                message,
                self.strings["promoted_fullrights"].format(
                    id=user.id, name=user.first_name
                ),
            )
        except Exception as e:
            return await utils.answer(message, self.strings["error"].format(error=e))

    @loader.command(ru_doc="Снять с админки", jp_doc="参加者の降格")
    @loader.tag("no_pm")
    async def demote(self, message):
        """Demote a participant"""
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        elif args:
            user = await self._client.get_entity(await utils.get_target(message))
        else:
            return await utils.answer(message, self.strings["no_user"])
        try:
            await self._client(
                channels.EditAdminRequest(
                    channel=chat,
                    user_id=user.id,
                    admin_rights=types.ChatAdminRights(
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
                        manage_topics=None,
                    ),
                    rank="",
                )
            )
            return await utils.answer(
                message,
                self.strings["demoted"].format(id=user.id, name=user.first_name),
            )
        except Exception as e:
            return await utils.answer(message, self.strings["error"].format(error=e))

    async def invite_user(self, message, chat, user):
        try:
            await self._client(
                channels.InviteToChannelRequest(channel=chat, users=[user])
            )
        except Exception as e:
            return await utils.answer(
                message,
                self.strings["error"].format(error=str(e)),
            )
        await utils.answer(
            message,
            self.strings["user_invited"].format(user=user.first_name, id=user.id),
        )
        await asyncio.sleep(3)
        return None

    def parse_time(self, time: str) -> timedelta:
        unit_to_days = {
            "m": 1 / 1440,
            "h": 1 / 24,
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
