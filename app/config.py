from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str = None
    DATABASE_PORT: str = None
    DATABASE_PASSWORD: str = None
    DATABASE_NAME: str = None
    DATABASE_USERNAME: str = None
    DATABASE_URL: str = None  # Add this line
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def sql_alchemy_database_url(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL  # Use full URL if present
        return (
            f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
