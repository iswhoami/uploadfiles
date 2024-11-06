import sqlite3

from config import DB_PATH


class Connection:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        self._conn = sqlite3.connect(DB_PATH)
        self._cursor = self._conn.cursor()

    def execute(self, sql, *args):
        try:
            self._cursor.execute(sql, args)
            self._conn.commit()
            rows = self._cursor.fetchall()
            column_names = [description[0] for description in self._cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
            return result
        except sqlite3.Error as e:
            print(e)

    def execute_void(self, sql, *args):
        try:
            self._cursor.execute(sql, args)
            self._conn.commit()
        except sqlite3.Error as e:
            print(e)

    def close(self):
        if hasattr(self, '_conn'):
            self._conn.close()
            del self._conn
            del self._cursor

    def __del__(self):
        self.close()
