from functools import wraps

from config.config import DATABASE_CONFIG
from middleware.handler import route_handler


@route_handler
def check_database_connection(func):
    @wraps(func)
    def wrapper(self, repository, *args, **kwargs):
        try:
            repository.ensure_connection()
            return func(self, repository, *args, **kwargs)
        except Exception as exception:
            print(f"Error: {exception}")
            return None
        finally:
            repository.close_connection()

    return wrapper


class AccountController:
    TABLE_NAME = DATABASE_CONFIG["TABLE_NAME"]

    @check_database_connection
    def create_account(
        self,
        repository,
        id_account: str,
        owner: str,
        balance: float = 0,
        account_type: str | None = None,
    ):
        return repository.insert(
            self.TABLE_NAME,
            {
                "id": id_account,
                "owner": owner,
                "balance": balance,
                "account_type": account_type,
            },
        )

    @check_database_connection
    def deposit(self, repository, id_account: str, amount: float):
        if amount <= 0:
            raise ValueError("The deposit amount must be positive.")

        account = repository.select(self.TABLE_NAME, id_account)
        if not account:
            raise ValueError("Account not found.")

        previous_balance = float(account[2])
        new_balance = previous_balance + amount
        return repository.update(
            self.TABLE_NAME,
            id_account,
            {"balance": new_balance},
        )

    @check_database_connection
    def withdraw(self, repository, id_account: str, amount: float):
        if amount <= 0:
            raise ValueError("The withdrawal amount must be positive.")

        account = repository.select(self.TABLE_NAME, id_account)
        if not account:
            raise ValueError("Account not found.")

        self.balance = float(account[2])
        self.balance -= amount
        return repository.update(
            self.TABLE_NAME,
            id_account,
            {"balance": self.balance - amount},
        )

    @check_database_connection
    def transfer(self, repository, source_account_id: str, target_account_id: str, amount: float):
        if amount <= 0:
            raise ValueError("The transfer amount must be positive.")

        source_account = repository.select(self.TABLE_NAME, source_account_id)
        target_account = repository.select(self.TABLE_NAME, target_account_id)
        if not source_account or not target_account:
            raise ValueError("Source or target account not found.")

        source_balance = float(source_account[2])
        target_balance = float(target_account[2])
        if source_balance < amount:
            raise ValueError("Insufficient funds for the transfer.")

        source_balance -= amount
        target_balance += amount
        repository.update(
            self.TABLE_NAME,
            source_account_id,
            {"balance": source_balance},
        )
        repository.update(
            self.TABLE_NAME,
            target_account_id,
            {"balance": target_balance},
        )
        return True

    @check_database_connection
    def balance_status(self, repository, id_account: str):
        account = repository.select(self.TABLE_NAME, id_account)
        if not account:
            raise ValueError("Account not found.")

        balance = float(account[2])
        return "creditor" if balance >= 0 else "debtor"

    @check_database_connection
    def get_account_details(self, repository, id_account: str):
        account = repository.select(self.TABLE_NAME, id_account)
        if not account:
            raise ValueError("Account not found.")

        return f"Owner: {account[1]}, balance: ${account[2]}"