from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Union

from utils.win32 import win_client

@dataclass
class LivePrice:
    code: str
    name: str
    price: int
    tume: int

    @property
    def __dict__(self):
        return {
            'code': self.code,
            'name': self.name,
            'price': self.price,
            'tume': self.tume,
        }


class API(ABC):
    @abstractmethod
    def GetHeaderValue(self, type: int) -> Union[str, int]:
        pass
    @abstractmethod
    def SetInputValue(self, type: int, code: str):
        pass
    @abstractmethod
    def Unsubscribe(self):
        pass
    @abstractmethod
    def Subscribe(self):
        pass


class EventHandler(ABC):
    @abstractmethod
    def init(self, api: API, dto: LivePrice) -> None:
        pass
    @abstractmethod
    def OnReceived(self) -> None:
        pass


class LivePriceHandler(EventHandler):
    def init(self, api: API, dto: LivePrice) -> None:
        self.api = api
        self.dto = dto

    def OnReceived(self):
        self.dto.code  = self.api.GetHeaderValue(0)
        self.dto.name  = self.api.GetHeaderValue(1)
        self.dto.price = self.api.GetHeaderValue(13)
        self.dto.time  = self.api.GetHeaderValue(18)

class LivePriceAPI:
    MODULE_NAME = 'DsCbo1.StockCur'
    api: API
    is_subscribe: bool
    handler: LivePriceHandler
    dto: LivePrice

    def __init__(self, code: str) -> None:
        # TODO 실제 크레온 프로세스가 정상적으로 동작 중인지 확인
        self.api = win_client.dispatch(self.MODULE_NAME)
        self.is_subscribe = False
        self.set_value(code)

    @property
    def message(self) -> str:
        return json.dumps(self.dto.__dict__)

    def set_value(self, code: str):
        self.api.SetInputValue(0, code)

    def subscribe(self):
        self.handler = win_client.bind(self.api, LivePrice)
        self.handler.init(self.api, self.dto)
        self.api.Subscribe()
        self.is_subscribe = True

    def unsubscribe(self):
        self.api.Unsubscribe()
        self.is_subscribe = False

live_price_api = LivePriceAPI()