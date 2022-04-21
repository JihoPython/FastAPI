from typing import Dict
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import pythoncom

from utils.LoggerConfig import logger

from service.live import Channel

router = APIRouter()
pool: Dict[str, Channel] = {}
"""전역 Channel Pool"""

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/live/%s");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.insertBefore(message, messages.firstChild)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@router.get("/{code}")
async def check_creon_status(code: str):
    logger.info(f"종목 코드 {code} 수신 요청이 왔습니다.")

    channel = pool.get(code)
    if channel is None:
        logger.info(f"{code} channel Creon 연결을 시도합니다.")
        channel = pool[code] = Channel(code)
        await channel.generator.asend(None)
    return HTMLResponse(html % code)

@router.websocket("/{code}")
async def websocket_endpoint(websocket: WebSocket, code: str):
    channel = pool.get(code)
    await channel.connect(websocket)
    try:
        while True:
            pythoncom.PumpWaitingMessages()
            await asyncio.sleep(1)
            await channel.push()
    except (WebSocketDisconnect, StopAsyncIteration) as e:
        if len(channel.connections) == 0:
            await channel.api.unsubscribe()
            pool.pop(code)
        else:
            await channel.remove(websocket)
