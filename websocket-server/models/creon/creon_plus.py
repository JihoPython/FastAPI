from typing import Any, Union

from win32com.client import _PyIDispatchType

from .module import CreonModule
from utils.win32com_client import Win32Client


class CreonAPI:
    creon_module: Union[CreonModule, Any]

    def __init__(self, module_name: str) -> None:
        self.creon_module = Win32Client.dispatch(module_name)

    # win32com.client Event 엮는 부분 때문에 사용할 수 없으므로 사실상 죽은 코드
    def get_header_value(self, type: int) -> Union[str, int, float]:
        self.creon_module.GetHeaderValue(type)

    def set_input_value(self, type: int, code: str):
        self.creon_module.SetInputValue(type, code)

    def subscribe(self):
        self.creon_module.Subscribe()

    def unsubscribe(self):
        self.creon_module.Subscribe()

