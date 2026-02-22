# app/config.py

import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')

    @property
    def async_db_url(self) -> str:
        if self.db_url.startswith("postgresql+asyncpg://"):
            return self.db_url
        if self.db_url.startswith("postgresql://"):
            return self.db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.db_url

    @property
    def sync_db_url(self) -> str:
        if self.db_url.startswith("postgresql+psycopg2://"):
            return self.db_url
        if self.db_url.startswith("postgresql+asyncpg://"):
            return self.db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
        if self.db_url.startswith("postgresql://"):
            return self.db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return self.db_url

settings = Settings()
