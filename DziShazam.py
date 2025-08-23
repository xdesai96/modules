#
#█▀▄ ▀█ █ █▀█ █░█  █▀▀ ▄▀█ █▄█
#█▄▀ █▄ █ █▀▄ █▄█  █▄█ █▀█ ░█░
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @dziru
# meta pic: https://raw.githubusercontent.com/DziruModules/assets/master/DziruModules.jpg
# meta banner: https://raw.githubusercontent.com/DziruModules/assets/master/DziShazam.png
# scope: hikka_min 1.5.0
# scope: hikka_only
# version: 1.0

from .. import utils, loader

@loader.tds
class DziShazamMod(loader.Module):
    """Module for searching music's. Works using @lybot"""

    strings = {
        "name": "DziShazam",
        "dwait": "<emoji document_id=5334922351744132060>😉</emoji> <b>Just wait!</b>",
        "failed": "<emoji document_id=5335046240075784593>😠</emoji> <b>Provide the Song name!</b>",
        "loading": "<emoji document_id=5818687127000452892>🔎</emoji> <b>Searching...</b>",
        }

    strings_ru = {
        "dwait": "<emoji document_id=5334922351744132060>😉</emoji> <b>Просто подождите!</b>",
        "failed": "<emoji document_id=5335046240075784593>😠</emoji> <b>Укажите название песни!</b>",
        "loading": "<emoji document_id=5818687127000452892>🔎</emoji> <b>Поиск...</b>",
        }

    @loader.command(ru_doc="<песня> укажите название")
    async def mcdcmd(self, message):
        """<song> enter name"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings["failed"])
        try:
            await utils.answer(message, self.strings['loading'])
            music = await message.client.inline_query("lybot", args)
            return await utils.answer_file(
                message,
                music[0].result.document
            )
        except:
            return await utils.answer(
                message,
                self.strings["failed"],
            )