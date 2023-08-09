from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from typing import Optional, List
from repositories.repository import Repository
from model_data.dep import Dep
from datetime import date
from settings import date_format
from db.connection import Connection


class DepRepository(Repository):

    _SELECT_ONE = """
            SELECT id, code, name, created_at, closed_at FROM dep WHERE id=?; """
    _SELECT_BY_NAME = """
               SELECT id, code, name, created_at, closed_at FROM dep WHERE name=?; """
    _SELECT = """
                SELECT id, code, name, created_at 
                FROM dep 
                WHERE closed_at is NULL ; """

    _INSERT = "INSERT INTO dep (code, name, created_at, closed_at) VALUES(?, ?, ?, ?); "
    _INSERT_WORD = "INSERT INTO dep_word (dep_id, code_word) VALUES(?, ?) ; "
    _DELETE = "UPDATE dep SET closed_at = ? WHERE id=?; "
    _UPDATE = "UPDATE dep_word SET code_word=? WHERE id=? ; "

    def select_one(self, rid: int) -> Optional[Dep]:
        query = QSqlQuery()
        query.prepare(self._SELECT_ONE)
        query.addBindValue(rid)
        query.exec()
        if query.first():
            return Dep(query.value("id"), query.value("code"), query.value("name"),
                       query.value("created_at"), query.value("closed_at"))
        else:
            return None

    def select_by_name(self, name: str) -> Optional[Dep]:
        query = QSqlQuery()
        query.prepare(self._SELECT_BY_NAME)
        query.addBindValue(name)
        query.exec()
        if query.first():
            return Dep(query.value("id"), query.value("code"), query.value("name"),
                       query.value("created_at"), query.value("closed_at"))
        else:
            return None

    def __extract_data(self, query: QSqlQuery) -> List[Dep]:
        orgs = list()
        while query.next():
            orgs.append(Dep(query.value("id"), query.value("code"), query.value("name"),
                            query.value("created_at"), query.value("closed_at")))
        return orgs

    def select(self, params: dict = None) -> List[Dep]:
        query = QSqlQuery()
        query.prepare(self._SELECT)
        query.exec()
        deps = self.__extract_data(query)
        return deps

    def insert(self, entities: List[Dep]) -> int:
        query = QSqlQuery()
        query.prepare(self._INSERT)
        pk = 0
        for dep in entities:
            print(dep.row())
            query.addBindValue(dep.code)
            query.addBindValue(dep.name)
            query.addBindValue(date.today().strftime(date_format))
            query.addBindValue(dep.closed_at)
            if query.exec():
                pk = query.lastInsertId()
                self.__insert_dep_word(pk)
            else:
                print(query.lastError().text())
        return pk

    def delete(self, params: dict) -> None:
        query = QSqlQuery()
        query.prepare(self._DELETE)
        query.addBindValue(date.today().strftime(date_format))
        query.addBindValue(params["pk"])
        query.exec()

    def __insert_dep_word(self, pk: int) -> bool:
        query = QSqlQuery()
        query.prepare(self._INSERT_WORD)
        query.addBindValue(pk)
        query.addBindValue(None)
        return query.exec()



