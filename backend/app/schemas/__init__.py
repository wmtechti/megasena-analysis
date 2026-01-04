"""
Schemas Pydantic.

Exporta todos os schemas para uso na API.
"""

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserRoleUpdate,
    UserResponse,
    UserWithPayment,
    Token,
    TokenPayload,
)

from app.schemas.lottery import (
    LotteryCreate,
    LotteryResponse,
    DrawCreate,
    DrawResponse,
    DrawWithFeatures,
    DrawFeatureResponse,
    DrawStats,
    NumberFrequency,
    LotteryAnalysis,
)


__all__ = [
    # User
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserRoleUpdate",
    "UserResponse",
    "UserWithPayment",
    "Token",
    "TokenPayload",
    # Lottery
    "LotteryCreate",
    "LotteryResponse",
    "DrawCreate",
    "DrawResponse",
    "DrawWithFeatures",
    "DrawFeatureResponse",
    "DrawStats",
    "NumberFrequency",
    "LotteryAnalysis",
]
