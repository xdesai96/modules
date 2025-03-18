# meta developer: @xdesai

import asyncio
from .. import loader, utils


@loader.tds
class AccstatMod(loader.Module):
    """Gets information about user from funstat.\nBefore using unblock @Accstat_bot"""
    strings = {
        "name": "Accstat",
        "no_user": "<blockquote>❌ <b>User not specified</b></blockquote>",
        "error": "<blockquote><b>Error:</b> {err}</blockquote>",
        "timeout": "<blockquote>⏲ <b>Bot did not answer ...</b></blockquote>"
    }

    strings_ru = {
        "name": "Accstat",
        "no_user": "<blockquote>❌ <b>Пользователь не указан</b></blockquote>",
        "error": "<blockquote><b>Ошибка:</b> {err}</blockquote>",
        "timeout": "<blockquote>⏲ <b>Бот не ответил ...</b></blockquote>"
    }

    _bot = "@Accstat_bot"

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
    
    @loader.command(
        ru_doc="<user> | Получить информацию."
    )
    async def fstat(self, message):
        """<user> | Get info."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            if not args:
                return await utils.answer(message, self.strings("no_user"))
            else:
                if args.isdigit():
                    user_id = int(args)
                else:
                    try:
                        user_id = (await self.client.get_entity(args)).id
                        async with self._client.conversation(self._bot) as conv:
                            await conv.send_message(f"{user_id}")
                            try:
                                r = await conv.get_response(timeout=15)
                                await utils.answer(message, r.message)
                                r = await conv.get_response(timeout=15)
                                await utils.answer(message, r.message)
                            except asyncio.exceptions.TimeoutError:
                                return await utils.answer(self.strings('timeout'))
                    except Exception as e:
                        return utils.answer(message, self.strings('error').format(err=e))
        else:
            user_id = reply.sender_id
            async with self._client.conversation(self._bot) as conv:
                await conv.send_message(f"{user_id}")
                try:
                    r = await conv.get_response(timeout=15)
                    await utils.answer(message, r.message)
                    r = await conv.get_response(timeout=15)
                    await utils.answer(message, r.message)
                except asyncio.exceptions.TimeoutError:
                    return await utils.answer(message, self.strings('timeout'))
