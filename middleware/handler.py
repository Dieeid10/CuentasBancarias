from config.config import get_logger
from middleware.response import error
from functools import wraps

logger = get_logger(__name__)

def route_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return error(message="Internal server error", status_code=500)
    return wrapper