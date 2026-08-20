from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Định nghĩa các biến môi trường cần thiết
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env" # Chỉ định file đọc biến môi trường

# Tạo một instance duy nhất (singleton) để import dùng ở mọi nơi
settings = Settings()