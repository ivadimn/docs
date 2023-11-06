import sqlite3 as sql3
from settings import db_params


# class Connection:
#     #_instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls,  "instance"):
#             print("Create instance")
#             cls.instance = super().__new__(cls, *args, **kwargs)
#         return cls.instance
#
#     def __init__(self):
#         # self.connection = QSqlDatabase.addDatabase("QSQLITE")
#         # self.connection.setDatabaseName(db_params["dbname"])
#         # ok = self.connection.open()
#         print("Into init")
#         if not hasattr(self, "connection"):
#             self.connection = sql3.connect(db_params["dbname"])
#             print("Create connection")
#             if self.connection:
#                 print("Connection successed!")
#             else:
#                 print("Connection failed!")
#
#     def __del__(self):
#         print("Удаляем...")
#         if self.connection:
#             self.connection.close()
#             print("Соединение закрыто.")


class Connection:

    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = sql3.connect(db_params["dbname"])
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

