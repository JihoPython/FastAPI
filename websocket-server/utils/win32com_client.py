from typing import TYPE_CHECKING

import win32com.client

if TYPE_CHECKING:
    from models.creon.creon_plus import CreonAPI
    from models.creon.event_handler import EventHandler


class Win32Client:
    @staticmethod
    def dispatch(module: str) -> 'CreonAPI':
        return win32com.client.Dispatch(module)

    @staticmethod
    def bind(api: 'CreonAPI', handler: 'EventHandler') -> 'EventHandler':
        return win32com.client.WithEvents(api, handler)
