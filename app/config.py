import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # API
    API_TITLE: str = "Coffee Shop API"
    API_DESCRIPTION: str = "API para gerenciamento de pedidos de café"
    API_VERSION: str = "1.0.0"
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]

settings = Settings()
