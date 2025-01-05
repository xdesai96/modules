# meta developer: @xdesai & @devjmodules
import requests
from threading import Thread
from pyngrok import ngrok
from flask import Flask, request
from .. import loader, utils

app = Flask(__name__)

ip_addresses = []
ngrok_tunnel = None

@loader.tds
class ProbivMod(loader.Module):
    """Модуль для пробива по IP.
    IP адреса отправяться в избранные после остановки Flask и ngrok.
    Made by Desai"""

    strings = {
        "name": "ProbivModule"
    }

    @loader.owner
    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.owner
    async def startcmd(self, event):
        """Сгенерировать ссылку"""
        global ngrok_tunnel
        app_thread = Thread(target=self.run_flask)
        app_thread.start()
        ngrok_tunnel = await startngrok()
        if ngrok_tunnel:
            await event.edit(f"Flask и Ngrok запущены.\n{ngrok_tunnel.public_url}")
        else:
            await event.edit("Не удалось создать туннель с помощью Ngrok.")

    def run_flask(self):
        app.run(debug=False, use_reloader=False, threaded=True)

    @loader.owner
    async def stopcmd(self, event):
        """Остановка Flask и ngrok."""
        await stop()
        result = ""
        for i in ip_addresses:
            result += f"<code>{i}</code>\n"
        await event.delete()
        await self.client.send_message('me', f"Ip:\n{result}")

    @loader.owner
    async def probivcmd(self, event):
        """Пробить по айпи. Использование .probiv <ip>"""
        args = utils.get_args(event)
        if not args:
            await event.edit("❌ Укажите айпи.")
            return
        
        ip = args[0] if isinstance(args, list) else args
        data = await get_location_by_ip(ip)
        await event.edit(data)
    
    @loader.owner
    async def ngrokcmd(self, event):
        """Вставьте токен ngrok. Использование ngrok (token)."""
        args = utils.get_args(event)
        if not args:
            await event.edit("❌ Укажите токен.")
            return

        token = args[0] if isinstance(args, list) else args
        ngrok.set_auth_token(token)
        await event.edit("Token added!")

async def get_location_by_ip(ip_address):
    url = f'http://ip-api.com/json/{ip_address}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'fail':
            return "No data available"
        else:
            return f"""
IP: {ip_address}
City: {data.get('city', 'no city available')}
Region: {data.get('regionName', 'no region available')}
Country: {data.get('country', 'no country available')}
Location: {data.get('lat', 'no latitude available')}, {data.get('lon', 'no longitude available')}
"""

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

async def stop():
    # Stop ngrok
    try:
        ngrok.disconnect(ngrok_tunnel.public_url)
    except Exception as e:
        print(f"Ошибка при остановке ngrok: {e}")
    # Stop Flask
    try:
        shutdown_server()
    except Exception as e:
        print(f"Ошибка при остановке Flask: {e}")

async def startngrok():
    global ngrok_tunnel
    ngrok_tunnel = ngrok.connect(5000)
    if ngrok_tunnel:
        return ngrok_tunnel
    else:
        return None

@app.before_request
def check_request():
    global ip_addresses
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ip_addresses.append(ip)

@app.route('/')
def home():
    return "<h1>Hello World!</h1>"
