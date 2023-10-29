from PyQt6.QtSql import QSqlQuery
import sqlite3 as sql3
from typing import Optional, List
from repositories.repository import Repository
from model_data.org import Org
from model_data.dep import Dep
from datetime import date
from settings import date_format
from db.connection import Connection


class OrgRepository(Repository):
    _SELECT_ONE = """
        SELECT id, code, name, parent_id, created_at FROM org WHERE id=?; """
    _SELECT_BY_NAME = """
           SELECT id, code, name, parent_id, created_at FROM org WHERE name=?; """
    _SELECT_LEVEL_CHILD = """ 
        SELECT id, code, name, parent_id, created_at FROM org WHERE parent_id=?; """
    _SELECT_FIRST_LEVEL = """
        SELECT id, code, name, parent_id, created_at 
        FROM org 
        WHERE parent_id is NULL and closed_at is NULL 
        ORDER BY code ; """
    _SELECT_TREE = """
        SELECT id, code, name, parent_id, created_at 
        FROM org 
        WHERE parent_id = ? and closed_at is NULL ; """
    _SELECT = """
            SELECT id, code, name, parent_id, created_at 
            FROM org 
            WHERE closed_at is NULL ; """
    _SELECT_PARENTS = """
        SELECT parent_id FROM tree_path WHERE child_id = ? ;
    """
    _INSERT = "INSERT INTO org (code, name, parent_id, created_at, closed_at) VALUES(?, ?, ?, ?, ?); "
    _INSERT_TREE_PATH = "INSERT INTO tree_path (parent_id, child_id) VALUES(?, ?) ; "
    _DELETE = "DELETE FROM org WHERE id=?; "
    _CLOSE = "UPDATE org SET closed_at=? WHERE id=? ;"

    def select_one(self, rid: int) -> Optional[Org]:
        query = QSqlQuery()
        query.prepare(self._SELECT_ONE)
        query.addBindValue(rid)
        query.exec()
        if query.first():
            return Org(query.value("id"), query.value("code"), query.value("name"),
                       query.value("parent-id"), query.value("created_at"))
        else:
            return None

    def select_by_name(self, code: str) -> Optional[Org]:
        query = QSqlQuery()
        query.prepare(self._SELECT_BY_NAME)
        query.addBindValue(code)
        query.exec()
        if query.first():
            return Org(query.value("id"), query.value("code"), query.value("name"),
                       query.value("parent_id"), query.value("created_at"))
        else:
            return None

    def __select_parents(self, child_id: int) -> List[int]:
        parents = list()
        query = QSqlQuery()
        query.prepare(self._SELECT_PARENTS)
        query.exec()
        while query.next():
            parents.append(query.value("parent_id"))
        return parents

    def select_tree(self, params: dict = None) -> List[Org]:
        query = QSqlQuery()
        if params["parent_id"] == 0:
            query.prepare(self._SELECT_FIRST_LEVEL)
        else:
            query.prepare(self._SELECT_TREE)
            query.addBindValue(params["parent_id"])
        query.exec()
        orgs = self.__extract_data(query)
        for org in orgs:
            params["parent_id"] = org.pk
            org.child = self.select(params)
        return orgs

    def select_child(self, parent_id: int) -> List[Org]:
        query = QSqlQuery()
        query.prepare(self._SELECT_LEVEL_CHILD)
        query.addBindValue(parent_id)
        if not query.exec():
            print(query.lastError().text())
            return []
        return self.__extract_data(query)

    def __extract_data(self, curr: sql3.Cursor) -> List[Org]:
        orgs = list()
        result = curr.fetchall()
        for o in result:
            # orgs.append(Org(o[0], o[1], o[2], o[3], o[4]))
            orgs.append(Org(*o))
            print(*o)
        return orgs

    def __insert_tree_path(self, parent_id: int, child_id: int) -> None:
        query = QSqlQuery()
        query.prepare(self._INSERT_TREE_PATH)
        query.addBindValue(parent_id)
        query.addBindValue(child_id)
        query.exec()

    def select(self, params: dict = None) -> List[Org]:
        query = QSqlQuery()
        query.prepare(self._SELECT)
        query.exec()
        orgs = self.__extract_data(query)
        return orgs

    def select_first_level(self) -> List[Org]:
        curr = Connection().connection.cursor()
        curr.execute(self._SELECT_FIRST_LEVEL)
        orgs = self.__extract_data(curr)
        return orgs

    def insert(self, entities: List[Org]) -> int:
        query = QSqlQuery()
        query.prepare(self._INSERT)
        rid = 0
        for org in entities:
            # print(org.row())
            query.addBindValue(org.code)
            query.addBindValue(org.name)
            query.addBindValue(org.parent_id)
            query.addBindValue(date.today().strftime(date_format))
            query.addBindValue(org.closed_at)
            query.exec()
            rid = query.lastInsertId()
            if org.parent_id is None:
                self.__insert_tree_path(rid, rid)
            else:
                list_parents = self.__select_parents(org.parent_id)
                for pid in list_parents:
                    self.__insert_tree_path(pid, rid)
                self.__insert_tree_path(org.parent_id, rid)
        return rid

    def delete(self, params: dict) -> None:
        query = QSqlQuery()
        query.prepare(self._DELETE)
        query.exec()

    def update(self, orgs: List[Dep]):
        orgs = self.select_first_level()

    def close(self, pks: List[int]):
        query = QSqlQuery()
        query.prepare(self._CLOSE)
        data = [date.today().strftime(date_format) for _ in pks]
        query.addBindValue(data)
        query.addBindValue(pks)
        if not query.execBatch():
            print(query.lastError().text())



class TreeRepository(Repository):

    def select(self, params: dict) -> List[Org]:
        pass

    def insert(self, entities: List[Org]) -> Optional[int]:
        pass

    def delete(self, params: dict) -> None:
        pass

    def select_one(self, rid: int) -> Org:
        pass

    def load_first(self, data: list):
        query = QSqlQuery()
        query.prepare("INSERT INTO tree (name, ord, dep) VALUES (?, ?, ?); ")
        for elem in data:
            query.addBindValue(elem[0])
            query.addBindValue(elem[1])
            query.addBindValue(elem[2])
            query.exec()


