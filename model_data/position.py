from dataclasses import dataclass
from model_data.entity import Entity


@dataclass
class Position(Entity):
    name: str = None
    group_id: int = None

    def row(self) -> tuple:
        return self.pk, self.name, self.group_id

    def __eq__(self, other):
        return self.name == other.name
