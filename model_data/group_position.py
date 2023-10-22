from PyQt6.QtSql import QSqlQuery
from dataclasses import dataclass
from typing import List
from model_data.entity import Entity
import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@dataclass
class GroupPosition(Entity):
    name: str = None
    level: int = None

    _SELECT = """
           SELECT id, name, level FROM group_position ;
       """
    _SELECT_ONE = """
           SELECT id, name, level 
               FROM group_position
               WHERE id=? ;
           """
    _INSERT = """
           INSERT INTO group_position (name, level)
           VALUES(?, ?) ;
    """
    _UPDATE = """
           UPDATE group_position
           SET name=?, level=?  
           WHERE id=? ;
    """
    _DELETE = """
           DELETE FROM group_position WHERE id=? ;
    """

    def row(self) -> tuple:
        return self.pk, self.name, self.level

    @property
    def data(self):
        return self.name, self.level

    @classmethod
    def select(cls) -> List["GroupPosition"]:
        data: List[GroupPosition] = list()
        query = QSqlQuery()
        query.prepare(cls._SELECT)
        if query.exec():
            while query.next():
                data.append(GroupPosition(query.value("id"), query.value("name"), query.value("level")))
        return data

    def load(self) -> "GroupPosition":
        query = QSqlQuery()
        query.prepare(self._SELECT_ONE)
        query.addBindValue(self.pk)
        if query.exec() and query.first():
            self.name = query.value("name")
            self.level = query.value("level")
        else:
            LOG.info(query.lastError().text())
        return self

    def __insert(self):
        query = QSqlQuery()
        data = self.data
        query.prepare(self._INSERT)
        query.addBindValue(data[0])
        query.addBindValue(data[1])
        if query.exec():
            self.pk = query.lastInsertId()
            LOG.info("Group {0} inserted successfully!".format(self.name))
        else:
            LOG.info(query.lastError().text())

    def __update(self):
        query = QSqlQuery()
        data = self.data
        query.prepare(self._INSERT)
        query.addBindValue(data[0])
        query.addBindValue(data[1])
        query.addBindValue(self.pk)
        if query.exec():
            LOG.info("Group {0} inserted successfully!".format(self.name))
        else:
            LOG.info(query.lastError().text())

    def save(self):
        if self.pk is None:
            return self.__insert()
        else:
            return self.__update()


