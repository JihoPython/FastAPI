from dataclasses import dataclass


@dataclass
class LivePrice:
    code: str
    name: str
    price: int
    time: int

    @property
    def __dict__(self):
        return {
            'code': self.code,
            'name': self.name,
            'price': self.price,
            'time': self.time,
        }