# Environment Configuration
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EnvConfig:
    """Environment configuration class for managing all environment variables"""
    
    # Database Configuration
    DB_NAME = os.getenv('DB_NAME', 'visualflow_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    # AI/ML API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', '')
    LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'true')
    LANGCHAIN_PROJECT = os.getenv('LANGCHAIN_PROJECT', 'visualflow')
    
    # PlantUML Configuration
    PLANTUML_SERVER_URL = os.getenv('PLANTUML_SERVER_URL', 'http://www.plantuml.com/plantuml')
    
    # Django Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    
    # Application Configuration
    APP_NAME = os.getenv('APP_NAME', 'VisualFlow')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    
    @classmethod
    def get_database_url(cls):
        """Get database URL for Django"""
        return f'postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'
    
    @classmethod
    def validate_required_env_vars(cls):
        """Validate that all required environment variables are set"""
        required_vars = [
            'GROQ_API_KEY',
            'DB_PASSWORD'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True