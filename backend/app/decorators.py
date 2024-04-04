import logging

from .app_utils import response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

def catch(status_code: int = 500, message: str = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f'Error in {func.__name__}: {e}')
                body = {"message": str(e if message is None else message)}
                return response(status_code, message)
        return wrapper
    return decorator
