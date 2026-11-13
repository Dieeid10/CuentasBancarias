from db.use_cases import useCases
from functools import wraps
from config.config import config_db
from middleware.handler import route_handler

# Decorador que compreuba si hay conexión a la base de datos antes de ejecutar la función decorada
@route_handler
def comprobate_connection(func):
    @wraps(func)
    def wrapper(self, connection, *args, **kwargs):
        try:
            connection.ensure_connection()
            return func(self, connection, *args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return None
            raise
        finally:
            connection.close_connection()

    return wrapper
    
class CuentaControllers():
    TABLA = config_db["TABLE"]
    
    @comprobate_connection
    def create_account(self, connection, id_account: str, titular: str, saldo: float=0):
        result = connection.insert(self.TABLA, {"id": id_account, "titular": titular, "saldo": saldo})
        print(result)
        return result

    # función para depositar dinero en la cuenta. El monto a depositar debe ser positivo. Actualiza saldo.
    @comprobate_connection
    def deposit(self, connection, id_account: str, amount: float):
        if amount <= 0:
            raise ValueError("El monto a depositar debe ser positivo.")

        account = connection.select(self.TABLA, id_account)
        
        if not account:
            raise ValueError("Cuenta no encontrada.")

        previous_balance = float(account[2])
        new_amount = previous_balance + amount
        result = connection.update(self.TABLA, id_account, {"saldo": new_amount})
        return result

    # función para extraer dinero de la cuenta bancaria. El saldo de la cuenta puede quedar en negativo.
    @comprobate_connection
    def extraer(self, connection, id_account: str, amount: float):
        if amount <= 0:
            raise ValueError("El monto a extraer debe ser positivo.")

        account = connection.select(self.TABLA, id_account)
            
        if not account:
            raise ValueError("Cuenta no encontrada.")

        self.saldo = float(account[2])
        self.saldo -= amount
        return connection.update(self.TABLA, id_account, {"saldo": self.saldo - amount})

    @comprobate_connection
    def transferencia(self, connection, id_account_source: str, id_account_target: str, amount: float):
        if amount <= 0:
            raise ValueError("El monto a transferir debe ser positivo.")

        account_source = connection.select(self.TABLA, id_account_source)
        account_target = connection.select(self.TABLA, id_account_target)
        if not account_source or not account_target:
            raise ValueError("Cuenta origen o destino no encontrada.")

        saldo_source = float(account_source[2])
        saldo_target = float(account_target[2])
        
        if saldo_source < amount:
            raise ValueError("No se puede efectuar la transacción")
            
        saldo_source -= amount
        saldo_target += amount
        connection.update(self.TABLA, id_account_source, {"saldo": saldo_source})
        connection.update(self.TABLA, id_account_target, {"saldo": saldo_target})

        return True

    # función para obtener estado de la cuenta bancaria. Informará "Su saldo es acreedor" si el saldo de la cuenta es mayor o igual a cero y "Su saldo es deudor" en caso contrario 
    @comprobate_connection
    def estadoCuenta(self, connection, id_account: str):
        account = connection.select(self.TABLA, id_account)
        if not account:
            raise ValueError("Cuenta no encontrada.")
        saldo = float(account[2])
    
        return "acreedor" if saldo >= 0 else "deudor"

    # función para imprimir los datos del cliente
    @comprobate_connection
    def imprimirDatos(self, connection, id_account: str):
        account = connection.select(self.TABLA, id_account)

        if not account:
            raise ValueError("Cuenta no encontrada.")

        return f"titular: {account[1]}, saldo: ${account[2]}"
