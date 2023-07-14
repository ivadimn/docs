from dataclasses import dataclass
from typing import Optional
from model_data.entity import Entity
from datetime import date


@dataclass
class Org(Entity):
    code: str
    name: str
    code_word: Optional[str]
    parent_id: Optional[int]
    created_at: str
    closed_at: Optional[str]

    def row(self) -> tuple:
        return str(self.id), self.code, self.name, self.code_word, str(self.parent_id)

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def extract_code(cls, name: str) -> str:
        nc = name.split(" ")
        if len(nc) == 1:
            return nc[0]
        else:
            return nc[1]
