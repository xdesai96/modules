# meta developer: @xdesai

from .. import loader, utils

class DBMod(loader.Module):
    """Module to check and clean the database\nBe careful while using this module!"""
    strings = {"name": "DBMod",
        "del_text": "<b>Choose a module to delete from the database</b>\n\n⚠ Be careful and do not delete the core modules",
        "info_text": "<b>Which of the modules are you interested in?</b>",
        "deleted": "Key {key} deleted from Database",
        "not_found": "Key {key} not found in Database"
    }

    strings_ru = {
        "del_text": "<b>Выберите модуль для удаления из базы данных</b>\n\n⚠ Будьте осторожны и не удаляйте основные модули",
        "info_text": "<b>Какой из модулей вас интересует?</b>",
        "deleted": "Ключ {key} удален из базы данных",
        "not_found": "Ключ {key} не найден в базе данных"
    }

    async def delete_db(self, call, item):
        """Clean db of the module"""
        if item[0] in self._db.keys():
            self._db.pop(f"{item[0]}")
            self._db.save()
            await call.edit("Database", reply_markup=self.generate_markup("del"))
            await call.answer(self.strings("deleted").format(key=item[0]))
            return True
        await call.answer(self.strings("not_found").format(key=item[0]))
        return False

    async def info_db(self, call, item):
        """Info about db of the module"""
        if item[0] in self._db.keys():
            await call.edit(f"<pre><code class='language-INFO'>{item[0]}:\n{item[1]}</code></pre>", reply_markup=self.generate_markup("info"))
            return True
        await call.answer(self.strings("not_found").format(key=item[0]))
        return False

    def generate_markup(self, action: str = "info"):
        """Generate markup for inline form"""
        markup = [[]]
        for item in self._db.items():
            if item not in markup:
                if len(markup[-1]) == 4:
                    markup.append([])
                if action == "del":
                    markup[-1].append(
                        {
                            'text': f'{item[0]}',
                            'callback': self.delete_db,
                            'args': [item],
                        }
                    )
                elif action == "info":
                    markup[-1].append(
                        {
                            'text': f'{item[0]}',
                            'callback': self.info_db,
                            'args': [item],
                        }
                    )
        return markup

    @loader.command(
        ru_doc="Удалить модуль из базы данных",
    )
    async def cldbcmd(self, message):
        """Clean db of the module"""
        await utils.answer(
            message,
            self.strings("del_text"),
            reply_markup=self.generate_markup("del")
        )

    @loader.command(
        ru_doc="Посмотреть модуль в базе данных",
    )
    async def infodbcmd(self, message):
        """Check the info of the modules"""
        await utils.answer(
            message,
            self.strings("info_text"),
            reply_markup=self.generate_markup("info")
        )
