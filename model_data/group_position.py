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
class GroupPosition(Entity):
    name: str = None
    level: int = None

    @classmethod
    def select(cls) -> List["GroupPosition"]:
        g_poss = list()
        try:
            cursor = Db.select(query["GroupPosition"]["_SELECT"])
            for p in cursor:
                g_poss.append(GroupPosition(*p))
        except SqlError as ex:
            LOG.info("Ошибка получения списка групп должностей: {0}".format(ex.args[0]))
        return g_poss

    def row(self) -> tuple:
        return self.pk, self.name, self.level

    @property
    def data(self):
        return self.name, self.level

    def load(self) -> "GroupPosition":
        cursor = Db.select(query["GroupPosition"]["_SELECT_ONE"], (self.pk, ))
        data = cursor.fetchone()
        self.pk = data[0]
        self.name = data[1]
        self.level = data[2]
        return self

    def load_by_name(self):
        cursor = Db.select(query["GroupPosition"]["_SELECT_BY_NAME"], (self.name, ))
        data = cursor.fetchone()
        self.pk = data[0]
        self.level = data[2]
        return self

    def __insert(self):
        try:
            self.pk = Db.insert(query["GroupPosition"]["_INSERT"], self.data)
        except SqlError as ex:
            LOG.info("Ошибка вставки группы должностей: {0}".format(ex.args[0]))

    def __update(self):
        try:
            Db.update(query["GroupPosition"]["_UPDATE"], [(self.name, self.level, self.pk,)])
        except SqlError as ex:
            LOG.info("Ошибка обновления группы должностей: {0}".format(ex.args[0]))

    def save(self):
        if self.pk is None:
            return self.__insert()
        else:
            return self.__update()
