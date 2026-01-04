"""
Schemas Pydantic para loterias e sorteios.

Validação de dados de entrada/saída da API.
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date, datetime
from typing import List, Optional


# ========== Loteria ==========

class LotteryBase(BaseModel):
    """Schema base de loteria."""
    slug: str = Field(..., pattern="^[a-z]+$", max_length=50)
    name: str = Field(..., max_length=100)
    total_numbers: int = Field(..., gt=0)
    draw_size: int = Field(..., gt=0)
    grid_rows: int = Field(..., gt=0)
    grid_cols: int = Field(..., gt=0)


class LotteryCreate(LotteryBase):
    """Schema para criar loteria."""
    pass


class LotteryResponse(LotteryBase):
    """Schema de resposta de loteria."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ========== Sorteio (Draw) ==========

class DrawBase(BaseModel):
    """Schema base de sorteio."""
    contest_number: int = Field(..., gt=0, description="Número do concurso")
    draw_date: date = Field(..., description="Data do sorteio")
    numbers: List[int] = Field(..., description="Números sorteados")
    prize_value: Optional[float] = Field(None, ge=0, description="Valor do prêmio em R$")
    winners: Optional[int] = Field(None, ge=0, description="Quantidade de ganhadores")
    
    @field_validator("numbers")
    @classmethod
    def validate_numbers(cls, v: List[int]) -> List[int]:
        """Valida se números estão ordenados e não duplicados."""
        if len(v) != len(set(v)):
            raise ValueError("Números duplicados não são permitidos")
        
        if v != sorted(v):
            # Ordena automaticamente
            return sorted(v)
        
        return v


class DrawCreate(DrawBase):
    """Schema para criar sorteio."""
    lottery_id: int


class DrawResponse(DrawBase):
    """Schema de resposta de sorteio."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    lottery_id: int
    created_at: datetime
    updated_at: datetime


class DrawWithFeatures(DrawResponse):
    """Schema de resposta com features calculadas."""
    features: Optional['DrawFeatureResponse'] = None


# ========== Features ==========

class DrawFeatureResponse(BaseModel):
    """Schema de resposta com features espaciais."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    draw_id: int
    
    # Features básicas (15)
    mean_distance: float
    std_distance: float
    min_distance: float
    max_distance: float
    mean_row: float
    std_row: float
    mean_col: float
    std_col: float
    spread_row: int
    spread_col: int
    count_top_half: int
    count_bottom_half: int
    count_left_half: int
    count_right_half: int
    count_border: int
    
    # Features avançadas (12)
    spatial_autocorr: float
    cluster_coefficient: float
    mean_nearest_neighbor: float
    convex_hull_area: float
    centroid_distance: float
    quadrant_q1: int
    quadrant_q2: int
    quadrant_q3: int
    quadrant_q4: int
    entropy_spatial: float
    dispersion_index: float
    pattern_regularity: float
    
    created_at: datetime
    updated_at: datetime


# ========== Análise e Estatísticas ==========

class DrawStats(BaseModel):
    """Estatísticas gerais de uma loteria."""
    lottery_slug: str
    total_draws: int
    latest_contest: int
    earliest_date: date
    latest_date: date
    total_prize_value: Optional[float] = None


class NumberFrequency(BaseModel):
    """Frequência de um número específico."""
    number: int
    frequency: int
    percentage: float
    last_drawn: Optional[date] = None


class LotteryAnalysis(BaseModel):
    """Análise completa de uma loteria."""
    lottery: LotteryResponse
    stats: DrawStats
    most_frequent_numbers: List[NumberFrequency]
    least_frequent_numbers: List[NumberFrequency]
    avg_features: DrawFeatureResponse
