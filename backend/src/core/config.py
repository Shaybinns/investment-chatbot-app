from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Investment Chatbot"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/db"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()