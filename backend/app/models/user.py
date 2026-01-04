"""
Modelo de usuários.

Suporta múltiplos bancos de dados (PostgreSQL/Supabase/MSSQL).
"""

from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    """Papéis de usuário no sistema."""
    FREE = "free"
    INDIVIDUAL = "individual"
    MULTI = "multi"
    COMPLETE = "complete"
    ADMIN = "admin"


class User(Base, TimestampMixin):
    """
    Modelo de usuário.
    
    Attributes:
        id: Identificador único
        email: Email (único, usado para login)
        name: Nome completo
        password_hash: Senha criptografada (bcrypt)
        is_active: Conta ativa?
        role: Papel/plano do usuário
        stripe_customer_id: ID do cliente no Stripe (nullable)
        mercadopago_customer_id: ID do cliente no Mercado Pago (nullable)
    """
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True, comment="Email do usuário")
    name = Column(String(255), nullable=False, comment="Nome completo")
    password_hash = Column(String(255), nullable=False, comment="Senha criptografada (bcrypt)")
    is_active = Column(Boolean, default=True, nullable=False, comment="Conta ativa?")
    role = Column(
        SQLEnum(UserRole, native_enum=False),  # native_enum=False para compatibilidade MSSQL
        default=UserRole.FREE,
        nullable=False,
        index=True,
        comment="Papel/plano do usuário"
    )
    
    # Integrações de pagamento (nullable)
    stripe_customer_id = Column(String(255), nullable=True, index=True, comment="ID do cliente no Stripe")
    mercadopago_customer_id = Column(String(255), nullable=True, index=True, comment="ID do cliente no Mercado Pago")
    
    # Relacionamentos
    # subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role={self.role})>"
    
    @property
    def has_premium_access(self) -> bool:
        """Verifica se usuário tem acesso premium (Individual ou superior)."""
        return self.role in [UserRole.INDIVIDUAL, UserRole.MULTI, UserRole.COMPLETE, UserRole.ADMIN]
    
    @property
    def can_access_all_lotteries(self) -> bool:
        """Verifica se usuário tem acesso a todas as loterias (Complete ou Admin)."""
        return self.role in [UserRole.COMPLETE, UserRole.ADMIN]
    
    @property
    def max_lotteries(self) -> int:
        """Retorna quantidade máxima de loterias que o usuário pode acessar."""
        limits = {
            UserRole.FREE: 1,
            UserRole.INDIVIDUAL: 1,
            UserRole.MULTI: 3,
            UserRole.COMPLETE: 999,  # Ilimitado
            UserRole.ADMIN: 999,
        }
        return limits.get(self.role, 0)
