from dataclasses import dataclass


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