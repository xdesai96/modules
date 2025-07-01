# meta developer: @xdesai

from .. import loader, utils
import socket
import aiohttp
import aiodns


@loader.tds
class URLMod(loader.Module):
    """A module for parsing URLs."""

    strings = {
        "name": "URLModule",
        "no_url": "<emoji document_id=5416076321442777828>❌</emoji> <b>Please provide a shortened URL to expand.</b>",
        "err": '<emoji document_id=5416076321442777828>❌</emoji> <b>An error occurred:</b> <pre><code class="language-Error">{err}</code></pre>',
        "expanded_url": "<emoji document_id=5816580359642421388>➡️</emoji> <b>Expanded URL:</b> <a href='{expanded_url}'>{expanded_url}</a>",
        "ip_addr": "<emoji document_id=5447410659077661506>🌐</emoji> <b>The IP address of {url}:</b> <code>{ip_address}</code>",
    }

    strings_ru = {
        "no_url": "<emoji document_id=5416076321442777828>❌</emoji> <b>Пожалуйста, предоставьте сокращённую URL для расширения.</b>",
        "err": '<emoji document_id=5416076321442777828>❌</emoji> <b>Произошла ошибка:</b> <pre><code class="language-Error">{err}</code></pre>',
        "expanded_url": "<emoji document_id=5816580359642421388>➡️</emoji> <b>Расширенный URL:</b> <a href='{expanded_url}'>{expanded_url}</a>",
        "ip_addr": "<emoji document_id=5447410659077661506>🌐</emoji> <b>IP-адрес для {url}:</b> <code>{ip_address}</code>",
    }

    strings_jp = {
        "no_url": "<emoji document_id=5416076321442777828>❌</emoji> <b>展開する短縮URLを入力してください。</b>",
        "err": '<emoji document_id=5416076321442777828>❌</emoji> <b>エラーが発生しました：</b> <pre><code class="language-Error">{err}</code></pre>',
        "expanded_url": "<emoji document_id=5816580359642421388>➡️</emoji> <b>展開されたURL：</b> <a href='{expanded_url}'>{expanded_url}</a>",
        "ip_addr": "<emoji document_id=5447410659077661506>🌐</emoji> <b>{url} のIPアドレス：</b> <code>{ip_address}</code>",
    }

    @loader.command(
        ru_doc="Показывает куда ведет сокращенная ссылка",
        jp_doc="指定された短縮URLを展開します",
    )
    async def expandurlcmd(self, message):
        """Expands the given shortened URL"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_url"))
            return
        short_url = args.strip()
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(short_url, allow_redirects=True) as response:
                    response.raise_for_status()
                    expanded_url = str(response.url)
                    await utils.answer(
                        message,
                        self.strings("expanded_url").format(expanded_url=expanded_url),
                    )
        except aiohttp.ClientError as e:
            await utils.answer(message, self.strings("err").format(err=e))

    @loader.command(
        ru_doc="Получить IP адрес сайта", jp_doc="WebサイトのIPアドレスを取得する"
    )
    async def ipurlcmd(self, message):
        """Gets the IP address of the given URL"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_url"))
            return
        url = args.strip()
        resolver = aiodns.DNSResolver()

        try:
            hostname = url.split("//")[-1].split("/")[0]
            response = await resolver.gethostbyname(hostname, socket.AF_INET)
            ip_address = response.addresses[0]
            await utils.answer(
                message, self.strings("ip_addr").format(url=url, ip_address=ip_address)
            )
        except aiodns.error.DNSError as e:
            await utils.answer(message, self.strngs("err").format(err=e))
