# import os
# from pydantic_settings import BaseSettings, SettingsConfigDict
# from functools import lru_cache

# # Determine current environment
# ENV = os.getenv("ENVIRONMENT", "local")

# # Automatically load .env file based on environment
# env_file = f".env.{ENV}" if os.path.exists(f".env.{ENV}") else ".env"

# class Settings(BaseSettings):
#     ENVIRONMENT: str = "local"
#     DEBUG: bool = True

#     DATABASE_URL: str
#     SECRET_KEY: str
#     LOG_LEVEL: str = "INFO"

#     model_config = SettingsConfigDict(
#         env_file=env_file,
#         env_file_encoding="utf-8",
#         extra="ignore"
#     )

# @lru_cache()
# def get_settings():
#     return Settings()

# settings = get_settings()

# # Expose common ones for easy import
# LOG_LEVEL = settings.LOG_LEVEL

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# Choose env file based on ENVIRONMENT variable
ENV = os.getenv("ENVIRONMENT", "local")
env_file = f".env.{ENV}" if os.path.exists(f".env.{ENV}") else ".env"

class Settings(BaseSettings):
    # General
    ENVIRONMENT: str = "local"
    SECRET_KEY: str
    LOG_LEVEL: str = "INFO"

    # Local DB
    LOCAL_DATABASE_URL: str
    LOCAL_DEBUG: bool = True

    # Production DB
    PROD_DATABASE_URL: str
    PROD_DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="allow",  # allow extra keys in .env
    )

    @property
    def DATABASE_URL(self) -> str:
        if self.ENVIRONMENT.lower() == "local":
            return self.LOCAL_DATABASE_URL
        else:
            return self.PROD_DATABASE_URL

    @property
    def DEBUG(self) -> bool:
        return self.LOCAL_DEBUG if self.ENVIRONMENT.lower() == "local" else self.PROD_DEBUG

# Cache settings
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Convenience variables
DATABASE_URL = settings.DATABASE_URL
DEBUG = settings.DEBUG
LOG_LEVEL = settings.LOG_LEVEL

# Test when running directly
if __name__ == "__main__":
    print("ENVIRONMENT:", settings.ENVIRONMENT)
    print("DEBUG:", settings.DEBUG)
    print("DATABASE_URL:", settings.DATABASE_URL)
    print("LOG_LEVEL:", settings.LOG_LEVEL)
