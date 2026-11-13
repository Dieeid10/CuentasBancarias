import sqlite3


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def initialize_connection(self, database_file):
        if self._connection is None:
            self._connection = sqlite3.connect(database_file)
            print("Database connection opened.")
        else:
            print("An active database connection is being reused.")
        return self._connection

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            print("Database connection closed.")