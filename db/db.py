import sqlite3 as sql3
from db.connection import Connection
from settings import db_params


class Db:
    _connection = None

    @classmethod
    def init_connection(cls):
        cls._connection = sql3.connect(db_params["dbname"])

    @classmethod
    def close_connection(cls):
        if cls._connection:
            cls._connection.close()

    @classmethod
    def select(cls, sql: str, params: tuple = None) -> sql3.Cursor:
        cursor = cls._connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor

    @classmethod
    def insert(cls, sql: str, params: tuple):
        cursor = cls._connection.cursor()
        if len(params) > 0:
            cursor.execute(sql, params)
            cls._connection.commit()
        else:
            cursor.execute(sql)
            cls._connection.commit()
        return cursor.lastrowid

    @classmethod
    def update(cls, sql: str, params: list) -> int:
        cursor = cls._connection.cursor()
        if len(params) > 0:
            cursor.executemany(sql, params)
            cls._connection.commit()
        else:
            cursor.execute(sql)
            cls._connection.commit()
        return cursor.lastrowid


class Param:
    def __init__(self, table: str, filed: str, op: str):
        self.table = table
        self.field = filed
        self.op = op

    def __str__(self):
        return "{0}.{1}{2}?".format(self.table, self.field, self.op)
