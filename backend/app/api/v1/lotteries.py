"""
Endpoints de loterias.

Operações CRUD e consultas de loterias.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.lottery import Lottery, Draw
from app.schemas.lottery import (
    LotteryResponse,
    DrawResponse,
    DrawWithFeaturesResponse,
)
from app.services.lottery_service import LotteryService
from app.services.draw_service import DrawService

router = APIRouter()


@router.get("", response_model=List[LotteryResponse])
def list_lotteries(
    only_active: bool = True,
    db: Session = Depends(get_db)
):
    """
    Lista todas as loterias disponíveis.
    
    Args:
        only_active: Retornar apenas loterias ativas
        db: Sessão do banco de dados
        
    Returns:
        Lista de loterias
    """
    lotteries = LotteryService.get_all(db, only_active=only_active)
    return lotteries


@router.get("/{slug}", response_model=LotteryResponse)
def get_lottery(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Detalhes de uma loteria específica.
    
    Args:
        slug: Identificador da loteria (megasena, lotofacil, etc.)
        db: Sessão do banco de dados
        
    Returns:
        Dados da loteria
        
    Raises:
        404: Loteria não encontrada
    """
    lottery = LotteryService.get_by_slug(db, slug)
    if not lottery:
        raise HTTPException(status_code=404, detail=f"Lottery '{slug}' not found")
    return lottery


@router.get("/{slug}/draws", response_model=List[DrawResponse])
def list_draws(
    slug: str,
    skip: int = Query(0, ge=0, description="Quantidade de registros a pular"),
    limit: int = Query(100, ge=1, le=500, description="Máximo de registros"),
    order_desc: bool = Query(True, description="Ordenar por concurso decrescente"),
    db: Session = Depends(get_db)
):
    """
    Lista histórico de sorteios de uma loteria (paginado).
    
    Args:
        slug: Identificador da loteria
        skip: Quantos registros pular (paginação)
        limit: Máximo de registros a retornar
        order_desc: Ordenar por número do concurso decrescente
        db: Sessão do banco de dados
        
    Returns:
        Lista de sorteios
        
    Raises:
        404: Loteria não encontrada
    """
    lottery = LotteryService.get_by_slug(db, slug)
    if not lottery:
        raise HTTPException(status_code=404, detail=f"Lottery '{slug}' not found")
    
    draws = DrawService.get_by_lottery(
        db,
        lottery_id=lottery.id,
        skip=skip,
        limit=limit,
        order_desc=order_desc
    )
    
    return draws


@router.get("/{slug}/draws/{contest_number}", response_model=DrawWithFeaturesResponse)
def get_draw(
    slug: str,
    contest_number: int,
    db: Session = Depends(get_db)
):
    """
    Detalhes de um sorteio específico (com features espaciais).
    
    Args:
        slug: Identificador da loteria
        contest_number: Número do concurso
        db: Sessão do banco de dados
        
    Returns:
        Dados do sorteio com features espaciais
        
    Raises:
        404: Loteria ou sorteio não encontrado
    """
    lottery = LotteryService.get_by_slug(db, slug)
    if not lottery:
        raise HTTPException(status_code=404, detail=f"Lottery '{slug}' not found")
    
    draw = DrawService.get_by_contest(db, lottery.id, contest_number)
    if not draw:
        raise HTTPException(
            status_code=404,
            detail=f"Contest {contest_number} not found for lottery '{slug}'"
        )
    
    return draw


@router.get("/{slug}/stats")
def get_stats(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Estatísticas gerais de uma loteria.
    
    Retorna informações como:
    - Total de sorteios
    - Último concurso
    - Data do último sorteio
    - Números do último sorteio
    
    Args:
        slug: Identificador da loteria
        db: Sessão do banco de dados
        
    Returns:
        Estatísticas da loteria
        
    Raises:
        404: Loteria não encontrada
    """
    lottery = LotteryService.get_by_slug(db, slug)
    if not lottery:
        raise HTTPException(status_code=404, detail=f"Lottery '{slug}' not found")
    
    stats = LotteryService.get_stats(db, slug)
    return stats


@router.get("/{slug}/frequency")
def get_frequency(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Frequência de números sorteados.
    
    Retorna a contagem de quantas vezes cada número foi sorteado,
    ordenado do mais frequente para o menos frequente.
    
    Args:
        slug: Identificador da loteria
        db: Sessão do banco de dados
        
    Returns:
        Frequência de cada número
        
    Raises:
        404: Loteria não encontrada
    """
    lottery = LotteryService.get_by_slug(db, slug)
    if not lottery:
        raise HTTPException(status_code=404, detail=f"Lottery '{slug}' not found")
    
    frequency = LotteryService.get_frequency(db, slug)
    return frequency


@router.get("/{slug}/analysis")
def get_analysis(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Análise completa de uma loteria.
    
    Combina estatísticas gerais, frequência de números e
    informações sobre o último sorteio.
    
    Args:
        slug: Identificador da loteria
        db: Sessão do banco de dados
        
    Returns:
        Análise completa
        
    Raises:
        404: Loteria não encontrada
    """
    lottery = LotteryService.get_by_slug(db, slug)
    if not lottery:
        raise HTTPException(status_code=404, detail=f"Lottery '{slug}' not found")
    
    stats = LotteryService.get_stats(db, slug)
    frequency = LotteryService.get_frequency(db, slug)
    
    return {
        "lottery": stats["lottery"],
        "statistics": {
            "total_draws": stats["total_draws"],
            "last_contest": stats["last_contest"],
            "last_draw_date": stats["last_draw_date"],
            "last_numbers": stats["last_numbers"],
        },
        "frequency": frequency["frequency"][:10],  # Top 10 mais frequentes
    }
