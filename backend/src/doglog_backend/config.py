from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = config('SECRET_KEY', cast=Secret)