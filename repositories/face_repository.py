from PyQt6.QtSql import QSqlQuery
from typing import Optional, List
from repositories.repository import Repository
from model_data.face import Face
from datetime import date
from settings import birthday_format


class FaceRepository(Repository):
    _SELECT = "SELECT id, snils, birthday FROM face ; "
    _INSERT_LOADED = """
        INSERT INTO face (snils, birthday) 
        SELECT snils, birthday 
        FROM tmp_face
        WHERE snils not in ( SELECT snils FROM face) ; 
    """
    _INSERT_TMP = " INSERT INTO tmp_face (snils, tn, firstname, name, fathername) VALUES (?, ?, ?, ?, ?) ; "
    _INSERT_ONE = " INSERT INTO face (snils, birthday) VALUES (?, ?) ; "
    _DELETE_TMP = " DELETE FROM tmp_face ; "

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
        query.addBindValue([face.snils for face in faces])
        query.addBindValue([face.tn for face in faces])
        query.addBindValue([face.fio[0] for face in faces])
        query.addBindValue([face.fio[1] for face in faces])
        query.addBindValue([face.fio[2] for face in faces])
        if query.execBatch(QSqlQuery.BatchExecutionMode.ValuesAsRows):
            return True
        else:
            print("Insert into tmp error: {0}".format(query.lastError().text()))
            return False

    def insert(self, faces: List[Face], orgs: List[int] = None) -> int:
        if not self.__insert_tmp(faces):
            return 0
        query = QSqlQuery()
        query.prepare(self._INSERT_ONE)
        if not query.exec():
            print("Insert into face error: {0}".format(query.lastError().text()))
            return 0
        if self.__insert_tmp(faces):
            pass
            #insert pd

    def select_one(self, rid: int) -> Face:
        pass

    def delete(self, params: dict = None) -> None:
        query = QSqlQuery(self._DELETE_TMP)
        query.exec()

    def load_from_list(self, data: List[Face]):
        query = QSqlQuery()
        query.prepare(self._INSERT_TMP)
        query.addBindValue([f.snils for f in data])
        query.addBindValue([f.tn for f in data])
        query.addBindValue([f.fio[0] for f in data])
        query.addBindValue([f.fio[1] for f in data])
        query.addBindValue([f.fio[2] for f in data])
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





