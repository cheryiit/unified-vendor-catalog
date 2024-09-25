from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    POSTGRES_DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "product_updates"

    class Config:
        env_file = ".env"

settings = Settings()