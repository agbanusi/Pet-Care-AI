from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Pet Care App"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    OPENAI_API_KEY: str
    OPENAI_ASST_ID: str
    class Config:
        env_file = ".env"

settings = Settings()