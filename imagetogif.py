# meta developer: @xdesai

import os
import asyncio
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import cv2
import numpy as np

from .. import loader, utils


@loader.tds
class ImageToGif(loader.Module):
    """Module to convert image to GIF"""

    strings = {
        "name": "ImageToGif",
        "processing": "<emoji document_id=6039573425268201570>📤</emoji> Image Processing...",
        "no_image": "<emoji document_id=5219776129669276751>❌</emoji> No image found!",
        "error": "<emoji document_id=5219776129669276751>❌</emoji> An error occurred: <code>{error}</code>",
    }

    strings_ru = {
        "name": "ImageToGif",
        "_cls_doc": "Модуль для преобразования изображения в GIF",
        "processing": "<emoji document_id=6039573425268201570>📤</emoji> Обработка изображения...",
        "no_image": "<emoji document_id=5219776129669276751>❌</emoji> Изображение не найдено!",
        "error": "<emoji document_id=5219776129669276751>❌</emoji> Произошла ошибка: <code>{error}</code>",
    }

    async def image_to_gif_async(self, image_path, output_video, duration=5, fps=24):
        """Convert image to video asynchronously using thread pool"""

        def sync_conversion():
            pil_image = Image.open(image_path)
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            height, width = opencv_image.shape[:2]

            total_frames = int(duration * fps)

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

            for _ in range(total_frames):
                video_writer.write(opencv_image)

            video_writer.release()
            return output_video

        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, sync_conversion)
            return result

    @loader.command(doc_ru="Создает GIF из изображения.", alias="mg")
    async def makegif(self, m):
        """Creates a GIF from an image."""
        reply = await m.get_reply_message()
        msg = reply or m
        if not hasattr(msg, "media") or not hasattr(getattr(msg, "media"), "photo"):
            await utils.answer(m, self.strings["no_image"])
            return
        try:
            await utils.answer(m, self.strings["processing"])
            image = await msg.download_media()
            saved = await self.image_to_gif_async(image, "gif.mp4")
            await utils.answer(m, "", file=saved)
        except Exception as e:
            await utils.answer(m, self.strings["error"].format(error=e))
            return
        finally:
            if image and os.path.exists(image):
                os.remove(image)
            if saved and os.path.exists(saved):
                os.remove(saved)
