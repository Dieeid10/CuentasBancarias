# MVC Refactoring Plan

This document describes the proposed changes. No source code or database was changed when the plan was first created.

## Current State

- `main.py` contains the console interface, coordinates operations, and formats responses.
- `controllers/AccountController.py` contains banking rules and database queries.
- `models/Account.py` represents an account and contains its domain operations.
- `db/account_repository.py` provides generic SQLite CRUD operations and migrates legacy `cuentas` data into `accounts`.
- The old `cuentas` table is retained in `accounts.db` as a data-preserving migration source.
- Withdrawals currently subtract the amount twice in the controller. Transfers commit account updates separately, so a failure between writes can leave inconsistent balances.
- Error handling is split across decorators; the controller decorator catches exceptions and returns `None`, making them difficult for higher layers to handle.

## Target Architecture

Flow: **View → Controller → Use case → Model and repository → SQLite**.

- **Console view:** collects input and displays results; it contains no banking rules or SQL.
- **Controller:** receives view actions, calls the relevant use case, and adapts results for the view.
- **Use cases:** coordinate complete operations, load entities, and save changes. Transfers are coordinated here so they can be atomic.
- **`Account` model:** represents an account and enforces its domain rules. It does not know about SQLite, the console, or controllers.
- **Account repository:** owns SQL queries, converts SQLite rows into `Account` objects, and persists changes.
- **Database connection:** manages connections and transactions; it contains no business rules.

## Proposed Changes

### 1. Complete the Account Schema

Ensure new tables include `account_type` and migrate existing tables after checking their columns. The migration must be idempotent and preserve saved accounts.

Existing accounts have no known account type: do not invent one. Keep it `NULL` temporarily or define a valid mapping before migration. Agree on accepted account types before making the field required.

### 2. Implement the `Account` Model

Define `id_account`, `owner`, `balance`, and `account_type` in `models/Account.py`, along with domain operations such as deposit, withdraw, transfer, and balance-status checks. These operations validate amounts and modify the object without printing messages or writing to the database.

Preserve the current rules: withdrawals may leave a negative balance, while transfers cannot exceed the available balance. Ensure a withdrawal deducts the amount only once. Decide whether account type is required and which values it accepts.

### 3. Separate Persistence and Connections

Use a dedicated account repository with account-specific operations to get by ID, create, update, list, and delete. Convert rows into `Account` objects using named columns rather than positional indexes such as `account[2]`.

Keep connection and transaction management in `db/connection.py`. Review the current lifecycle, which opens the database when constructing the repository and closes it from the controller decorator. Transfers should use one transaction, committing both updates together and rolling back on errors.

### 4. Add a Use-Case Layer

Add an independent `use_cases/` layer for creating accounts, depositing, withdrawing, transferring, checking balance status, and retrieving account details. These use cases load accounts through the repository, invoke the model, and persist the results.

Transfers must validate both accounts and the amount, apply model rules, and save both balances atomically.

### 5. Keep the Controller Thin

Keep SQL, balance calculations, and banking validation out of `controllers/AccountController.py`. Each controller method should delegate to a use case and return a defined result or error.

Consolidate error handling into one layer. Remove exception handling that prints an error and returns `None`, and correct or remove the current decorator to avoid inconsistent responses and hidden errors.

### 6. Separate the View and Dependency Setup

Move input collection and response presentation out of `main.py` into a console view, such as `views/ConsoleView.py`. Keep `main.py` as the entry point that creates the connection, repository, use cases, controller, and view, then starts the application.

Ask for an account type once the allowed values have been agreed upon. Keep messages and response codes out of the model and repository.

### 7. Add Tests

- **Model:** valid deposits and withdrawals, non-positive amounts, negative balances under the current rule, creditor/debtor status, and transfers with sufficient or insufficient funds.
- **Schema and migration:** a new database and an existing database without `account_type`; verify repeatability and row preservation.
- **Repository:** conversion between rows and `Account`, and CRUD operations using a temporary database.
- **Use cases:** successful operations, missing accounts, and transfer rollback if one write fails.
- **Console integration:** create an account and perform an operation without coupling tests to the real `accounts.db` database.

## Completion Criteria

- The model is the source of balance rules and has no dependency on SQLite or the console.
- The repository is the only module that contains account SQL.
- A transfer persists both changes in one transaction.
- Existing data is migrated without loss or invented account types.
- The view, controller, and use cases have distinct responsibilities.
- Tests cover model rules, migrations, and transactions.