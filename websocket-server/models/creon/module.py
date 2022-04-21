from abc import ABC, abstractmethod
from typing import Union


class CreonModule(ABC):
    @abstractmethod
    def GetHeaderValue(self, type: int) -> Union[str, int, float]:
        pass
    @abstractmethod
    def SetInputValue(self, type: int, code: str):
        pass
    @abstractmethod
    def Subscribe(self):
        pass
    @abstractmethod
    def Unsubscribe(self):
        pass