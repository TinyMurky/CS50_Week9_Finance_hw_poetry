import sqlite3
from typing import Any, Union

from src.libs.common import get_abs_path, hash_password, get_offset, get_timestamp_now
from src.libs.errors.error_classes import (
    InvalidDevInputArgument,
    NoSuchUser,
    NotEnoughMoney,
    NotEnoughShare,
)


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
        get unique users from users table
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
        """
        Save quote history from yahoo
        """

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

    def get_user_single_stock_shares(self, user_id: int, symbol: str) -> int:
        """
        GET how many stock an user have
        """
        assert self._connect is not None, "Connect is None"
        assert self._cursor is not None, "Cursor is None"

        symbol = symbol.upper()

        query = """
        SELECT SUM(share) as total_shares
        FROM transactions
        WHERE user_id = ? AND symbol = ?;
        """

        self._cursor.execute(query, (user_id, symbol))
        result = self._cursor.fetchone()
        total_shares = (
            result["total_shares"] if (result and result["total_shares"]) else 0
        )

        return total_shares

    # Buy and sell logic
    def buy(self, user_id: int, symbol: str, price: float, share: int):
        """
        Buy Stock by transaction

        :param: price is 1 stock price
        :param: share need to be negative
        """
        assert self._connect is not None, "Connect is None"
        assert self._cursor is not None, "Cursor is None"

        print("user_id", user_id)
        user = self.find_unique_user(user_id)
        symbol = symbol.upper()
        share = abs(share)
        price = abs(price)

        if not user:
            raise NoSuchUser

        total_price = abs(price * share)

        if user["cash"] < total_price:
            raise NotEnoughMoney

        update_cash_query = """
        UPDATE users
        SET cash = cash - (? * ?)
        WHERE id = ?;
        """

        insert_buy_transaction_query = """
        INSERT INTO transactions (symbol, share, price, timestamp, user_id)
        VALUES
        (?, ?, ?, ?, ?);
        """

        try:
            # start transaction
            self._connect.execute("BEGIN TRANSACTION")
            now = get_timestamp_now()
            self._cursor.execute(update_cash_query, (price, share, user_id))
            self._cursor.execute(
                insert_buy_transaction_query, (symbol, share, price, now, user_id)
            )
            self._connect.commit()
            print("Execute!")
        except sqlite3.Error as e:
            # 如果发生错误，回滚事务
            print(f"An error occurred in buy: {e}")
            self._connect.rollback()

        return self._cursor.lastrowid

    def sell(self, user_id: int, symbol: str, price: float, share: int):
        """
        Sell stock if have enough share
        """
        assert self._connect is not None, "Connect is None"
        assert self._cursor is not None, "Cursor is None"

        user_stock = self.get_user_single_stock_shares(user_id=user_id, symbol=symbol)
        share = -1 * abs(share)
        price = abs(price)
        symbol = symbol.upper()

        if user_stock < share:
            raise NotEnoughShare

        update_cash_query = """
        UPDATE users
        SET cash = cash - (? * ?)
        WHERE id = ?;
        """

        insert_buy_transaction_query = """
        INSERT INTO transactions (symbol, share, price, timestamp, user_id)
        VALUES
        (?, ?, ?, ?, ?);
        """
        try:
            # start transaction
            self._connect.execute("BEGIN TRANSACTION")
            now = get_timestamp_now()
            self._cursor.execute(update_cash_query, (price, share, user_id))
            self._cursor.execute(
                insert_buy_transaction_query, (symbol, share, price, now, user_id)
            )
            self._connect.commit()
        except sqlite3.Error as e:
            # 如果发生错误，回滚事务
            print(f"An error occurred in buy: {e}")
            self._connect.rollback()
        return self._cursor.lastrowid

    def get_portfolio(self, user_id: int):
        """
        Return be like

        1. symbol
        2. total_price
        3. avg_price
        4. total_share

        You need to get total cash and total price + total cash
        """
        assert self._cursor is not None, "Cursor is None"

        query = """
        SELECT
            symbol,
            sum(price * share) as total_price,
            CASE
                WHEN sum(share) != 0 THEN ABS(ROUND(sum(price * share) / sum(share), 2))
                ELSE 0
            END as avg_price,
            sum(share) as total_share
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING sum(share) != 0
        ORDER BY total_share DESC;
        """

        self._cursor.execute(query, (user_id,))

        portfolio = self._cursor.fetchall()

        return portfolio

    def find_many_history(self, user_id: int, page: int, limit: int):
        """
        get history of transaction
        """
        assert self._cursor is not None, "Cursor is None"

        offset = get_offset(page=page, limit=limit)

        query = """
        SELECT id, symbol, ABS(share) as abs_share, price, timestamp,
            CASE
                WHEN share > 0 THEN 'Buy'
                ELSE 'Sell'
            END as action
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?;
        """

        self._cursor.execute(query, (user_id, limit, offset))

        history = self._cursor.fetchall()

        return history


sql_client = SQL()
