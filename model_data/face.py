from sqlite3 import Error as SqlError
from dataclasses import dataclass
from typing import List
from model_data.entity import Entity
from db.sql import query
from db.db import Db

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

@dataclass
class Face(Entity):
    tn: int = None
    snils: str = None
    birthday: str = None
    fio: tuple = None
    org_name: str = None
    position: str = None

    @classmethod
    def select(cls) -> List["Face"]:
        faces = list()
        try:
            cursor = Db.select(query["Face"]["_SELECT"])
            for f in cursor:
                faces.append(Face(pk=f[0], snils=f[1], birthday=f[2]))
        except SqlError as ex:
            LOG.info("Ошибка получения списка лиц: {0}".format(ex.args[0]))
        return faces

    @classmethod
    def load_from_list(cls, data: List["Face"]):
        try:
            Db.update(query["Face"]["_INSERT_TMP"],
                      [(face.snils, face.birthday, face.tn, face.fio[0],
                        face.fio[1], face.fio[2], face.position) for face in data])
            Db.update(query["Face"]["_INSERT_LOADED"], [])
            #Db.update(query["Face"]["_DELETE_TMP"], [])
        except SqlError as ex:
            LOG.info("Ошибка загрузки списка лиц: {0}".format(ex.args[0]))

    @property
    def row(self) -> tuple:
        return self.pk, self.snils, self.birthday

    def __eq__(self, other: "Face"):
        return self.snils == other.snils



