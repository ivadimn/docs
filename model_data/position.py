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

    @property
    def data(self):
        return self.name, self.group_id

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

    def load(self, pk: int) -> "Position":
        cursor = Db.select(query["Position"]["_SELECT_ONE"], (self.pk,))
        data = cursor.fetchone()
        self.name = data[1]
        self.group_id = data[2]
        self.group_name = data[3]
        return self

    def __insert(self):
        try:
            self.pk = Db.insert(query["Position"]["_INSERT"], self.data)
        except SqlError as ex:
            LOG.info("Ошибка вставки должности: {0}".format(ex.args[0]))

    def __update(self):
        try:
            Db.update(query["Position"]["_UPDATE"], [(self.name, self.group_id, self.pk,)])
        except SqlError as ex:
            LOG.info("Ошибка обновления должности: {0}".format(ex.args[0]))

    def save(self):
        if self.pk is None:
            return self.__insert()
        else:
            return self.__update()

    def row(self) -> tuple:
        return self.pk, self.name, self.group_id, self.group_name

    def __eq__(self, other):
        return self.name == other.name
