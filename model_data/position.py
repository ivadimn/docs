from sqlite3 import Error as SqlError
from dataclasses import dataclass
from typing import List
from model_data.entity import Entity
from db.db import Db
from db.sql import query

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@dataclass
class Position(Entity):
    name: str = None
    group_id: int = None
    group_name: str = None

    @classmethod
    def select(cls) -> List["Position"]:
        poss = list()
        try:
            cursor = Db.select(query["Position"]["_SELECT"])
            for p in cursor:
                poss.append(Position(*p))
        except SqlError as ex:
            LOG.info("Ошибка получения списка должностей: {0}".format(ex.args[0]))
        return poss

    @classmethod
    def load_from_list(cls, data: List[str]):
        try:
            Db.update(query["Position"]["_INSERT_TMP"], [(pos,) for pos in data])
            Db.update(query["Position"]["_INSERT_LOADED"], [])
            Db.update(query["Position"]["_DELETE_TMP"], [])
        except SqlError as ex:
            LOG.info("Ошибка загрузки списка должностей: {0}".format(ex.args[0]))

    def row(self) -> tuple:
        return self.pk, self.name, self.group_id

    def __eq__(self, other):
        return self.name == other.name
