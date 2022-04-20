from typing import List
from fastapi import WebSocket

from service.live import LivePriceAPI
from api.live import pool

class Connection:
    def __init__(self, code: str) -> None:
        self.connections: List[WebSocket] = []
        self.generator = self._generator()
        self.code = code

        try:
            # TODO 실제 CreonPlus와 연결 상태 여부 확인
            self.api = LivePriceAPI(code)
            self.api.subscribe()
        except Exception as e:
            # TODO 모듈 연결 또는 구독 실패 시 재연결 및 기타 처리
            raise e

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def push(self):
        await self.generator.asend(self.api.message)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _generator(self):
        """self.push()에서 넘긴 메시지가 올 때까지 대기하다가 메시지가 생기면 발행
        """
        while True:
            message = yield
            await self._broadcast(message)

    async def _broadcast(self, message: str):
        """connetions에 등록된 websockets에 메시지를 발행한다.
        """
        if len(self.connections) == 0:
            self.api.unsubscribe()
            pool.pop(self.code)
            return
        living_connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections