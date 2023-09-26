from dynaconf import settings


ENV = settings.ENV
DB_TYPE: str = settings.DB_TYPE or "sqlite"
DB_HOST: str = settings.DB_HOST or ""
DB_PORT: int = settings.DB_PORT or 0
DB_USER: str = settings.DB_USER or ""
DB_PASSWORD: str = settings.DB_PASSWORD or ""
DB_DATABASE: str = settings.DB_DATABASE or ".db/demo.sqlite"

SSH_HOST: str = settings.SSH_HOST or ""
SSH_USER: str = settings.SSH_USER or ""
SSH_PASSWORD: str = settings.SSH_PASSWORD or ""
SSH_KEYFILE: str = settings.SSH_KEYFILE or ""
SSH_PORT: int = settings.SSH_PORT or 22
