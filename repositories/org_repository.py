from PyQt6.QtSql import QSqlQuery
from typing import Optional, List
from repositories.repository import Repository
from model_data.org import Org


class OrgRepository(Repository):
    _SELECT_ONE = """
        SELECT id, code, name, code_word, parent_id, created_at FROM org WHERE id=?; """
    _SELECT_BY_CODE = """
           SELECT id, code, name, code_word, parent_id, created_at FROM org WHERE code=?; """
    _SELECT_LEVEL_CHILD = """ S
        ELECT id, code, name, code_word, parent_id, created_at FROM org WHERE parent_id=?; """
    _SELECT_FIRST_LEVEL = """
        SELECT id, code, name, code_word, parent_id, created_at 
        FROM org 
        WHERE parent_id is NULL and closed_at is NULL ; """
    _SELECT_TREE = """
        SELECT id, code, name, code_word, parent_id, created_at 
        FROM org 
        WHERE parent_id = ? and closed_at is NULL ; """
    _SELECT = """
            SELECT id, code, name, code_word, parent_id, created_at 
            FROM org 
            WHERE closed_at is NULL ; """
    _SELECT_PARENTS = """
        SELECT parent_id FROM tree_path WHERE child_id = ? ;
    """
    _INSERT = "INSERT INTO org (code, name, code_word, parent_id, created_at, closed_at) VALUES(?, ?, ?, ?, ?, ?); "
    _INSERT_TREE_PATH = "INSERT INTO tree_path (parent_id, child_id) VALUES(?, ?) ; "
    _DELETE = "DELETE FROM org WHERE id=?; "

    def select_one(self, rid: int) -> Optional[Org]:
        query = QSqlQuery()
        query.prepare(self._SELECT_ONE)
        query.addBindValue(rid)
        query.exec()
        if query.first():
            return Org(query.value("id"), query.value("code"), query.value("name"),
                       query.value("code_word"), query.value("parent-id"), query.value("created_at"))
        else:
            return None

    def select_by_code(self, code: str) -> Optional[Org]:
        query = QSqlQuery()
        query.prepare(self._SELECT_BY_CODE)
        query.addBindValue(code)
        query.exec()
        if query.first():
            return Org(query.value("id"), query.value("code"), query.value("name"),
                       query.value("code_word"), query.value("parent_id"), query.value("created_at"))
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
            params["parent_id"] = org.id
            org.child = self.select(params)
        return orgs

    def select_child(self, parent_id: int) -> List[Org]:
        query = QSqlQuery()
        query.prepare(self._SELECT_LEVEL_CHILD)
        query.addBindValue(parent_id)
        query.exec()
        return self.__extract_data(query)

    def __extract_data(self, query: QSqlQuery) -> List[Org]:
        orgs = list()
        while query.next():
            orgs.append(Org(query.value("id"), query.value("code"), query.value("name"),
                            query.value("code_word"), query.value("parent_id"), query.value("created_at")))
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

    def insert(self, entities: List[Org]) -> int:
        query = QSqlQuery()
        query.prepare(self._INSERT)
        rid = 0
        for org in entities:
            print(org.row())
            query.addBindValue(org.code)
            query.addBindValue(org.name.upper())
            query.addBindValue(org.code_word)
            query.addBindValue(org.parent_id)
            query.addBindValue(org.created_at)
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


