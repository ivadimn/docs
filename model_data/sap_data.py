from dataclasses import dataclass
from model_data.entity import Entity
from .face import Face
from .dep import Dep

@dataclass
class SapData(Entity):
    tn: int = None
    snils: str = None
    birthday: str = None
    firstname: str = None
    name: str = None
    fathername: str = None
    dep: str = None
    upr: str = None
    otdel: str = None

    def row(self) -> tuple:
        return self.tn, self.snils, self.birthday, "{} {} {}".format(self.firstname, self.name, self.fathername),

    @property
    def face(self):
        return Face(self.pk, self.snisl, self.birthday)

