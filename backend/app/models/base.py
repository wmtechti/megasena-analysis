"""
SQLAlchemy Base e utilitários comuns.

Configuração agnóstica de banco de dados (PostgreSQL/Supabase/MSSQL).
"""

from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, DateTime


# Naming convention compatível com PostgreSQL, MSSQL e Supabase
# Evita conflitos de nomes entre dialetos
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(DeclarativeBase):
    """
    Base class para todos os modelos.
    
    Fornece:
    - Naming convention consistente
    - Timestamps automáticos (created_at, updated_at)
    - Nome de tabela automático baseado no nome da classe
    """
    metadata = metadata
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Gera nome de tabela automaticamente a partir do nome da classe.
        
        Examples:
            User -> users
            DrawFeature -> draw_features
        """
        # Converte CamelCase para snake_case e adiciona 's' no plural
        name = cls.__name__
        # Adiciona underscore antes de letras maiúsculas
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        
        # Adiciona 's' no plural (simplificado)
        if not name.endswith('s'):
            name += 's'
        
        return name


class TimestampMixin:
    """
    Mixin para adicionar timestamps automáticos.
    
    Adiciona colunas:
    - created_at: Data de criação (preenchido automaticamente)
    - updated_at: Data de atualização (atualizado automaticamente)
    """
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="Data de criação do registro"
    )
    
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="Data da última atualização"
    )
