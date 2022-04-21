import asyncio
import websockets
import requests


SERVER_HOST = 'localhost:8000/live/'
SYMBOL_CODE = 'A005930'
URL = {
    "HTTP": f"http://{SERVER_HOST}{SYMBOL_CODE}",
    "WS": f"ws://{SERVER_HOST}{SYMBOL_CODE}",
    "TEST": "ws://simple-websocket-server-echo.glitch.me/"
}

# Live Price Server에서 준비시킴
print(requests.get(URL["HTTP"]))

async def listen():
    async with websockets.connect(URL["WS"]) as ws:
        while True:
            msg = await ws.recv()
            print(msg)

asyncio.get_event_loop().run_until_complete(listen())
