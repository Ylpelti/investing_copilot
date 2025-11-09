from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    database_url: str = Field(default="sqlite:///./investing_copilot.db", env="DATABASE_URL")
    environment: str = "development"

    # 👇 Correct v2 configuration style
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # ignore any extra env vars not defined as fields
    )

# Singleton instance
settings = Settings()
