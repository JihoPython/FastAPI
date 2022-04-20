from typing import Dict
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import pythoncom

from service.live import Connection


router = APIRouter()
pool: Dict[str, Connection] = {}
"""전역 Connection Pool"""


@router.get("{code}")
async def check_creon_status(code: str):
    channel = pool[code]
    if channel is None:
        channel = pool[code] = Connection(code)
        await channel.generator.asend(None)
    return { 'ack': True, 'connection': pool.code }

@router.websocket("{code}")
async def websocket_endpoint(websocket: WebSocket, code: str):
    channel = pool[code]
    await channel.connect()
    try:
        while True:
            pythoncom.PumpWaitingMessages()
            await asyncio.sleep(0.01)
            await channel.push()
    except WebSocketDisconnect:
        channel.remove(websocket)
