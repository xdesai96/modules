# meta developer: @xdesai

from .. import utils, loader
from telethon.tl.types import UserStatusOnline, UserStatusOffline, User, InputPeerUser
from telethon.tl.functions.messages import GetCommonChatsRequest


def format_bool(value):
    """Форматирует булевы значения в читаемый вид"""
    if value is None:
        return "<code>Unknown</code>"
    return "<code>True</code>" if value else "<code>False</code>"


def format_status(status):
    """Форматирует статус пользователя"""
    if isinstance(status, UserStatusOnline):
        expires = (
            status.expires.strftime("%Y-%m-%d %H:%M:%S UTC")
            if status.expires
            else "Unknown"
        )
        return f"Online (until {expires})"
    elif isinstance(status, UserStatusOffline):
        last_seen = (
            status.was_online.strftime("%Y-%m-%d %H:%M:%S UTC")
            if status.was_online
            else "Unknown"
        )
        return f"Offline (last seen {last_seen})"
    else:
        return "Unknown"


@loader.tds
class GetUserMod(loader.Module):
    strings = {
        "name": "GetUser",
        "no_user": "🚫 User not found.",
        "deleted": "🚫 Deleted account.",
        "telegram_service": "🚫 This is a Telegram service account. What do you want to know about it?",
        "yourself": "🚫 You can't get information about yourself. What do you want to know about me?",
        "user_info": "👤 <b>User Information:</b>",
        "id": "🆔 <b>ID:</b> <code>{id}</code>",
        "first_name": "👤 <b>First Name:</b> <code>{first_name}</code>",
        "last_name": "👤 <b>Last Name:</b> <code>{last_name}</code>",
        "username": "📱 <b>Username:</b> <code>@{username}</code>",
        "usernames": "📱 <b>Usernames:</b>",
        "phone": "📞 <b>Phone:</b> <code>{phone}</code>",
        "status": "📊 <b>Status:</b> <code>{status}</code>",
        "contact": "🤝 <b>Contact:</b> {contact}",
        "mutual_contact": "🤝 <b>Mutual Contact:</b> {mutual_contact}",
        "bot": "🤖 <b>Bot:</b> {bot}",
        "verified": "✅ <b>Verified:</b> {verified}",
        "restricted": "🚫 <b>Restricted:</b> {restricted}",
        "scam": "⚠️ <b>Scam:</b> {scam}",
        "fake": "🎭 <b>Fake:</b> {fake}",
        "premium": "⭐️ <b>Premium:</b> {premium}",
        "support": "🛠 <b>Support:</b> {support}",
        "common_chats": "💬 <b>Common Chats:</b> <code>{count}</code>",
        "common_chats_list": "📋 <b>Common Chats List:</b>",
        "no_common_chats": "😢 <b>No common chats</b>",
        "phone_hidden": "What do you want to do with my phone number?",
        "account_flags": "<b>Account Flags:</b>",
    }

    strings_ru = {
        "no_user": "🚫 Пользователь не найден.",
        "deleted": "🚫 Удаленный аккаунт.",
        "telegram_service": "🚫 Это аккаунт Telegram сервиса. Что вы хотите узнать о нем?",
        "yourself": "🚫 Вы не можете получить информацию о себе. Что вы хотите узнать обо мне?",
        "user_info": "👤 <b>Информация о пользователе:</b>",
        "id": "🆔 <b>ID:</b> <code>{id}</code>",
        "first_name": "👤 <b>Имя:</b> <code>{first_name}</code>",
        "last_name": "👤 <b>Фамилия:</b> <code>{last_name}</code>",
        "username": "📱 <b>Username:</b> <code>@{username}</code>",
        "usernames": "📱 <b>Usernames:</b>",
        "phone": "📞 <b>Телефон:</b> <code>{phone}</code>",
        "status": "📊 <b>Статус:</b> <code>{status}</code>",
        "contact": "🤝 <b>Контакт:</b> {contact}",
        "mutual_contact": "🤝 <b>Взаимный контакт:</b> {mutual_contact}",
        "bot": "🤖 <b>Бот:</b> {bot}",
        "verified": "✅ <b>Верифицирован:</b> {verified}",
        "restricted": "🚫 <b>Ограничен:</b> {restricted}",
        "scam": "⚠️ <b>Мошенник:</b> {scam}",
        "fake": "🎭 <b>Фейк:</b> {fake}",
        "premium": "⭐️ <b>Премиум:</b> {premium}",
        "support": "🛠 <b>Поддержка:</b> {support}",
        "common_chats": "💬 <b>Общие чаты:</b> <code>{count}</code>",
        "common_chats_list": "📋 <b>Список общих чатов:</b>",
        "no_common_chats": "😢 <b>Нет общих чатов</b>",
        "phone_hidden": "Что вы хотите сделать с моим номером телефона?",
        "account_flags": "<b>Флаги аккаунта:</b>",
    }

    @loader.command(ru_doc="Получить информацию о пользователе")
    async def getuser(self, message):
        """Get information about the user"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        user_id = await utils.get_target(message) if not args and not reply else None
        if user_id:
            data = await self.client.get_entity(user_id)
        elif reply:
            data = await self.client.get_entity(reply.sender_id)
        elif args:
            if args.isdigit():
                data = await self.client.get_entity(int(args))
            else:
                data = await self.client.get_entity(args)
        else:
            return await utils.answer(message, self.strings["no_user"])

        if not data:
            return await utils.answer(message, self.strings["no_user"])

        error_message = self._check_special_cases(data)
        if error_message:
            return await utils.answer(message, error_message)

        common_chats = await self._get_common_chats(data.id)

        result = await self._build_user_info(data, common_chats)

        return await utils.answer(message, result)

    def _check_special_cases(self, data):
        if not isinstance(data, (User, InputPeerUser)):
            return self.strings["no_user"]
        if data.deleted:
            return self.strings["deleted"]
        return None

    async def _get_common_chats(self, user_id):
        try:
            comm = await self.client(
                GetCommonChatsRequest(user_id=user_id, max_id=0, limit=100)
            )
            common_chats = [chat.title for chat in comm.chats]
            common_chats.sort()
            return common_chats
        except Exception:
            return []

    async def _build_user_info(self, data, common_chats):
        try:
            is_self = data.id == self._client.tg_id
        except:
            is_self = False

        phone = data.phone or "None"
        if is_self and phone != "None":
            phone = utils.censor(data, ["phone"], "hidden").phone

        result = [
            f'<blockquote expandable>{self.strings["user_info"]}',
            "",
            self.strings["id"].format(id=data.id),
            self.strings["first_name"].format(first_name=data.first_name or "None"),
            self.strings["last_name"].format(last_name=data.last_name or "None"),
            "",
        ]

        self._add_usernames_info(result, data)
        result.append(self.strings["phone"].format(phone=phone))
        result.append("")

        result.extend(
            [
                self.strings["status"].format(status=format_status(data.status)),
                "</blockquote>",
            ]
        )

        result.extend(self._build_account_flags(data))

        result.extend(self._build_common_chats_info(common_chats))

        return "\n".join(result)

    def _add_usernames_info(self, result, data):
        if hasattr(data, "usernames") and data.usernames:
            result.append(self.strings["usernames"])
            for username_obj in data.usernames:
                result.append(f"  • @{username_obj.username}")
        elif data.username:
            result.append(self.strings["username"].format(username=data.username))
        else:
            result.append(self.strings["username"].format(username="None"))
        result.append("")

    def _build_account_flags(self, data):
        return [
            f'<blockquote expandable>{self.strings["account_flags"]}',
            self.strings["contact"].format(contact=format_bool(data.contact)),
            self.strings["mutual_contact"].format(
                mutual_contact=format_bool(data.mutual_contact)
            ),
            self.strings["bot"].format(bot=format_bool(data.bot)),
            self.strings["verified"].format(verified=format_bool(data.verified)),
            self.strings["restricted"].format(restricted=format_bool(data.restricted)),
            self.strings["scam"].format(scam=format_bool(data.scam)),
            self.strings["fake"].format(fake=format_bool(data.fake)),
            self.strings["premium"].format(premium=format_bool(data.premium)),
            f'{self.strings["support"].format(support=format_bool(data.support))}</blockquote>',
        ]

    def _build_common_chats_info(self, common_chats):
        result = [
            f'<blockquote expandable>{self.strings["common_chats"].format(count=len(common_chats))}'
        ]
        if common_chats:
            result.append(self.strings["common_chats_list"])
            for i, chat in enumerate(common_chats, 1):
                result.append(f"{i}. <code>{chat}</code>")
        else:
            result.append(self.strings["no_common_chats"])
        result.append("</blockquote>")
        return result
