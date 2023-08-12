from dataclasses import dataclass
from model_data.entity import Entity


@dataclass
class Pd(Entity):
    fio: tuple = None
    created_at: str = None
    closed_at: str = None


    def row(self) -> tuple:
        return str(self.pk), self.fio

