"""
Configuração do banco de dados agnóstico.

Suporta:
- PostgreSQL
- Supabase (PostgreSQL)
- MS SQL Server

Usa SQLAlchemy 2.0 com suporte a múltiplos dialectos.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool, QueuePool
from typing import Generator
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Metadata com naming convention para compatibilidade entre bancos
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)

# Base class para models
Base = declarative_base(metadata=metadata)


def get_engine_kwargs() -> dict:
    """
    Retorna kwargs específicos para cada tipo de banco.
    
    Otimizações por dialeto:
    - PostgreSQL/Supabase: Pool de conexões otimizado
    - MS SQL Server: Configurações específicas para ODBC
    """
    base_kwargs = {
        "echo": settings.ENVIRONMENT == "development",  # Log SQL em dev
        "future": True,  # SQLAlchemy 2.0 style
    }
    
    if settings.DATABASE_TYPE == "mssql":
        # MS SQL Server com ODBC
        base_kwargs.update({
            "pool_pre_ping": True,  # Testa conexão antes de usar
            "pool_size": 10,
            "max_overflow": 20,
            "connect_args": {
                "connect_timeout": 30,
                "timeout": 30,
            }
        })
    elif settings.DATABASE_TYPE in ["postgresql", "supabase"]:
        # PostgreSQL/Supabase
        is_production = settings.ENVIRONMENT == "production"
        
        if is_production:
            # Produção: usa pool de conexões
            base_kwargs.update({
                "pool_pre_ping": True,
                "pool_size": 20,
                "max_overflow": 40,
                "pool_recycle": 3600,  # Recicla conexões a cada 1h
                "poolclass": QueuePool,
            })
        else:
            # Desenvolvimento: sem pool (NullPool não aceita pool_size/max_overflow)
            base_kwargs.update({
                "poolclass": NullPool,
            })
        
        # Supabase: Adiciona parâmetros específicos
        if settings.DATABASE_TYPE == "supabase":
            base_kwargs["connect_args"] = {
                "sslmode": "require",
                "options": "-c statement_timeout=30000"  # 30s timeout
            }
    
    return base_kwargs


# Engine global
engine = create_engine(
    settings.DATABASE_URL,
    **get_engine_kwargs()
)

# SessionLocal factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco.
    
    Uso em FastAPI:
    ```python
    @app.get("/items")
    def read_items(db: Session = Depends(get_db)):
        return db.query(Item).all()
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa o banco de dados.
    
    Cria todas as tabelas se não existirem.
    Em produção, use Alembic migrations ao invés disso.
    """
    logger.info(f"Inicializando banco de dados: {settings.DATABASE_TYPE}")
    
    try:
        # Importar todos os models aqui para que sejam registrados
        from app.models import lottery, draw, user  # noqa
        
        if settings.ENVIRONMENT == "dev":
            # Em dev, pode criar tabelas automaticamente
            Base.metadata.create_all(bind=engine)
            logger.info("Tabelas criadas com sucesso")
        else:
            logger.info("Produção: Use Alembic migrations")
            
    except Exception as e:
        logger.error(f"Erro ao inicializar banco: {e}")
        raise


def check_db_connection() -> bool:
    """
    Verifica se a conexão com o banco está ativa.
    
    Returns:
        bool: True se conectado, False caso contrário
    """
    try:
        with engine.connect() as conn:
            if settings.DATABASE_TYPE == "mssql":
                conn.execute("SELECT 1")
            else:  # postgresql/supabase
                conn.execute("SELECT 1")
        logger.info(f"✓ Conectado ao banco: {settings.DATABASE_TYPE}")
        return True
    except Exception as e:
        logger.error(f"✗ Erro de conexão: {e}")
        return False
