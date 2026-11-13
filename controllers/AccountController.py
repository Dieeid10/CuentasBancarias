from functools import wraps
from decimal import Decimal

from middleware.handler import route_handler
from models.Account import Account


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
    @check_database_connection
    def create_account(
        self,
        repository,
        id_account: str,
        owner: str,
        balance: Decimal = Decimal("0.00"),
        account_type: str | None = None
    ):
        account = Account(
            id_account=id_account,
            owner=owner,
            balance=balance,
            account_type=account_type,
        )
        return repository.add_account(account)

    @check_database_connection
    def deposit(self, repository, id_account: str, amount: Decimal):
        account = repository.get_by_id(id_account)
        if account is None:
            raise ValueError("Account not found.")

        account.deposit(amount)
        repository.save_account(account)
        return True

    @check_database_connection
    def withdraw(self, repository, id_account: str, amount: Decimal):
        account = repository.get_by_id(id_account)
        if account is None:
            raise ValueError("Account not found.")

        account.withdraw(amount)
        repository.save_account(account)
        return True

    @check_database_connection
    def transfer(self, repository, source_account_id: str, target_account_id: str, amount: Decimal):
        source_account = repository.get_by_id(source_account_id)
        target_account = repository.get_by_id(target_account_id)
        if source_account is None or target_account is None:
            raise ValueError("Source or target account not found.")

        source_account.transfer_to(target_account, amount)
        repository.save_accounts((source_account, target_account))
        return True

    @check_database_connection
    def balance_status(self, repository, id_account: str):
        account = repository.get_by_id(id_account)
        if account is None:
            raise ValueError("Account not found.")

        return account.balance_status()

    @check_database_connection
    def get_account_details(self, repository, id_account: str):
        account = repository.get_by_id(id_account)
        if account is None:
            raise ValueError("Account not found.")

        return f"Owner: {account.owner}, balance: ${account.balance}"