# meta developer: @xdesai

from telethon.tl.types import Message
from PIL import Image
import os
import subprocess
from .. import loader, utils

@loader.tds
class P2G(loader.Module):
    """Модуль для преобразования изображения в GIF"""
    strings = {
        "name": "ImageToGif",
        "processing": "📤 Image Processing...",
        "no_image": "❌ No image found!",
        "gif_ready": "✅ GIF is ready!"
    }

    strings_ru = { 
        "name": "ImageToGif",
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
        mp4_path = file.rsplit(".", 1)[0] + ".mp4"
        try:
            img = Image.open(file)
            frames = [img.copy() for _ in range(10)]
            temp_dir = "temp_frames"
            os.makedirs(temp_dir, exist_ok=True)
            frame_files = []

            for i, frame in enumerate(frames):
                frame_file = os.path.join(temp_dir, f"frame_{i:03d}.png")
                frame.save(frame_file)
                frame_files.append(frame_file)

            ffmpeg_command = [
                "ffmpeg",
                "-y",
                "-framerate", "10",
                "-i", os.path.join(temp_dir, "frame_%03d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                mp4_path
            ]
            subprocess.run(ffmpeg_command, check=True)

            async with message.client.action(message.chat_id, "document"):
                await message.client.send_file(
                    message.chat_id, mp4_path, reply_to=reply.id
                )

            await message.delete()
        finally:
            if os.path.exists(file):
                os.remove(file)
            if mp4_path and os.path.exists(mp4_path):
                os.remove(mp4_path)
            for frame_file in frame_files:
                if os.path.exists(frame_file):
                    os.remove(frame_file)
