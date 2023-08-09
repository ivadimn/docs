from dataclasses import dataclass
from typing import Optional
from model_data.entity import Entity
from datetime import date


@dataclass
class Dep(Entity):
    code: str = None
    name: str = None
    created_at: str = None
    closed_at: str = None

    def row(self) -> tuple:
        return self.pk, self.code, self.name, self.created_at, self.closed_at

    def __eq__(self, other: "Dep"):
        return self.name.upper() == other.name.upper()

    def extract_code(self):
        nc = self.name.strip().split(" ")
        if len(nc) == 1:
            return nc[0]
        else:
            return nc[-1]
