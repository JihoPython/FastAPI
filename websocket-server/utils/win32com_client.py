import win32com.client

from models.creon import CreonAPI, EventHandler


class Win32Client:
    @staticmethod
    def dispatch(module: str) -> CreonAPI:
        return win32com.client.Dispatch(module)

    @staticmethod
    def bind(api: CreonAPI, handler: EventHandler) -> EventHandler:
        return win32com.client.WithEvents(api, handler)
