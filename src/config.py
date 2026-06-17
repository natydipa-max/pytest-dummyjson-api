import os

BASE_URL = os.getenv("BASE_URL", "https://dummyjson.com")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))