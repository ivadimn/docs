from pandas.core.frame import DataFrame, Series
from repositories.pos_repository import PosRepository


class LoadPositions:
    _COLUMN = "Полное наименование ШД"

    def __init__(self, data_frame: DataFrame):
        self.__data = None
        self.__data_frame = data_frame
        self.__load_positions()

    def __load_positions(self):
        data: Series = self.__data_frame[self._COLUMN]
        self.__data = [elem for elem in data.unique()]

    def update_db_data(self):
        rep = PosRepository()
        rep.load_from_list(self.__data)

