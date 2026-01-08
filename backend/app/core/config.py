from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from app.schemas.llm_provider import LLMProvider


class Settings(BaseSettings):
    secret_key: str = Field(min_length=5)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    database_url: str


    environment: str = "development"

    llm_provider: LLMProvider = LLMProvider.OPENAI
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
