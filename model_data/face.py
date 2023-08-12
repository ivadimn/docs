from dataclasses import dataclass
from model_data.entity import Entity


@dataclass
class Face(Entity):
    tn: int = None
    snils: str = None
    birthday: str = None
    fio: tuple = None
    org_id: int = None

    def row(self) -> tuple:
        return self.pk, self.snils, self.birthday

    def __eq__(self, other: "Face"):
        return self.snils == other.snils



