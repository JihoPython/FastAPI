import asyncio
import websockets
import requests
# from fastapi import WebSocket

# async def connect():
#     async with websockets.connect("ws://localhost:8000/ws") as websocket:
#         # await websocket.send('python client connected')
#         data = await websocket.recv()
#         print(data)

# asyncio.get_event_loop().run_until_complete(connect())

# while True:
#     pass

async def hello():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        requests.get("http://localhost:8000/push/client")
        await websocket.recv()

asyncio.run(hello())

while True:
    pass