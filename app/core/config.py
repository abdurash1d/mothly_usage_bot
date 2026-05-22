from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Oylik Rasxot Bot"
    app_base_url: str = "http://localhost:8000"
    secret_key: str = "change-me"

    bot_token: str = ""
    owner_telegram_id: int = 0
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/rasxot_bot"
    webapp_url: str = "http://localhost:8000/app"

    timezone: str = "Asia/Tashkent"

    @property
    def sqlalchemy_database_url(self) -> str:
        # Render/Postgres often provides postgres:// or postgresql://
        # SQLAlchemy with psycopg driver should use postgresql+psycopg://
        if self.database_url.startswith("postgres://"):
            return self.database_url.replace("postgres://", "postgresql+psycopg://", 1)
        if self.database_url.startswith("postgresql://") and "+psycopg" not in self.database_url:
            return self.database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return self.database_url


settings = Settings()
