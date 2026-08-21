from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Định nghĩa các biến môi trường cần thiết
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Chỉ định file .env để pydantic-settings tự động đọc
        env_file = ".env"
        env_file_encoding = "utf-8"

# để import dùng ở mọi nơi
settings = Settings()