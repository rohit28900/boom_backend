import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# ------------------------------------------------------------------------------
# Detect environment directly from .env (no need for export ENVIRONMENT)
# ------------------------------------------------------------------------------
default_env = "local"
env_file_base = ".env"

# Try to read ENVIRONMENT value from .env file if present
if os.path.exists(env_file_base):
    with open(env_file_base, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("ENVIRONMENT="):
                default_env = line.split("=", 1)[1].strip()
                break

ENV = default_env
env_file = f".env.{ENV}" if os.path.exists(f".env.{ENV}") else env_file_base

print(f"🔧 Loaded environment: {ENV} → using file: {env_file}")  # optional, for debugging

# ------------------------------------------------------------------------------
# Settings
# ------------------------------------------------------------------------------
class Settings(BaseSettings):
    # --- General ---
    ENVIRONMENT: str = "local"
    SECRET_KEY: str = "supersecretkey"
    LOG_LEVEL: str = "INFO"

    # --- Database URLs ---
    LOCAL_DATABASE_URL: Optional[str] = None
    PROD_DATABASE_URL: Optional[str] = None
    DATABASE_URL: Optional[str] = None  # Railway default fallback

    # --- Debug flags ---
    LOCAL_DEBUG: bool = True
    PROD_DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="allow",
    )

    @property
    def DATABASE_CONNECTION_URL(self) -> str:
        """Return the correct database URL based on environment."""
        env = self.ENVIRONMENT.lower()

        if env == "local" and self.LOCAL_DATABASE_URL:
            return self.LOCAL_DATABASE_URL
        elif env in ["prod", "production"] and self.PROD_DATABASE_URL:
            return self.PROD_DATABASE_URL
        elif self.DATABASE_URL:
            # ✅ Fallback for Railway or similar platforms
            return self.DATABASE_URL
        else:
            raise ValueError(
                f"No database URL found for environment '{self.ENVIRONMENT}'. "
                f"Expected LOCAL_DATABASE_URL, PROD_DATABASE_URL, or DATABASE_URL."
            )

    @property
    def DEBUG(self) -> bool:
        return self.LOCAL_DEBUG if self.ENVIRONMENT.lower() == "local" else self.PROD_DEBUG

# ------------------------------------------------------------------------------
# Cached settings
# ------------------------------------------------------------------------------
@lru_cache()
def get_settings():
    return Settings()

# Expose for easy imports
settings = get_settings()
DATABASE_URL = settings.DATABASE_CONNECTION_URL
DEBUG = settings.DEBUG
LOG_LEVEL = settings.LOG_LEVEL
