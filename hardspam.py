# meta developer: @xdesai

import asyncio
from .. import loader, utils


@loader.tds
class HardSpam(loader.Module):
    strings = {
        "name": "HardSpam",
        "spam_help": "<b>Usage sample: {}hspam [-c|--clean] 23 text</b>",
    }
    strings_ru = {
        "spam_help": "<b>Пример использования: {}hspam [-c|--clean] 23 text</b>",
    }

    async def send_msgs(self, c, chat_id, text):
        msg = await c.send_message(chat_id, text)
        return msg.id

    @loader.command(
        ru_doc="[-c|--clean] n text - Отправить n кол-во сообщений одновременно"
    )
    async def hspamcmd(self, message):
        """[-c|--clean] n text - Send n number of messages at the same time"""
        args = utils.get_args(message)
        delete_all = False
        if "--clean" in args:
            delete_all = True
            args.remove("--clean")
        elif "-c" in args:
            delete_all = True
            args.remove("-c")
        if not args[0].isdigit() or len(args) < 2:
            return await utils.answer(
                message,
                self.strings["spam_help"].format(self.get_prefix()),
            )
        number = int(args[0])
        text = " ".join(args[1:])
        tasks = [
            self.send_msgs(self._client, message.chat_id, text) for _ in range(number)
        ]
        message_ids = await asyncio.gather(*tasks)
        if delete_all:
            await self._client.delete_messages(message.chat_id, message_ids)
        return await message.delete()
