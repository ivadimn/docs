from dataclasses import dataclass
from model_data.entity import Entity


@dataclass
class Pd(Entity):
    name: str = None
    comment: str = None

    def row(self) -> tuple:
        return str(self.pk), self.name, self.comment

