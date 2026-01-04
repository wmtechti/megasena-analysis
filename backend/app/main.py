"""
FastAPI main application.

Backend para plataforma multi-loteria com suporte multi-database.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.db import engine
from app.models import Base

# Importar routers (quando criados)
# from app.api.v1 import lotteries, users, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia lifecycle da aplicação.
    
    Startup:
    - Cria tabelas no banco (dev only)
    - Inicializa cache
    
    Shutdown:
    - Fecha conexões
    """
    # Startup
    print(f"🚀 Starting application with {settings.database_type} database...")
    
    # Em produção, usar Alembic migrations
    # Em desenvolvimento, criar tabelas automaticamente
    if settings.environment == "development":
        print("📦 Creating database tables...")
        Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    print("👋 Shutting down application...")
    engine.dispose()


app = FastAPI(
    title="Lottery Analysis API",
    description="API para análise espacial de loterias brasileiras",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status da aplicação e banco de dados
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "database": settings.database_type,
    }


@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        Informações básicas da API
    """
    return {
        "message": "Lottery Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Registrar routers (quando criados)
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(lotteries.router, prefix="/api/v1/lotteries", tags=["lotteries"])
