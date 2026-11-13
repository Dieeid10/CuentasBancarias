from db.conecction import Connection
    
class useCases(Connection):
    def __init__(self):
        self.connection = self.init_connection("cuentas.db")
        self.create_table()

    def ensure_connection(self):
        if self._connection is None:
            self.connection = self.init_connection("cuentas.db")

    # --- CREATE TABLE IF NOT EXISTS ---
    def create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS cuentas (
                id TEXT PRIMARY KEY,
                titular TEXT NOT NULL,
                saldo REAL NOT NULL DEFAULT 0
            )
        """)
        self.connection.commit()

    # --- INSERT ---
    def insert(self, table: str, data: dict):
        """
        table: nombre de la tabla
        data: dict con {columna: valor}, ej: {"titular": "Juan", "saldo": 1000}
        """
        colum = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())

        sql = f"INSERT INTO {table} ({colum}) VALUES ({placeholders})"
        cursor = self.connection.execute(sql, values)
        self.connection.commit()
        return cursor.lastrowid

    # --- SELECT (por id) ---
    def select(self, table: str, id_value, id_field: str = "id"):
        sql = f"SELECT * FROM {table} WHERE {id_field} = ?"
        cursor = self.connection.execute(sql, (id_value,))
        return cursor.fetchone()

    # --- SELECT (todos, con filtro opcional) ---
    def select_all(self, table: str, condition: str = None, parameters: tuple = ()):
        """
        condition (opcional): ej. "saldo > ?"
        parameters: values para la condición, ej. (0,)
        """
        sql = f"SELECT * FROM {table}"
        if condition:
            sql += f" WHERE {condition}"
        cursor = self.connection.execute(sql, parameters)
        return cursor.fetchall()

    # --- UPDATE ---
    def update(self, table: str, id_value, data: dict, id_field: str = "id"):
        """
        data: dict con {columna: nuevo_valor}
        """
        set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
        values = tuple(data.values()) + (id_value,)

        sql = f"UPDATE {table} SET {set_clause} WHERE {id_field} = ?"
        self.connection.execute(sql, values)
        self.connection.commit()
        return self.connection.total_changes

    # --- DELETE ---
    def delete(self, table: str, id_value, id_field: str = "id"):
        sql = f"DELETE FROM {table} WHERE {id_field} = ?"
        self.connection.execute(sql, (id_value,))
        self.connection.commit()

    # --- CLOSE CONNECTION ---
    def close_connection(self):
        super().close_connection()
        self.connection = None