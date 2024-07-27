import sqlite3
from typing import Any

from src.libs.common import get_abs_path


class SQL:
    """
    Singleton to access database by sqlite
    """

    _db_path = get_abs_path("sql/finance.db")
    _instance = None
    _connect = None
    _cursor = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SQL, cls).__new__(cls, *args, **kwargs)
            cls._connect = sqlite3.connect(cls._db_path, check_same_thread=False)
            cls._connect.row_factory = SQL.dict_factory
            cls._cursor = cls._connect.cursor()
        return cls._instance

    @staticmethod
    def dict_factory(cursor: sqlite3.Cursor, row):
        """
        auto mapping sql data to dictionary
        """
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    @staticmethod
    def migrate():
        """
        migrate database
        """
        if SQL._connect is None or SQL._cursor is None:
            SQL._connect = sqlite3.connect(SQL._db_path, check_same_thread=False)
            SQL._cursor = SQL._connect.cursor()

        sql_schema_path = get_abs_path("sql/schema.sql")

        with open(sql_schema_path, "r", encoding="utf-8") as f:
            sql_query = f.read()

        SQL._cursor.executescript(sql_query)
        SQL._connect.commit()

    def findUniqueUser(self, username: str) -> dict[str, Any]:
        """
        get unique user from users table
        """
        assert self._cursor is not None
        assert isinstance(username, str)
        query = """
        SELECT * FROM users
        WHERE username = ?
        LIMIT 1;
        """

        self._cursor.execute(query, (username,))
        user = self._cursor.fetchone()
        return user
