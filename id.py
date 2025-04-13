# meta developer: @xdesai

from .. import loader, utils

@loader.tds
class ID(loader.Module):
    """Module to check the ids"""

    strings = {
        "name": "ID",
        "id_info": "<emoji document_id=5208454037531280484>💜</emoji> <b>My ID:</b> <code>{my_id}</code>\n<emoji document_id=5886436057091673541>💬</emoji> <b>Chat ID:</b> <code>{chat_id}</code>\n",
        "id_user": "<emoji document_id=6035084557378654059>👤</emoji> <b>User's ID:</b> <code>{user_id}</code>"
    }

    strings_ru = {
        "id_info": "<emoji document_id=5208454037531280484>💜</emoji> <b>Мой ID:</b> <code>{my_id}</code>\n<emoji document_id=5886436057091673541>💬</emoji> <b>ID Чата:</b> <code>{chat_id}</code>\n",
        "id_user": "<emoji document_id=6035084557378654059>👤</emoji> <b>ID Пользователя:</b> <code>{user_id}</code>"
    }

    @loader.command(
        ru_doc="Посмотреть ID"
    )
    async def idcmd(self, m):
        """See the IDs"""
        r = await m.get_reply_message()
        output = self.strings("id_info").format(my_id=self.tg_id, chat_id=m.chat_id)
        if r:
            if not m.is_private:
                output += self.strings("id_user").format(user_id=r.from_id.user_id)
            else:
                output += self.strings("id_user").format(user_id=r.peer_id.user_id)
        await utils.answer(m, output)
