from sqlite3 import Error as SqlError
from dataclasses import dataclass
from typing import List
from db.sql import query
from db.db import Db
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@dataclass
class Staff:
    position: str = None
    tn: int = None
    firstname: str = None
    name: str = None
    fathername: str = None

    @classmethod
    def select(cls) -> List["Staff"]:
        staffs = list()
        try:
            cursor = Db.select(query["Staff"]["_SELECT"])
            for st in cursor:
                staffs.append(Staff(position=st[0], tn=st[1], firstname=st[2], name=st[3], fathername=st[4]))
        except SqlError as ex:
            LOG.info("Ошибка получения списка работников: {0}".format(ex.args[0]))
        return staffs

    @classmethod
    def select_staffs(cls, org_id: int) -> List["Staff"]:
        staffs = list()
        try:
            cursor = Db.select(query["Staff"]["_SELECT"], (org_id, ))
            for st in cursor:
                staffs.append(Staff(position=st[0], tn=st[1], firstname=st[2], name=st[3], fathername=st[4]))
        except SqlError as ex:
            LOG.info("Ошибка получения списка работников: {0}".format(ex.args[0]))
        return staffs

    @property
    def row(self):
        return self.position, self.tn, self.firstname, self.name, self.fathername