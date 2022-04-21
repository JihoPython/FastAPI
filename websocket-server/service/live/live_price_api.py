
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from models.creon.module import CreonModule

from models.dto import LivePrice
from models.creon.creon_plus import CreonAPI
from models.creon.event_handler import EventHandler
from models.creon.creon_plus import Win32Client
from models.creon.constants import STOCK_CUR

from utils.LoggerConfig import logger


class LivePriceHandler(EventHandler):
    def init(self, module: 'CreonModule', dto: 'LivePrice') -> None:
        self.module = module
        self.dto = dto

    def OnReceived(self):
        # 종목 코드는 변할 경우가 없다고 판단되어 dto에 값을 재할당하는 것은 넘어감
        # self.dto.code  = self.module.GetHeaderValue(0)
        self.dto.name  = self.module.GetHeaderValue(1)
        self.dto.price = self.module.GetHeaderValue(13)
        self.dto.time  = self.module.GetHeaderValue(18)

        logger.info(f"[{self.dto.code} {self.dto.name}] [time {self.dto.time}] {self.dto.price}")


# TODO CreonAPI 객체를 상속하는 형태로 가능한지 검토 / 그 경우 CreonAPI는 추상 클래스로 작성
class LivePriceAPI:
    def __init__(self, code: str) -> None:
        self.api = CreonAPI(STOCK_CUR)
        self.api.set_input_value(0, code)
        self.dto = LivePrice(code, None, 0, 0)
        self.handler: LivePriceHandler

    @property
    def message(self) -> str:
        """json message from dto"""
        # 유니코드로 값이 할당되기 때문에 enscure_ascii 옵션을 False로 할당하여 한글이 깨지지 않게 처리함
        return json.dumps(self.dto.__dict__, ensure_ascii=False)

    def subscribe(self):
        self.handler = Win32Client.bind(self.api.creon_module, LivePriceHandler)
        self.handler.init(self.api.creon_module, self.dto)
        self.api.subscribe()

    async def unsubscribe(self):
        self.api.unsubscribe()
