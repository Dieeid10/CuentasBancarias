from dotenv import load_dotenv
import logging
import os

load_dotenv()  # Load environment variables from the .env file.

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def get_logger(name: str):
    return logging.getLogger(name=name)
    
DATABASE_CONFIG = {
    "TABLE_NAME": os.getenv("TABLE_NAME", "accounts")
}