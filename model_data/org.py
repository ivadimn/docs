import sqlite3
from sqlite3 import Error as SqlError
from dataclasses import dataclass
from typing import Optional, List
from model_data.entity import Entity
from datetime import date
from db.db import Db
from db.sql import query
from settings import date_format
import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@dataclass
class Org(Entity):
    code: str = None
    name: str = None
    parent_id: Optional[int] = None
    created_at: str = None
    closed_at: Optional[str] = None
    child: Optional[list] = None

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

    @classmethod
    def __select(cls, sql: str, params: tuple = None) -> List["Org"]:
        poss = list()
        try:
            cursor = Db.select(sql, params)
            for p in cursor:
                poss.append(Org(*p))
        except SqlError as ex:
            LOG.info("Ошибка получения списка орг. единиц: {0}".format(ex.args[0]))
        return poss

    @classmethod
    def select(cls) -> List["Org"]:
        return cls.__select(query["Org"]["_SELECT"])

    @classmethod
    def select_first_level(cls) -> List["Org"]:
        return cls.__select(query["Org"]["_SELECT_FIRST_LEVEL"])

    @classmethod
    def select_child(cls, parent_id: int) -> List["Org"]:
        return cls.__select(query["Org"]["_SELECT_LEVEL_CHILD"], (parent_id,))

    @classmethod
    def insert(cls, entities: List["Org"]) -> int:
        rid = 0
        for org in entities:
            params = (org.code, org.name, org.parent_id, )
            rid = Db.insert(query["Org"]["_INSERT"], params)
            if org.parent_id is None:
                Db.insert(query["Org"]["_INSERT_TREE_PATH"], (rid, rid,))
            else:
                cursor = Db.select(query["Org"]["_SELECT_PARENTS"], (org.parent_id,))
                for row in cursor:
                    print("Parent: {0}, Child: {1}".format(row[0], rid))
                    Db.insert(query["Org"]["_INSERT_TREE_PATH"], (row[0], rid,))
                print("-------------------------------------------------------------")
                print("Parent: {0}, Child: {1}".format(org.parent_id, rid))
                Db.insert(query["Org"]["_INSERT_TREE_PATH"], (org.parent_id, rid,))
        return rid

    @classmethod
    def close(cls, pks: List[int]):
        Db.update(query["Org"]["_CLOSE"], [(pk,) for pk in pks])

    def load_by_name(self):
        cursor = Db.select(query["Org"]["_SELECT_BY_NAME"], (self.name, ))
        data = cursor.fetchone()
        self.pk = data[0]
        self.code = data[1]
        self.parent_id = data[3]
        self.created_at = data[4]
        return self

    @property
    def row(self) -> tuple:
        return self.pk, self.code, self.name, self.parent_id

    def __eq__(self, other: "Org"):
        return self.name.upper() == other.name.upper()

    def __str__(self):
        return "{0} {1} parent_id: {2}".format(self.code, self.name, self.parent_id)

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

