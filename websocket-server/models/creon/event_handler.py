from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from models.creon.creon_plus import CreonAPI


class EventHandler(ABC):
    @abstractmethod
    def init(self, api: 'CreonAPI', dto: Any) -> None:
        pass
    @abstractmethod
    def OnReceived(self) -> None:
        pass