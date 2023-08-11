import pandas as pd
from dataclasses import dataclass
from typing import Optional, List
from model_data.entity import Entity
from datetime import date


@dataclass
class Dep(Entity):
    code: str = None
    name: str = None
    parent_code: str = None
    childs: List["Dep"] = None

    def row(self) -> tuple:
        return self.pk, self.code, self.name,

    def __eq__(self, other: "Dep"):
        return self.name.upper() == other.name.upper()

