import os

BASE_URL = os.getenv("BASE_URL", "https://dummyjson.com")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))

AUTH_USERNAME = os.getenv("AUTH_USERNAME", "emilys")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "emilyspass")