from PyQt6.QtSql import QSqlQuery
from typing import Optional, List
from repositories.repository import Repository
from model_data.group_position import GroupPosition


class GroupPosRepository(Repository):

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

    def select_one(self, pk: int) -> Optional[GroupPosition]:
        query = QSqlQuery()
        query.prepare(self._SELECT_ONE)
        query.addBindValue(pk)
        query.exec()
        if query.first():
            return GroupPosition(query.value("id"), query.value("name"), query.value("level"))
        else:
            return None

    def select(self, params: dict) -> List[GroupPosition]:
        query = QSqlQuery()
        query.prepare(self._SELECT)
        query.exec()
        groups = self.__extract_data(query)
        return groups

    def insert(self, entities: List[GroupPosition]) -> Optional[int]:
        query = QSqlQuery()
        query.prepare(self._INSERT)
        pk = 0
        for group in entities:
            # print(org.row())
            query.addBindValue(group.name)
            query.addBindValue(group.level)
            query.exec()
            pk = query.lastInsertId()
        return pk

    def delete(self, params: dict) -> None:
        query = QSqlQuery()
        query.prepare(self._DELETE)
        query.addBindValue(params["pk"])
        query.exec()

    def update(self, group: GroupPosition) -> None:
        query = QSqlQuery()
        query.prepare(self._UPDATE)
        query.addBindValue(group.name)
        query.addBindValue(group.level)
        query.addBindValue(group.pk)
        query.exec()

    def __extract_data(self, query: QSqlQuery) -> List[GroupPosition]:
        groups = list()
        while query.next():
            groups.append(GroupPosition(query.value("id"), query.value("name"), query.value("level")))
        return groups
