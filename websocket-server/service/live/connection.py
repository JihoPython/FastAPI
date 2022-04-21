from typing import List
from fastapi import WebSocket

from .live_price_api import LivePriceAPI

from utils import logger

class Channel:
    def __init__(self, code: str) -> None:
        self.connections: List[WebSocket] = []
        """WebSocket 인스턴스가 저장된 list"""
        self.generator = self._generator()
        """broadcast를 수행하는 AsyncGenerator"""
        self.code = code
        """채널이 현재가를 수신하는 종목의 코드"""

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
        """generator에 broadcast 할 메시지를 전송"""
        await self.generator.asend(self.api.message)

    async def remove(self, websocket: WebSocket):
        """연결이 끊어진 Websocket을 connections에서 제거"""
        try:
            logger.warn(f"{websocket} 연결이 끊어져 connections에서 제거합니다.")
            self.connections.remove(websocket)
        except:
            pass

    async def _generator(self):
        """전송할 메시지가 올 때까지 대기하다가 메시지가 생기면 발행
        """
        while True:
            message = yield
            await self._broadcast(message)

    async def _broadcast(self, message: str):
        """connetions에 등록된 websockets에 메시지를 발행한다.

        connections에서 웹소켓이 제거되어 message를 연결하려는 도중에
        client과 연결이 끊어질 경우에 대한 예외처리 병행
        """
        living_connections = []

        while len(self.connections) > 0:
            try:
                websocket = self.connections.pop()
                await websocket.send_text(message)
                living_connections.append(websocket)
            except Exception as e:
                yellow = ['\033[1;33m', '\033[0m']
                logger.warn( f'broadcast 중 {websocket} 연결 끊어짐: {e}'.join(yellow))

        if len(living_connections) == 0:
            error_msg = '활성화된 websocket이 없으므로 channel을 닫습니다.'
            logger.error(error_msg)
            raise Exception(error_msg)

        self.connections = living_connections

