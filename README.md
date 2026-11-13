# Gestor de cuentas bancarias

Aplicación bancaria sencilla de línea de comandos, desarrollada con Python y SQLite. Es un proyecto académico para practicar programación orientada a objetos y separar las reglas de las cuentas del almacenamiento de datos.

## Funcionalidades

- Crear cuentas y generar su identificador.
- Depositar y retirar dinero.
- Transferir dinero entre cuentas si hay saldo suficiente en la cuenta de origen.
- Consultar si el saldo es acreedor o deudor.
- Ver el titular y el saldo de una cuenta.

Un retiro puede dejar la cuenta con saldo negativo. Las transferencias requieren fondos suficientes y guardan juntos los saldos de ambas cuentas.

## Requisitos

- Python 3.12 o posterior.
- [uv](https://docs.astral.sh/uv/) para instalar las dependencias fijadas del proyecto.

## Ejecución

Desde la carpeta del proyecto:

```sh
uv sync
uv run python main.py
```

Elegí una operación del menú. Guardá el identificador que se muestra al crear una cuenta; lo vas a necesitar para las operaciones siguientes. Ingresá los montos con decimales, por ejemplo `25.50`. Escribí `exit` para salir.

Al iniciar, la aplicación crea `accounts.db` en el directorio actual. Si la base contiene la tabla anterior `cuentas`, sus filas se copian a la tabla `accounts` la primera vez que se inicializa el repositorio. La tabla original se conserva.

## Estructura del proyecto

- `main.py` gestiona el menú de consola y la entrada del usuario.
- `controllers/AccountController.py` coordina las solicitudes y delega las operaciones de las cuentas.
- `models/Account.py` contiene el estado de la cuenta y las reglas para depósitos, retiros, transferencias y consultas de saldo.
- `db/account_repository.py` convierte filas de SQLite en objetos `Account` y guarda los cambios.
- `db/connection.py` administra la conexión con SQLite.
- `middleware/` contiene las respuestas y el manejador de errores.

