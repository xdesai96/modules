# meta developer: @xdesai
# requires: requests

import requests
from .. import loader, utils


@loader.tds
class InfoIPMod(loader.Module):
    strings = {
        "name": "InfoIP",
        "invalid_ip": "❌ <b>Specify IP address</b>",
        "no_data": "😢 <b>No data available</b>",
        "data": "<blockquote><emoji document_id=5447410659077661506>🌐</emoji><b> Information about IP</b></blockquote>\n<blockquote><emoji document_id=6334617384782923882>📟</emoji><b> IP: <code>{ip}</code></b></blockquote>\n<blockquote><emoji document_id=5235794253149394263>🗺</emoji><b> Country: {country}</b></blockquote>\n<blockquote><emoji document_id=5247209275494769660>🕓</emoji><b> Timezone: {timezone}</b></blockquote>\n<blockquote><emoji document_id=5330371855368866588>🌇</emoji><b> City: {city}</b></blockquote>\n<blockquote><emoji document_id=5308028293033764449>⚡️</emoji><b> Region: {region}</b></blockquote>\n<blockquote><emoji document_id=5391032818111363540>📍</emoji><b> Coordinates: <code>{coordinates}</code></b></blockquote>\n<blockquote><emoji document_id=5447410659077661506>🌐</emoji> <b>Provider: {provider}</b></blockquote>",
    }
    strings_ru = {
        "invalid_ip": "❌ <b>Укажите ip адрес</b>",
        "no_data": "😢 <b>Нет данных</b>",
        "data": "<blockquote><emoji document_id=5447410659077661506>🌐</emoji><b> Информация об IP</b></blockquote>\n<blockquote><emoji document_id=6334617384782923882>📟</emoji><b> IP: <code>{ip}</code></b></blockquote>\n<blockquote><emoji document_id=5235794253149394263>🗺</emoji><b> Страна: {country}</b></blockquote>\n<blockquote><emoji document_id=5247209275494769660>🕓</emoji><b> Часовой пояс: {timezone}</b></blockquote>\n<blockquote><emoji document_id=5330371855368866588>🌇</emoji><b> Город: {city}</b></blockquote>\n<blockquote><emoji document_id=5308028293033764449>⚡️</emoji><b> Регион: {region}</b></blockquote>\n<blockquote><emoji document_id=5391032818111363540>📍</emoji><b> Координаты: <code>{coordinates}</code></b></blockquote>\n<blockquote><emoji document_id=5447410659077661506>🌐</emoji> <b>Провайдер: {provider}</b></blockquote>",
    }

    strings_jp = {
        "invalid_ip": "❌ <b>IPアドレスを指定してください</b>",
        "no_data": "😢 <b>データが見つかりません</b>",
        "data": "<blockquote><emoji document_id=5447410659077661506>🌐</emoji><b> IP情報</b></blockquote>\n<blockquote><emoji document_id=6334617384782923882>📟</emoji><b> IP: <code>{ip}</code></b></blockquote>\n<blockquote><emoji document_id=5235794253149394263>🗺</emoji><b> 国: {country}</b></blockquote>\n<blockquote><emoji document_id=5247209275494769660>🕓</emoji><b> タイムゾーン: {timezone}</b></blockquote>\n<blockquote><emoji document_id=5330371855368866588>🌇</emoji><b> 市: {city}</b></blockquote>\n<blockquote><emoji document_id=5308028293033764449>⚡️</emoji><b> 地域: {region}</b></blockquote>\n<blockquote><emoji document_id=5391032818111363540>📍</emoji><b> 座標: <code>{coordinates}</code></b></blockquote>\n<blockquote><emoji document_id=5447410659077661506>🌐</emoji> <b>プロバイダー: {provider}</b></blockquote>",
    }

    @loader.command(ru_doc="<ip> | Информация об IP", jp_doc="IPに関する情報")
    async def ipi(self, message):
        """<ip> | Information about IP"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("invalid_ip"))

        ip = await self.get_location_by_ip(str(args))
        await utils.answer(message, ip)

    async def get_location_by_ip(self, ip_address):
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "fail":
                return self.strings("no_data")
            else:
                return self.strings("data").format(
                    ip=data.get("query"),
                    country=data.get("country"),
                    timezone=data.get("timezone"),
                    city=data.get("city"),
                    region=data.get("regionName"),
                    coordinates=f"{data.get('lat')}, {data.get('lon')}",
                    provider=f"{data.get('isp')}",
                )
