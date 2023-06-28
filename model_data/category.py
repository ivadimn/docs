from dataclasses import dataclass
from model_data.entity import Entity


@dataclass
class Category(Entity):
    code: str
    name: str

    def row(self) -> tuple:
        return str(self.id), self.code, self.name
