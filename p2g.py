# meta developer: @xdesai

from telethon.tl.types import Message
from PIL import Image
import os
from .. import loader, utils

@loader.tds
class P2G(loader.Module):
    """Модуль для преобразования изображения в GIF"""
    strings = {
        "name": "P2G",
        "processing": "📤 Image Processing...",
        "no_image": "❌ No image found!",
        "gif_ready": "✅ GIF is ready!"
    }

    strings_ru = { 
        "name": "P2G",
        "processing": "📤 Обработка изображения...",
        "no_image": "❌ Изображение не найдено!",
        "gif_ready": "✅ GIF готов!"
    }

    @loader.command(
        doc_ru = "Создает GIF из изображения. Использование: .gif (ответ на изображение)"
    )
    async def p2g(self, message: Message):
        """Creates a GIF from an image. Usage: .gif (response to the image)"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings("no_image", message))
            return

        await utils.answer(message, self.strings["processing"])

        file = await reply.download_media()
        if not file or not file.endswith((".jpg", ".jpeg", ".png")):
            await utils.answer(message, self.strings("no_image", message))
            return

        try:
            img = Image.open(file)
            frames = [img.copy() for _ in range(10)]
            gif_path = file.rsplit(".", 1)[0] + ".gif"

            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=100,
                loop=0
            )

            await self.client.send_file(
                message.chat_id, gif_path, reply_to=reply.id
            )
            await message.delete()

        finally:
            if os.path.exists(file):
                os.remove(file)
            if os.path.exists(gif_path):
                os.remove(gif_path)
