from PyQt6.QtSql import QSqlQuery
from typing import List
from repositories.repository import Repository
from model_data.pd import Pd


class PdRepository(Repository):
    _INSERT = "INSERT INTO pd (name, comment) VALUES(?, ?);"

    def insert(self, entities: List[Pd]) -> None:
        query = QSqlQuery()
        query.prepare(self._INSERT)
        for pd in entities:
            query.addBindValue(pd.name)
            query.addBindValue(pd.comment)
            query.exec()

    def select(self, params: dict) -> List[Pd]:
        return []

    def delete(self, params: dict) -> None:
        pass



