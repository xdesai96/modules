# meta developer: @xdesai & @devjmodules

from .. import loader, utils
from telethon.tl.functions.contacts import GetBlockedRequest

@loader.tds
class Stats(loader.Module):
    """Показывает статистику твоего аккаунта"""

    strings = {
"name": "Stats",

"stats": """
<emoji document_id=5774022692642492953>✅</emoji><b> Account Statistics</b>

</b><emoji document_id=5208454037531280484>💜</emoji><b> Total chats: </b><code>{all_chats}</code><b>

</b><emoji document_id=6035084557378654059>👤</emoji><b> Private chats: </b><code>{users}</code><b>
</b><emoji document_id=6030400221232501136>🤖</emoji><b> Bots: </b><code>{bots}</code><b>
</b><emoji document_id=6032609071373226027>👥</emoji><b> Groups: </b><code>{groups}</code><b>
</b><emoji document_id=5870886806601338791>👥</emoji><b> Channels: </b><code>{channels}</code><b>
</b><emoji document_id=5870563425628721113>📨</emoji><b> Archived chats: </b><code>{archived}</code><b>
</b><emoji document_id=5870948572526022116>✋</emoji><b> Blocked: </b><code>{blocked}</code>""",

"loading_stats": "<b><emoji document_id=5309893756244206277>🫥</emoji> Loading statistics...</b>",
    }

    strings_ru = {
"name": "Stats",

"stats": """
<emoji document_id=5774022692642492953>✅</emoji><b> Статистика аккаунта

</b><emoji document_id=5208454037531280484>💜</emoji><b> Всего чатов: </b><code>{all_chats}</code><b>

</b><emoji document_id=6035084557378654059>👤</emoji><b> Личных чатов: </b><code>{users}</code><b>
</b><emoji document_id=6030400221232501136>🤖</emoji><b> Ботов: </b><code>{bots}</code><b>
</b><emoji document_id=6032609071373226027>👥</emoji><b> Групп: </b><code>{groups}</code><b>
</b><emoji document_id=5870886806601338791>👥</emoji><b> Каналов: </b><code>{channels}</code><b>
</b><emoji document_id=5870563425628721113>📨</emoji><b> Архивированных чатов: </b><code>{archived}</code><b>
</b><emoji document_id=5870948572526022116>✋</emoji><b> Заблокированных: </b><code>{blocked}</code>""",

"loading_stats": "<b><emoji document_id=5309893756244206277>🫥</emoji> Загрузка статистики...</b>",
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def stats(self, message):
        """Показать статистику аккаунта"""
        await utils.answer(message, self.strings['loading_stats'])
        users = 0
        bots = 0
        groups = 0
        channels = 0
        all_chats = 0
        archived = 0
        blocked_chats = await self._client(GetBlockedRequest(offset=0, limit=1))
        blocked = blocked_chats.count

        async for dialog in self._client.iter_dialogs():
            all_chats += 1
            if getattr(dialog, "archived", False):
                archived += 1
            if dialog.is_user:
                if getattr(dialog.entity, "bot", False):
                    bots += 1
                else:
                    users += 1
            elif getattr(dialog, "is_group", False):
                groups += 1
            elif dialog.is_channel:
                if getattr(dialog.entity, "megagroup", False) or getattr(dialog.entity, "gigagroup", False):
                    groups += 1
                elif getattr(dialog.entity, "broadcast", False):
                    channels += 1

        await utils.answer(message, self.strings("stats", message).format(users=users, bots=bots, channels=channels,
                                                                          groups=groups, all_chats=all_chats,
                                                                          blocked=blocked, archived=archived))
