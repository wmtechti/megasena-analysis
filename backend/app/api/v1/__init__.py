"""
API v1 routers.
"""

from fastapi import APIRouter
from app.api.v1 import lotteries

api_router = APIRouter()

# Incluir routers de cada módulo
api_router.include_router(
    lotteries.router,
    prefix="/lotteries",
    tags=["lotteries"]
)

__all__ = ["api_router"]
