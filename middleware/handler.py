from config.config import get_logger
from middleware.response import error
from functools import wraps

logger = get_logger(__name__)

def route_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            # errores HTTP que vos lanzás (401, 403, 404...)
            return error(message=e.detail, status_code=e.status_code)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {e}")
            return error(message="Error interno del servidor", status_code=500)
    return wrapper