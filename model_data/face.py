from dataclasses import dataclass
from typing import Optional
from model_data.entity import Entity
from datetime import date


@dataclass
class Face(Entity):
    tn: int = None
    snils: str = None
    birthday: str = None
    firstname: str = None
    name: str = None
    fathername: str = None
    dep: str = None

    def row(self) -> tuple:
        return self.pk, self.tn, self.snils, self.birthday, "{0} {1} {2}".format(self.firstname, self.name, self.fathername)

    def __eq__(self, other: "Dep"):
        return self.snils == other.snils
