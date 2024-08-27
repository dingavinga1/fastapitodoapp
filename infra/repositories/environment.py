from typing import Any, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

from bll import IEnvironmentVariables

class DotenvEnvironmentVariables(BaseSettings, IEnvironmentVariables):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    JWT_SECRET: str
    JWT_EXPIRY: int
    DEBUG_MODE: bool

    @staticmethod
    @lru_cache
    def _get_dotenv():
        selected_env = os.getenv("CLEAN_ENV")
        if selected_env == 'PROD':
            return None

        if selected_env is None:
            return '.env'

        return f".env.{selected_env}"

    model_config = SettingsConfigDict(env_file=_get_dotenv(), env_file_encoding='utf-8')

    def get_var(self, key: str) -> Any:
        vars: Dict[str, Any] = self.model_dump()
        return vars.get(key)