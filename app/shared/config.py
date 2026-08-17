from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# Carga las variables del .env de la raíz del proyecto sin sobrescribir las del sistema.
load_dotenv(Path(__file__).resolve().parents[2] / ".env.example", override=False)


class Settings(BaseSettings):
    app_name: str = "codigo-cafe-api"
    environment: str = "local"
    api_prefix: str = "/api/v1"
    database_url: str = ""
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str = "codigo_cafe"
    mysql_user: str = "codigo_cafe"
    mysql_password: str = "codigo_cafe"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_verify_token: str = ""
    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()
