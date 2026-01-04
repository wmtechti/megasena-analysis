"""
Schemas Pydantic para usuários.

Validação de dados de entrada/saída da API.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

from app.models.user import UserRole


# ========== Schemas de criação ==========

class UserCreate(BaseModel):
    """Schema para criação de usuário."""
    email: EmailStr = Field(..., description="Email do usuário")
    name: str = Field(..., min_length=2, max_length=255, description="Nome completo")
    password: str = Field(..., min_length=8, max_length=100, description="Senha (mínimo 8 caracteres)")


class UserLogin(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str


# ========== Schemas de atualização ==========

class UserUpdate(BaseModel):
    """Schema para atualização de usuário."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserRoleUpdate(BaseModel):
    """Schema para atualização de role (admin only)."""
    role: UserRole


# ========== Schemas de resposta ==========

class UserResponse(BaseModel):
    """Schema de resposta com dados do usuário."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    name: str
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime
    
    # Propriedades calculadas
    has_premium_access: bool
    can_access_all_lotteries: bool
    max_lotteries: int


class UserWithPayment(UserResponse):
    """Schema com informações de pagamento (admin only)."""
    stripe_customer_id: Optional[str] = None
    mercadopago_customer_id: Optional[str] = None


# ========== Schemas de autenticação ==========

class Token(BaseModel):
    """Schema de resposta com token JWT."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenPayload(BaseModel):
    """Payload do token JWT."""
    sub: int  # user_id
    exp: datetime
    role: UserRole
