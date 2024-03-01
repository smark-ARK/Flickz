from pydantic import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str = "12345smARK"
    database_name: str
    database_username: str = "postgres"
    secret_key: str
    refresh_secret_key: str
    algorithm: str
    access_expire_minutes: int
    refresh_expire_minutes: int
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket_name: str


settings = Settings(_env_file=".env")
