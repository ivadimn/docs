from PyQt6.QtSql import QSqlQuery
from typing import Optional, List
from repositories.repository import Repository
from model_data.position import Position


class PosRepository(Repository):

    _SELECT_ONE = """
        SELECT id, name, group_id
            FROM position 
            WHERE id=? ;
    """
    _SELECT = """
        SELECT id, name, group_id
            FROM position ;
    """
    _SELECT_BY_NAME = """
        SELECT id, name, group_id
            FROM position 
            WHERE name=? ;
    """
    _INSERT = """
        INSERT INTO position (name)
               VALUES(?) ;
    """
    _UPDATE = """
        UPDATE position
             SET name=?, group_id=?  
             WHERE id=? ;
            """
    _DELETE = """
        DELETE FROM position WHERE id=? ;
    """
    _INSERT_TMP = """
        INSERT INTO tmp_pos (name) VALUES(?) ; 
    """
    _INSERT_LOADED = """
        INSERT INTO position (name) 
        SELECT name 
        FROM tmp_pos
        WHERE name not in ( SELECT name FROM position) ;
    """
    _DELETE_TMP = """
        DELETE FROM tmp_pos ; 
    """

    def select_one(self, pk: int) -> Optional[Position]:
        query = QSqlQuery()
        query.prepare(self._SELECT_ONE)
        query.addBindValue(pk)
        query.exec()
        if query.first():
            return Position(query.value("id"), query.value("name"), query.value("group_id"))
        else:
            return None

    def select(self, params: dict) -> List[Position]:
        query = QSqlQuery()
        query.prepare(self._SELECT)
        query.exec()
        poss = self.__extract_data(query)
        return poss

    def insert(self, entities: List[Position]) -> Optional[int]:
        query = QSqlQuery()
        query.prepare(self._INSERT)
        pk = 0
        for group in entities:
            # print(org.row())
            query.addBindValue(group.name)
            query.exec()
            pk = query.lastInsertId()
        return pk

    def delete(self, params: dict) -> None:
        query = QSqlQuery()
        query.prepare(self._DELETE)
        query.addBindValue(params["pk"])
        query.exec()

    def update(self, pos: Position) -> None:
        query = QSqlQuery()
        query.prepare(self._UPDATE)
        query.addBindValue(pos.name)
        query.addBindValue(pos.group_id)
        query.addBindValue(pos.pk)
        query.exec()

    def __extract_data(self, query: QSqlQuery) -> List[Position]:
        poss = list()
        while query.next():
            poss.append(Position(query.value("id"), query.value("name"), query.value("group_id")))
        return poss

    def load_from_list(self, data: List[str]):
        query = QSqlQuery()
        query.prepare(self._INSERT_TMP)
        query.addBindValue(data)
        if query.execBatch(QSqlQuery.BatchExecutionMode.ValuesAsRows):
            if self.__insert_loaded():
                self.__delete_tmp()
            else:
                print("Load from tmp error: {0}".format(query.lastError().text()))
        else:
            print("Insert into tmp error: {0}".format(query.lastError().text()))

    def __insert_loaded(self) -> bool:
        query = QSqlQuery()
        query.prepare(self._INSERT_LOADED)
        return query.exec()

    def __delete_tmp(self):
        query = QSqlQuery()
        query.prepare(self._DELETE_TMP)
        query.exec()
