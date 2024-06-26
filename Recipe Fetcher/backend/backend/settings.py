from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_API_KEY: str
    SEARCH_ENGINE_ID: str

    class Config:
        env_file = ".env"

settings = Settings()

print(f"GOOGLE_API_KEY: {settings.GOOGLE_API_KEY}")
print(f"SEARCH_ENGINE_ID: {settings.SEARCH_ENGINE_ID}")
