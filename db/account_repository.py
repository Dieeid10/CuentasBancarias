from decimal import Decimal

from db.connection import DatabaseConnection
from models.Account import Account


class AccountRepository(DatabaseConnection):
    def __init__(self):
        self.connection = self.initialize_connection("accounts.db")
        self.create_table()

    def ensure_connection(self):
        if self._connection is None:
            self.connection = self.initialize_connection("accounts.db")

    def create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                owner TEXT NOT NULL,
                balance_cents INTEGER NOT NULL DEFAULT 0,
                account_type TEXT NULL
            )
        """)

        legacy_columns = {
            row[1]
            for row in self.connection.execute("PRAGMA table_info(cuentas)").fetchall()
        }
        if {"id", "titular", "saldo"}.issubset(legacy_columns):
            owner_expression = "COALESCE(owner, titular)" if "owner" in legacy_columns else "titular"
            balance_expression = "balance" if "balance" in legacy_columns else "saldo"
            account_type_expression = "account_type" if "account_type" in legacy_columns else "NULL"
            self.connection.execute(f"""
                INSERT OR IGNORE INTO accounts (id, owner, balance, account_type)
                SELECT id, {owner_expression}, {balance_expression}, {account_type_expression}
                FROM cuentas
            """)

        self.connection.commit()

    def get_by_id(self, id_account: str) -> Account | None:
        row = self.connection.execute(
            """
            SELECT id, owner, balance, account_type
            FROM accounts
            WHERE id = ?
            """,
            (id_account,)
        ).fetchone()
        if row is None:
            return None

        return Account(
            id_account=row[0],
            owner=row[1],
            balance=Decimal(str(row[2])),
            account_type=row[3],
        )

    def add_account(self, account: Account):
        return self.insert(
            "accounts",
            {
                "id": account.id_account,
                "owner": account.owner,
                "balance": account.balance,
                "account_type": account.account_type,
            }
        )

    def save_account(self, account: Account):
        return self.update(
            "accounts",
            account.id_account,
            {"balance": account.balance}
        )

    def save_accounts(self, accounts: tuple[Account, ...]):
        with self.connection:
            for account in accounts:
                self.connection.execute(
                    "UPDATE accounts SET balance = ? WHERE id = ?",
                    (str(account.balance), account.id_account)
                )
        return True

    def insert(self, table_name: str, data: dict):
        column_names = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(
            str(value) if isinstance(value, Decimal) else value
            for value in data.values()
        )
        sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        cursor = self.connection.execute(sql, values)
        self.connection.commit()
        return cursor.lastrowid

    def select(self, table_name: str, id_value, id_field: str = "id"):
        sql = f"SELECT * FROM {table_name} WHERE {id_field} = ?"
        cursor = self.connection.execute(sql, (id_value,))
        return cursor.fetchone()

    def select_all(self, table_name: str, condition: str = None, parameters: tuple = ()):
        sql = f"SELECT * FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        cursor = self.connection.execute(sql, parameters)
        return cursor.fetchall()

    def update(self, table_name: str, id_value, data: dict, id_field: str = "id"):
        set_clause = ", ".join([f"{column} = ?" for column in data.keys()])
        values = tuple(
            str(value) if isinstance(value, Decimal) else value
            for value in data.values()
        ) + (id_value,)
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {id_field} = ?"
        self.connection.execute(sql, values)
        self.connection.commit()
        return self.connection.total_changes

    def delete(self, table_name: str, id_value, id_field: str = "id"):
        sql = f"DELETE FROM {table_name} WHERE {id_field} = ?"
        self.connection.execute(sql, (id_value,))
        self.connection.commit()

    def close_connection(self):
        super().close_connection()
        self.connection = None