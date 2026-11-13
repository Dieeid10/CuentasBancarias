import sqlite3

class Connection():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def init_connection(self, db_file):
        if self._connection is None:
            self._connection = sqlite3.connect(db_file)
            print("Conexión iniciada.")
        else:
            print("Ya existe una conexión activa, se reutiliza.")
        return self._connection

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            print("Conexión cerrada correctamente.")