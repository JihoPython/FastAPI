from abc import ABC, abstractmethod
from typing import Any

from models.creon import CreonAPI
from models.dto import LivePrice


class EventHandler(ABC):
    @abstractmethod
    def init(self, api: CreonAPI, dto: Any) -> None:
        pass
    @abstractmethod
    def OnReceived(self) -> None:
        pass