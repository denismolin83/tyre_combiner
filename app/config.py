from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Параметры БД (совпадают с docker-compose.yml)
    DB_USER: str = "admin"
    DB_PASSWORD: str = "secret_password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "tyre_combiner_db"

    # Ссылка на xml ЯМ Robotyre
    ROBOTYRE_XML_URL: str = "https://lk.robotyre.ru/Shop/MarketUnloadings/GetYandexMarketUnloading?customerId=48691"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
