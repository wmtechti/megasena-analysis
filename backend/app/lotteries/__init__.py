"""
Módulo de loterias disponíveis.

Centraliza todas as implementações de loterias.
"""

from app.lotteries.base import LotteryBase
from app.lotteries.megasena import megasena
from app.lotteries.lotofacil import lotofacil


# Registry de todas as loterias
LOTTERIES: dict[str, LotteryBase] = {
    "megasena": megasena,
    "lotofacil": lotofacil,
}


def get_lottery(slug: str) -> LotteryBase:
    """
    Retorna instância de loteria pelo slug.
    
    Args:
        slug: Identificador da loteria (ex: 'megasena', 'lotofacil')
        
    Returns:
        Instância da loteria
        
    Raises:
        ValueError: Se loteria não encontrada
        
    Examples:
        >>> lottery = get_lottery("megasena")
        >>> lottery.name
        'Mega-Sena'
    """
    if slug not in LOTTERIES:
        available = ", ".join(LOTTERIES.keys())
        raise ValueError(f"Loteria '{slug}' não encontrada. Disponíveis: {available}")
    
    return LOTTERIES[slug]


def list_lotteries() -> list[dict]:
    """
    Lista todas as loterias disponíveis.
    
    Returns:
        Lista de dicionários com metadados das loterias
        
    Examples:
        >>> lotteries = list_lotteries()
        >>> len(lotteries)
        2
        >>> lotteries[0]['slug']
        'megasena'
    """
    return [
        {
            "slug": lottery.slug,
            "name": lottery.name,
            "total_numbers": lottery.total_numbers,
            "draw_size": lottery.draw_size,
            "grid_rows": lottery.grid_rows,
            "grid_cols": lottery.grid_cols,
        }
        for lottery in LOTTERIES.values()
    ]


__all__ = ["LotteryBase", "megasena", "lotofacil", "LOTTERIES", "get_lottery", "list_lotteries"]
