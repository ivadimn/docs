from PyQt6.QtSql import QSqlQuery
from typing import List
from repositories.repository import Repository
from model_data.goal import Goal


class GoalRepository(Repository):
    _INSERT = "INSERT INTO goal (code, name) VALUES(?, ?);"

    def insert(self, entities: List[Goal]) -> None:
        query = QSqlQuery()
        query.prepare(self._INSERT)
        for cat in entities:
            query.addBindValue(cat.code)
            query.addBindValue(cat.name)
            query.exec()

    def select(self, params: dict) -> List[Goal]:
        return []

    def delete(self, params: dict) -> None:
        pass
