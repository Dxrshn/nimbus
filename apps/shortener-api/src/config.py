from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql://nimbus:nimbus-local-dev@localhost:5432/nimbus"
    redis_url: str = "redis://localhost:6379"
    sqs_endpoint: str = "http://localhost:4566"
    sqs_queue_url: str = "http://localhost:4566/000000000000/click-events"
    aws_default_region: str = "ap-south-1"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    otlp_endpoint: str = "http://localhost:4317"

settings = Settings()