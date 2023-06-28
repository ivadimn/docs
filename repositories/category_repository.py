from PyQt6.QtSql import QSqlQuery
from typing import List
from repositories.repository import Repository
from model_data.category import Category


class CategoryRepository(Repository):
    _INSERT = "INSERT INTO category (code, name) VALUES(?, ?);"

    def insert(self, entities: List[Category]) -> None:
        query = QSqlQuery()
        query.prepare(self._INSERT)
        for cat in entities:
            query.addBindValue(cat.code)
            query.addBindValue(cat.name)
            query.exec()

    def select(self, params: dict) -> List[Category]:
        return []

    def delete(self, params: dict) -> None:
        pass
