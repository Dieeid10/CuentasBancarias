from controllers.CuentaControllers import CuentaControllers
from middleware.response import success, error
from db.use_cases import useCases
from uuid import uuid4

connection = useCases()
cuentaController = CuentaControllers()
    
def main():
    while option := input("Ingrese una opción (1: Crear cuenta, 2: Depositar, 3: Extraer, 4: Transferir, 5: Estado de cuenta, 6: Imprimir datos, exit: Salir): "):
        
        match option:
            case "1":
                id_account: str = str(uuid4())
                nombre = input("Ingrese el nombre del titular: ")
                
                result = cuentaController.create_account(connection=connection, id_account=id_account, titular=nombre, saldo=0)
                if result:
                    print(success(message = f"Cuenta creada con éxito. ID de la cuenta: {id_account}", status_code=201))
                else:
                    print(error(message="Error al crear la cuenta.", status_code=400))
            case "2":
                id_account = input("Ingrese el número de cuenta: ")
                amount = float(input("Ingrese el monto a depositar: "))
                result = cuentaController.deposit(connection=connection, id_account=id_account, amount=amount)
                if result:
                    print(success(message=f"Depósito realizado con éxito en la cuenta: {id_account}", status_code=200))
                else:
                    print(error(message="Error al realizar el depósito.", status_code=400))
            case "3":
                id_account = input("Ingrese el número de cuenta: ")
                amount = float(input("Ingrese el monto a extraer: "))
                result = cuentaController.extraer(connection=connection, id_account=id_account, amount=amount)
                if result:
                    print(success(message=f"Extracción realizada con éxito en la cuenta: {id_account}", status_code=200))
                else:
                    print(error(message="Error al realizar la extracción.", status_code=400))
            case "4":
                id_account_origen = input("Ingrese el número de cuenta origen: ")
                id_account_destino = input("Ingrese el número de cuenta destino: ")
                amount = float(input("Ingrese el monto a transferir: "))
                result = cuentaController.transferencia(connection=connection, id_account_source=id_account_origen, id_account_target=id_account_destino, amount=amount)
                if result:
                    print(success(message=f"Transferencia realizada con éxito entre las cuentas: {id_account_origen} y {id_account_destino}", status_code=200))
                else:
                    print(error(message="Error al realizar la transferencia.", status_code=400))
            case "5":
                id_account = input("Ingrese el número de cuenta: ")
                result = cuentaController.estadoCuenta(connection=connection, id_account=id_account)
                if result:
                    print(success(message=f"Su saldo es {result}", status_code=200))
                else:
                    print(error(message="Error al obtener el estado de la cuenta.", status_code=400))
            case "6":
                id_account = input("Ingrese el número de cuenta: ")
                result = cuentaController.imprimirDatos(connection=connection, id_account=id_account)
                if result:
                    print(success(message=f"Datos de la cuenta {id_account}: {result}", status_code=200))
                else:
                    print(error(message="Error al imprimir los datos de la cuenta.", status_code=400))
            case "exit":
                print("Saliendo del programa.")
                break
            

if __name__ == "__main__":
    main()