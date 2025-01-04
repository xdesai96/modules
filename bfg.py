import asyncio
import time
from telethon import functions
from .. import loader

class Farm:
    async def autofarm(self):
        async with self._client.conversation(self._bot) as conv:
            commands = [
                ('моя ферма', [0, 1]),
                ('мой бизнес', [0, 1]),
                ('мой генератор', [0, 1]),
                ('мое дерево', [0, 1]),
                ('мой карьер', [0, 1]),
                ('мой сад', [0, 1, 3]),
            ]
            for command, clicks in commands:
                await conv.send_message(command)
                try:
                    r = await conv.get_response()
                except:
                    continue

                for click in clicks:
                    await asyncio.sleep(3)
                    try:
                        await r.click(click)
                    except:
                        continue

class BfgMod(loader.Module, Farm):
    """
    Автоматическая фарма в боте BFG.
    """

    strings = {"name": "BFG"}

    _bot = "@bforgame_bot"

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "AutoFarm",
                True,
                "Автоматически собирать и оплачивать налоги.",
                validator=loader.validators.Boolean(),
            )
        )

    @loader.loop(interval=1, autostart=True)
    async def main_loop(self):
        if self.config["AutoFarm"] and (not self.get("Tree_time") or (time.time() - self.get("Tree_time")) >= 3600):
            await self.autofarm()
            self.set("Tree_time", int(time.time()))

        await self._client(functions.messages.ReadMentionsRequest(self._bot))

    @loader.command()
    async def bfg(self, message):
        """Начать автоматическую фарму."""
        self.config["AutoFarm"] = True
        self.main_loop.start()
        await message.edit("Автоматическая фарма включена.")
        
    @loader.command()
    async def bfgstop(self, message):
        """Остановить автоматическую фарму."""
        self.config["AutoFarm"] = False
        self.main_loop.stop()
        await message.edit("Автоматическая фарма остановлена.")