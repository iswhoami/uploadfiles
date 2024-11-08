import sqlite3

from config import DB_PATH
from errors import DBQueryException
from logger import logger


class Connection:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        self._conn = sqlite3.connect(DB_PATH)

    def execute(self, sql, *args):
        try:
            self._cursor = self._conn.cursor()
            self._cursor.execute(sql, args)
            self._conn.commit()
            rows = self._cursor.fetchall()
            column_names = [description[0] for description in self._cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
            return result
        except sqlite3.Error as e:
            logger.error('Run SQL-query, error: {}'.format(e))
            raise DBQueryException(str(e))
        finally:
            self._cursor.close()

    def execute_void(self, sql, *args):
        try:
            self._cursor = self._conn.cursor()
            self._cursor.execute(sql, args)
            self._conn.commit()
        except sqlite3.Error as e:
            logger.error('Run SQL-query, error: {}'.format(e))
            raise DBQueryException(str(e))
        finally:
            self._cursor.close()

    def close(self):
        if hasattr(self, '_conn'):
            self._conn.close()
            del self._conn
            del self._cursor

    def __del__(self):
        self.close()
