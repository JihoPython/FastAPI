from typing import List, Tuple

from fastapi import WebSocket
import win32com.client


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
    def set_client(self, client, price: List):
        self.client = client
        self.price = price

    def OnReceived(self):
        # values = []
        # values.append(self.client.GetHeaderValue(0))
        # values.append(self.client.GetHeaderValue(1))
        # values.append(self.client.GetHeaderValue(13))
        # values.append(self.client.GetHeaderValue(18))
        # for i in range(4):
        #     self.price[i] = values[i]

        code = self.client.GetHeaderValue(0)
        name = self.client.GetHeaderValue(1)
        price= self.client.GetHeaderValue(13)
        time = self.client.GetHeaderValue(18)

        self.price[0] = code
        self.price[1] = name
        self.price[2] = price
        self.price[3] = time


class Bridge:

    def __init__(self) -> None:
        self.connections: List[WebSocket] = []
        self.generator = self.get_publish_generator()

        self.live_price = [0, 0, 0, 0]

        self.is_subscribe = False
        self.client = win32com.client.Dispatch('DsCbo1.StockCur')
        self.subscribe()

    async def get_publish_generator(self):
        while True:
            message = yield
            await self._broadcast(message)

    async def push(self, msg: str = False):
        if msg:
            await self.generator.asend(msg)
        else:
            msg = f"{self.live_price[0]}, {self.live_price[1]}, {self.live_price[2]}, {self.live_price[3]}"
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
        if self.is_subscribe:
            self.unsubscribe()

        print(code)
        self.client.SetInputValue(0, code)

        handler = win32com.client.WithEvents(self.client, LivePriceEvent)
        handler.set_client(self.client, self.live_price)
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