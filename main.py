from decimal import Decimal
from uuid import uuid4

from controllers.AccountController import AccountController
from db.account_repository import AccountRepository
from middleware.response import error, success

repository = AccountRepository()
account_controller = AccountController()


def main():
    while option := input(
        "Choose an option (1: Create account, 2: Deposit, 3: Withdraw, "
        "4: Transfer, 5: Balance status, 6: Account details, exit: Quit): "
    ):
        match option:
            case "1":
                id_account = str(uuid4())
                owner = input("Enter the account owner's name: ")
                result = account_controller.create_account(
                    repository=repository,
                    id_account=id_account,
                    owner=owner,
                    balance=Decimal("0.00"),
                )
                if result:
                    print(success(
                        message=f"Account created successfully. Account ID: {id_account}",
                        status_code=201,
                    ))
                else:
                    print(error(message="Could not create the account.", status_code=400))
            case "2":
                id_account = input("Enter the account ID: ")
                amount = Decimal(input("Enter the deposit amount: "))
                result = account_controller.deposit(repository, id_account, amount)
                if result:
                    print(success(
                        message=f"Deposit completed for account {id_account}.",
                        status_code=200,
                    ))
                else:
                    print(error(message="Could not complete the deposit.", status_code=400))
            case "3":
                id_account = input("Enter the account ID: ")
                amount = Decimal(input("Enter the withdrawal amount: "))
                result = account_controller.withdraw(repository, id_account, amount)
                if result:
                    print(success(
                        message=f"Withdrawal completed for account {id_account}.",
                        status_code=200,
                    ))
                else:
                    print(error(message="Could not complete the withdrawal.", status_code=400))
            case "4":
                source_account_id = input("Enter the source account ID: ")
                target_account_id = input("Enter the target account ID: ")
                amount = Decimal(input("Enter the transfer amount: "))
                result = account_controller.transfer(
                    repository,
                    source_account_id,
                    target_account_id,
                    amount,
                )
                if result:
                    print(success(
                        message=(
                            f"Transfer completed from account {source_account_id} "
                            f"to account {target_account_id}."
                        ),
                        status_code=200,
                    ))
                else:
                    print(error(message="Could not complete the transfer.", status_code=400))
            case "5":
                id_account = input("Enter the account ID: ")
                result = account_controller.balance_status(repository, id_account)
                if result:
                    print(success(message=f"Balance status: {result}.", status_code=200))
                else:
                    print(error(message="Could not get the balance status.", status_code=400))
            case "6":
                id_account = input("Enter the account ID: ")
                result = account_controller.get_account_details(repository, id_account)
                if result:
                    print(success(message=result, status_code=200))
                else:
                    print(error(message="Could not get the account details.", status_code=400))
            case "exit":
                print("Exiting the program.")
                break


if __name__ == "__main__":
    main()