# meta developer: @xdesai
# scope: ffmpeg

from telethon.tl.types import Message
import os, subprocess
from .. import loader, utils
from PIL import Image


@loader.tds
class P2G(loader.Module):
    """Модуль для преобразования изображения в GIF"""

    strings = {
        "name": "ImageToGif",
        "processing": "📤 Image Processing...",
        "no_image": "❌ No image found!",
        "gif_ready": "✅ GIF is ready!",
    }

    strings_ru = {
        "name": "ImageToGif",
        "processing": "📤 Обработка изображения...",
        "no_image": "❌ Изображение не найдено!",
        "gif_ready": "✅ GIF готов!",
    }

    @loader.command(doc_ru="Создает GIF из изображения.")
    async def p2g(self, message: Message):
        """Creates a GIF from an image."""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings["no_image"])
            return

        await utils.answer(message, self.strings["processing"])

        file = await reply.download_media()
        if not file or not file.endswith((".jpg", ".jpeg", ".png")):
            await utils.answer(message, self.strings["no_image"])
            return

        try:
            img = Image.open(file)
            if img.format.lower() == "webp":
                file = file.rsplit(".", 1)[0] + ".png"
                img.save(file, format="PNG")
        except Exception:
            await utils.answer(message, self.strings["no_image"])
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
                "-framerate",
                "10",
                "-i",
                os.path.join(temp_dir, "frame_%03d.png"),
                "-vf",
                "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                mp4_path,
            ]

            subprocess.run(ffmpeg_command, check=True)

            await utils.answer_file(message, mp4_path, "")
        finally:
            if os.path.exists(file):
                os.remove(file)
            if mp4_path and os.path.exists(mp4_path):
                os.remove(mp4_path)
            for frame_file in frame_files:
                if os.path.exists(frame_file):
                    os.remove(frame_file)
