from dataclasses import dataclass
from model_data.entity import Entity


@dataclass
class Npa(Entity):
    code: str
    name: str

    def row(self) -> tuple:
        return str(self.pk), self.code, self.name
