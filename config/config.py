from dotenv import load_dotenv
import logging
import os

load_dotenv()  # Carga las variables de entorno desde el archivo .env

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def get_logger(name: str):
    return logging.getLogger(name=name)
    
config_db = {
    "TABLE": os.getenv("TABLE")
}