from PyQt6.QtSql import QSqlQuery
from typing import Optional, List
from repositories.repository import Repository
from model_data.face import Face
from datetime import date
from settings import birthday_format


class FaceRepository(Repository):
    _SELECT = "SELECT id, snils, birthday FROM face ; "
    _INSERT = """
        INSERT INTO face (snils, birthday) 
        SELECT snils, birthday 
        FROM tmp_face
        WHERE snils not in ( SELECT snils FROM face) ; 
    """
    _INSERT_TMP = "INSERT INTO tmp_face (snils, birthday) VALUES (?, ?) ; "
    _DELETE_TMP = "DELETE FROM tmp_face ; "

    def __extract_data(self, query: QSqlQuery) -> List[Face]:
        faces = list()
        while query.next():
            faces.append(Face(query.value("id"), query.value("snils"), query.value("birthday")))
        return faces

    def select(self, params: dict = None) -> List[Face]:
        query = QSqlQuery()
        query.prepare(self._SELECT)
        query.exec()
        faces = self.__extract_data(query)
        return faces

    def __insert_tmp(self, faces: List[Face]) -> bool:
        query = QSqlQuery()
        query.prepare(self._INSERT_TMP)
        list_snils = [face.snils for face in faces]
        list_birthday = [face.birthday for face in faces]
        query.addBindValue(list_snils)
        query.addBindValue(list_birthday)
        if query.execBatch(QSqlQuery.BatchExecutionMode.ValuesAsRows):
            return True
        else:
            print("Insert into tmp error: {0}".format(query.lastError().text()))
            return False

    def insert(self, faces: List[Face]) -> int:
        if not self.__insert_tmp(faces):
            return 0
        query = QSqlQuery(self._INSERT)
        if query.exec():
            self.delete()
            return query.lastInsertId()
        else:
            print("Insert into face error: {0}".format(query.lastError().text()))
            return 0

    def select_one(self, rid: int) -> Face:
        pass

    def delete(self, params: dict = None) -> None:
        query = QSqlQuery(self._DELETE_TMP)
        query.exec()






