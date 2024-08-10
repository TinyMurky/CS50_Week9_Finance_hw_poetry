import sqlite3
from typing import Any, Union

from src.libs.common import get_abs_path, hash_password, get_offset, get_timestamp_now
from src.libs.errors.error_classes import InvalidDevInputArgument


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

    def get_total_row_amount(self, table_name: str) -> int:
        """
        get amount of row from table
        """
        assert self._cursor is not None, "Cursor is None"

        query = f"SELECT COUNT(*) as `count` FROM {table_name}"

        rows_amount = 0

        try:
            self._cursor.execute(query)
            rows_amount = self._cursor.fetchone()["count"]
        except sqlite3.OperationalError as e:
            print(f"Error: {e}. Table '{table_name}' may not exist.")
            rows_amount = 0  # 如果表格不存在，可以返回 0 或其他適當的值

        return rows_amount

    def find_unique_user(self, identifier: Union[str, int]) -> dict[str, Any]:
        """
        get unique user from users table
        """
        assert self._cursor is not None
        if isinstance(identifier, str):
            query = """
            SELECT * FROM users
            WHERE username = ?
            LIMIT 1;
            """
        elif isinstance(identifier, int):
            query = """
            SELECT * FROM users
            WHERE id = ?
            LIMIT 1;
            """
        else:
            raise InvalidDevInputArgument

        self._cursor.execute(query, (identifier,))
        user = self._cursor.fetchone()
        return user

    def create_user(self, username: str, password: str):
        """
        create user
        """
        assert self._connect is not None
        assert self._cursor is not None

        if not isinstance(username, str) or not isinstance(password, str):
            raise InvalidDevInputArgument

        hashed_password = hash_password(password=password)
        query = """
        INSERT INTO users (username, hash)
        VALUES
        (?, ?)
        """

        self._cursor.execute(query, (username, hashed_password))
        self._connect.commit()

        return self._cursor.lastrowid

    # Below is Quote
    def find_many_quote(self, page: int, limit: int, user_id: int):
        """
        find many quote
        """
        assert self._cursor is not None, "Cursor is None"
        offset = get_offset(page=page, limit=limit)

        query = """
        SELECT * FROM quotes
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
        """

        self._cursor.execute(query, (user_id, limit, offset))

        rows = self._cursor.fetchall()
        return rows

    def create_quote(self, symbol: str, price: float, user_id: int):

        assert self._connect is not None, "Connect is None"
        assert self._cursor is not None, "Cursor is None"
        now = get_timestamp_now()

        query = """
        INSERT INTO quotes (symbol, price, user_id, timestamp)
        VALUES
        (?, ?, ?, ?)
        """

        self._cursor.execute(query, (symbol, price, user_id, now))
        self._connect.commit()

        return self._cursor.lastrowid


sql_client = SQL()
