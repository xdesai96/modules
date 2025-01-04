from .. import loader
from telethon import functions
import time
import datetime

class IrisFarm:
    async def autofarm(self):
        await self._client.send_message(self._bot, "фармить")
        

class IrFarmMod(loader.Module, IrisFarm):
    """Auto farm in iris bot"""

    strings = {
        "name": "IrisFarm",
        "on": "IrisFarm включен.",
        "off": "IrisFarm выключен."
    }

    _bot = "@iris_black_bot"

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "IrisFarm",
                True,
                "Автоматически собирать Iris Coins.",
                validator=loader.validators.Boolean()
            )
        )

    @loader.loop(interval=1, autostart=True)
    async def main_loop(self):
        if self.config["IrisFarm"] and (not self.get("Iris_time") or (time.time() - self.get('Iris_time')) >= 4 * 60 * 60 + 1):
            await self.autofarm()
            self.set("Iris_time", int(time.time()))

        await self._client(functions.messages.ReadMentionsRequest(self._bot))

    @loader.command()
    async def rstirfarm(self, message):
        """restart auto farm"""
        self.main_loop.stop()
        self.config['IrisFarm'] = False
        await self.autofarm()
        self.set("Iris_time", int(time.time()))
        self.main_loop.start()
        self.config['IrisFarm'] = True
        await message.edit("Auto farm restarted")

    @loader.command()
    async def irfarm(self, message):
        """turn on auto farm"""
        self.config['IrisFarm'] = True
        self.main_loop.start()
        await message.edit(self.strings("on"))

    @loader.command()
    async def irfarmstop(self, message):
        """turn off auto farm"""
        self.config['IrisFarm'] = False
        self.main_loop.stop()
        await message.edit(self.strings("off"))