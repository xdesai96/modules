# meta developer: @xdesai

from .. import loader
import pyfiglet

@loader.tds
class AsciiMod(loader.Module):
    """Пишет ASCII шрифтом"""
    strings = {"name": "Ascii"}

    @loader.owner
    async def asciicmd(self, event):
        """Пишет ASCII шрифтом. Использование: .ascii <текст>"""
        if len(event.text.split(" ", maxsplit=1)) > 1:
            text = event.text.split(" ", maxsplit=1)[1]
        else:
            await utils.answer(message, "❌ Пожалуйста, укажите текст для генерации.")
            return
        art = pyfiglet.figlet_format(text)
        await utils.answer(message, f"```\n⁠{art}\n```", parse_mode="markdown")
