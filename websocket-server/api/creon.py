from email import message
from typing import List

from fastapi import WebSocket


class Publisher:
    def __init__(self) -> None:
        self.connections: List[WebSocket] = []
        self.generator = self.get_publish_generator()

    async def get_publish_generator(self):
        while True:
            message = yield
            await self._broadcast(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _broadcast(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections


class LivePriceEvent:
    def set_client(self, client, callback):
        self.client = client
        self.callback = callback

    def OnReceived(self):
        code = self.client.GetHeaderValue(0)
        name = self.client.GetHeaderValue(1)
        price = self.client.GetHeaderValue(13)
        time = self.client.GetHeaderValue(18)

        print(code, name, price, time)


class Bridge:

    def __init__(self) -> None:
        import win32com.client

        self.connections: List[WebSocket] = []
        self.generator = self.get_publish_generator()

        self.is_subscribe = False
        self.client = win32com.client.Dispatch('DsCbo1.StockCur')

    async def get_publish_generator(self):
        import pythoncom
        while True:
            message = yield
            pythoncom.PumpWaitingMessages()
            await self._broadcast(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    def subscribe(self, code: str = 'A005930'):
        """
        Creon API Subscribe
        """
        import win32com.client
        if self.is_subscribe:
            self.unsubscribe()

        print(code)
        self.client.SetInputValue(0, code)

        handler = win32com.client.WithEvents(self.client, LivePriceEvent)
        handler.set_client(self.client, self.push)
        handler.client.Subscribe()

        self.is_subscribe = True

    def unsubscribe(self):
        if self.is_subscribe:
            self.client.Unsubscribe()
        self.is_subscribe = False

    async def _broadcast(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections