from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent
ENV_DIR = BASE_DIR / ".env"


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_asyncpg_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_psycopg2_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=ENV_DIR, extra="ignore")


class JwtSettings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "private_key.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public_key.pem"

    ALGORITHM: str
    ACCESS_TOKEN_NAME: str
    REFRESH_TOKEN_NAME: str
    ACCESS_TOKEN_EXPIRE_TIME: int
    REFRESH_TOKEN_EXPIRE_TIME: int

    model_config = SettingsConfigDict(env_file=ENV_DIR, extra="ignore")


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASS: str

    @property
    def redis_url(self):
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = SettingsConfigDict(env_file=ENV_DIR, extra="ignore")


class Settings(BaseSettings):
    MODE: str
    UPLOAD_PATH: Path = BASE_DIR / "uploads"

    db: DBSettings = DBSettings()
    jwt: JwtSettings = JwtSettings()
    redis: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(env_file=ENV_DIR, extra="ignore")


settings = Settings()
