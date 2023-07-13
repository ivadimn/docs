from dataclasses import dataclass
from model_data.entity import Entity


@dataclass
class Org(Entity):
    code: str
    name: str
    parent_id: int

    def row(self) -> tuple:
        return str(self.id), self.code, self.name, str(self.parent_id)
    