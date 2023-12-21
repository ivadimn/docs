
from hashlib import sha1
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
class Pd(Entity):
    face_id: int = None
    firstname: str = None
    name: str = None
    fathername: str = None
    created_at: str = None
    closed_at: str = None

    @classmethod
    def select(cls) -> List["Pd"]:
        pds = list()
        try:
            cursor = Db.select(query["Pd"]["_SELECT"])
            for pd in cursor:
                pds.append(Pd(pk=pd[0], face_id=pd[1], firstname=pd[2], name=pd[3], fathername=pd[4]))
        except SqlError as ex:
            LOG.info("Ошибка получения персональных данных: {0}".format(ex.args[0]))
        return pds

    @classmethod
    def select_tmp(cls) -> List["Pd"]:
        pds = list()
        try:
            cursor = Db.select(query["Pd"]["_SELECT_TMP"])
            for pd in cursor:
                pds.append(Pd(face_id=pd[0], firstname=pd[1], name=pd[2], fathername=pd[3]))
        except SqlError as ex:
            LOG.info("Ошибка получения временных персональных данных: {0}".format(ex.args[0]))
        return pds

    @classmethod
    def load_from_tmp(cls):
        pds = set(cls.select())
        pds_tmp = set(cls.select_tmp())
        dpd = pds_tmp - pds
        if len(dpd) > 0:
            Db.update(query["Pd"]["_INSERT"], [(pd.face_id, pd.firstname, pd.name, pd.fathername,) for pd in dpd])
        dpclose = (pds - pds_tmp)
        if len(dpclose) > 0:
            # закрыть в штатном расписании
            Db.update(query["Pd"]["_CLOSE"], [(pd.pk,) for pd in dpclose])

    @property
    def row(self) -> tuple:
        return self.pk, self.face_id, self.firstname, self.name, self.fathername

    def __eq__(self, other):
        return (self.face_id == other.face_id and self.firstname == other.firstname and self.name == other.name and
                self.fathername == other.fathername)

    def __hash__(self):
        data = "{0}{1}{2}{3}".format(self.face_id, self.firstname, self.name, self.fathername)
        hash_code = int(sha1(data.encode("utf-8")).hexdigest(), 16)
        return hash_code

    def save(self):
        try:
            self.pk = Db.insert(query["Pd"]["_INSERT"], self.row[1:])
        except SqlError as ex:
            LOG.info("Ошибка вставки персональных данных: {0}".format(ex.args[0]))