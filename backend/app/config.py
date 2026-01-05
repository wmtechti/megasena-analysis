"""
Configuração centralizada da aplicação.

Suporta múltiplos tipos de banco de dados:
- PostgreSQL (local ou cloud)
- Supabase (PostgreSQL gerenciado)
- MS SQL Server (enterprise)
"""

from pydantic_settings import BaseSettings
from typing import Literal
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # Environment
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    # Database
    DATABASE_TYPE: Literal["postgresql", "supabase", "mssql"] = "postgresql"
    DATABASE_URL: str
    
    # Supabase specific (optional)
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "LoteriaTech API"
    
    # Redis (optional)
    REDIS_URL: str | None = None
    
    # Celery (optional)
    CELERY_BROKER_URL: str | None = None
    CELERY_RESULT_BACKEND: str | None = None
    
    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def environment(self) -> str:
        """Retorna environment."""
        return self.ENVIRONMENT
    
    @property
    def database_type(self) -> str:
        """Retorna tipo de banco de dados."""
        return self.DATABASE_TYPE
    
    @property
    def database_url(self) -> str:
        """Retorna URL do banco de dados."""
        return self.DATABASE_URL
    
    @property
    def cors_origins(self) -> list[str]:
        """Retorna lista de origens CORS permitidas."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Verifica se está em produção."""
        return self.ENVIRONMENT == "production"
    
    @property
    def database_dialect(self) -> str:
        """Retorna o dialeto do banco de dados."""
        if self.DATABASE_TYPE == "mssql":
            return "mssql"
        else:  # postgresql ou supabase
            return "postgresql"


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna instância singleton das configurações.
    
    @lru_cache garante que Settings() seja chamado apenas uma vez.
    """
    settings = Settings()
    print(f"[DEBUG] Loaded DATABASE_URL: {settings.DATABASE_URL}")
    print(f"[DEBUG] Database type: {settings.DATABASE_TYPE}")
    return settings


# Instância global
settings = get_settings()
