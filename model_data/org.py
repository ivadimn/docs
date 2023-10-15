from dataclasses import dataclass
from typing import Optional
from model_data.entity import Entity
from datetime import date


@dataclass
class Org(Entity):
    code: str = None
    name: str = None
    parent_id: Optional[int] = None
    created_at: str = None
    closed_at: Optional[str] = None
    child: Optional[list] = None

    def row(self) -> tuple:
        return str(self.pk), self.code, self.name, str(self.parent_id)

    def __eq__(self, other: "Org"):
        return self.name.upper() == other.name.upper()

    def __str__(self):
        return "{0} {1} parent_id: {2}".format(self.code, self.name, self.parent_id)

    @classmethod
    def extract_code(cls, name: str) -> str:
        nc = name.strip().split(" ")
        if len(nc) == 1:
            return nc[0]
        else:
            return nc[-1]

    @classmethod
    def get_parent_code(cls, code: str):
        codes = code.split("/")
        if len(codes) < 3:
            return codes[0]
        return "/".join(codes[:-1])


@dataclass
class OrgForLoading:
    code: str = None
    name: str = None
    parent_name: str = None

    def __eq__(self, other):
        return self.name == other.name and self.code == other.code

    def clear(self):
        self.code = ""
        self.name = ""
        self.parent_name = ""

    def is_empty(self):
        return self.code == "" and self.name == ""

