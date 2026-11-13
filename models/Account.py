from decimal import Decimal

class Account:
    def __init__(
        self,
        id_account: str,
        balance: Decimal,
        account_type: str | None,
        owner: str,
    ):
        self.id_account = id_account
        self.balance = balance
        self.account_type = account_type
        self.owner = owner

    def deposit(self, amount: Decimal) -> None:
        if amount <= Decimal("0"):
            raise ValueError("The deposit amount must be positive.")

        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount <= Decimal("0"):
            raise ValueError("The withdrawal amount must be positive.")

        # Withdrawals may leave the account balance negative.
        self.balance -= amount

    def transfer_to(self, other_account: "Account", amount: Decimal) -> None:
        if amount <= Decimal("0"):
            raise ValueError("The transfer amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")

        self.balance -= amount
        other_account.balance += amount

    def balance_status(self) -> str:
        return "creditor" if self.balance >= Decimal("0") else "debtor"