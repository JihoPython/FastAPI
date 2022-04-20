from abc import ABC, abstractmethod
from typing import Union

from utils.win32com_client import Win32Client


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


class CreonAPI:
    api: CreonModule

    def __init__(self, module_name: str) -> None:
        self.api = Win32Client.dispatch(module_name)

    def get_header_value(self, type: int) -> Union[str, int, float]:
        self.api.GetHeaderValue(type)

    def set_input_value(self, type: int, code: str):
        self.api.SetInputValue(type, code)

    def subscribe(self):
        self.api.Subscribe()

    def unsubscribe(self):
        self.api.Subscribe()

