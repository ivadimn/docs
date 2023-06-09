from dataclasses import dataclass
from model_data.entity import Entity


@dataclass
class Pd(Entity):
    name: str
    comment: str

    def row(self) -> tuple:
        return str(self.id), self.name, self.comment

