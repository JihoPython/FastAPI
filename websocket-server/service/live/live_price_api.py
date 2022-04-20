import json
from models.creon.creon_plus import Win32Client

from models.creon import CreonAPI, EventHandler
from models.creon.constants import STOCK_CUR
from models.dto import LivePrice


class LivePriceHandler(EventHandler):
    def init(self, api: CreonAPI, dto: LivePrice) -> None:
        self.api = api
        self.dto = dto

    def OnReceived(self):
        self.dto.code  = self.api.get_header_value(0)
        self.dto.name  = self.api.get_header_value(1)
        self.dto.price = self.api.get_header_value(13)
        self.dto.time  = self.api.get_header_value(18)


class LivePriceAPI:
    def __init__(self, code: str) -> None:
        self.api = CreonAPI(STOCK_CUR)
        self.api.set_input_value(0, code)
        self.dto = LivePrice('', '', 0, 0)
        self.handler: LivePriceHandler

    @property
    def message(self) -> str:
        return json.dumps(self.dto.__dict__)

    def subscribe(self):
        self.handler = Win32Client.bind(self.api, LivePriceHandler)
        self.handler.init(self.api, self.dto)
        self.api.subscribe()

    def unsubscribe(self):
        self.api.unsubscribe()
