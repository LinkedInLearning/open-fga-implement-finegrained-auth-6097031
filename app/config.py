from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Configuration
    app_title: str = "FastAPI OpenFGA Project"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./app.db"
    
    # Paso 3: Cargar las variables de entorno de OpenFGA
    # en este caso se esta usando pydantic-settings para manejar la configuración
    # mas info: https://github.com/pydantic/pydantic-settings

    openfga_api_url: str = "http://localhost:8080"
    openfga_store_id: str = ""
    openfga_authorization_model_id: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()