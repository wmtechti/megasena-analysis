"""
Modelos de loterias e sorteios.

Tabelas agnósticas de banco de dados.
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, JSON, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class Lottery(Base, TimestampMixin):
    """
    Modelo de loteria.
    
    Armazena configurações das loterias disponíveis.
    
    Attributes:
        id: Identificador único
        slug: Identificador textual (ex: 'megasena')
        name: Nome oficial (ex: 'Mega-Sena')
        total_numbers: Total de números disponíveis
        draw_size: Quantidade de números sorteados
        grid_rows: Linhas do volante
        grid_cols: Colunas do volante
        is_active: Loteria ativa no sistema?
    """
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, nullable=False, index=True, comment="Identificador (megasena, lotofacil...)")
    name = Column(String(100), nullable=False, comment="Nome oficial da loteria")
    total_numbers = Column(Integer, nullable=False, comment="Total de números disponíveis")
    draw_size = Column(Integer, nullable=False, comment="Quantidade de números sorteados")
    grid_rows = Column(Integer, nullable=False, comment="Linhas do volante")
    grid_cols = Column(Integer, nullable=False, comment="Colunas do volante")
    is_active = Column(Boolean, default=True, nullable=False, comment="Loteria ativa?")
    
    # Relacionamentos
    draws = relationship("Draw", back_populates="lottery", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Lottery(id={self.id}, slug='{self.slug}', name='{self.name}')>"


class Draw(Base, TimestampMixin):
    """
    Modelo de sorteio (concurso).
    
    Armazena os resultados históricos dos sorteios.
    
    Attributes:
        id: Identificador único
        lottery_id: FK para loteria
        contest_number: Número do concurso
        draw_date: Data do sorteio
        numbers: Lista de números sorteados (JSON: [1, 5, 12, ...])
        prize_value: Valor do prêmio principal (em centavos)
        winners: Quantidade de ganhadores
    """
    
    id = Column(Integer, primary_key=True, index=True)
    lottery_id = Column(Integer, ForeignKey('lotteries.id'), nullable=False, index=True)
    contest_number = Column(Integer, nullable=False, comment="Número do concurso")
    draw_date = Column(Date, nullable=False, index=True, comment="Data do sorteio")
    
    # Números sorteados (armazenados como JSON para compatibilidade multi-DB)
    # PostgreSQL: pode usar ARRAY, mas JSON é universal
    numbers = Column(JSON, nullable=False, comment="Números sorteados [1, 5, 12, ...]")
    
    # Informações do prêmio
    prize_value = Column(Float, nullable=True, comment="Valor do prêmio em R$ (float)")
    winners = Column(Integer, nullable=True, comment="Quantidade de ganhadores")
    
    # Relacionamentos
    lottery = relationship("Lottery", back_populates="draws")
    features = relationship("DrawFeature", back_populates="draw", cascade="all, delete-orphan", uselist=False)
    
    # Índices compostos para consultas rápidas
    __table_args__ = (
        UniqueConstraint('lottery_id', 'contest_number', name='uq_lottery_contest'),
        Index('ix_lottery_date', 'lottery_id', 'draw_date'),
    )
    
    def __repr__(self) -> str:
        return f"<Draw(id={self.id}, lottery_id={self.lottery_id}, contest={self.contest_number})>"


class DrawFeature(Base, TimestampMixin):
    """
    Características espaciais calculadas para cada sorteio.
    
    Armazena 27 features de análise espacial + metadados.
    
    Attributes:
        id: Identificador único
        draw_id: FK para sorteio
        
        # Features básicas (15)
        mean_distance: Distância média entre números
        std_distance: Desvio padrão das distâncias
        min_distance: Distância mínima
        max_distance: Distância máxima
        mean_row: Linha média
        std_row: Desvio padrão das linhas
        mean_col: Coluna média
        std_col: Desvio padrão das colunas
        spread_row: Amplitude das linhas (max - min)
        spread_col: Amplitude das colunas (max - min)
        count_top_half: Números na metade superior
        count_bottom_half: Números na metade inferior
        count_left_half: Números na metade esquerda
        count_right_half: Números na metade direita
        count_border: Números nas bordas
        
        # Features avançadas (12)
        spatial_autocorr: Autocorrelação espacial (I de Moran)
        cluster_coefficient: Coeficiente de clustering
        mean_nearest_neighbor: Distância média ao vizinho mais próximo
        convex_hull_area: Área do polígono convexo
        centroid_distance: Distância do centro do volante
        quadrant_q1: Números no quadrante 1
        quadrant_q2: Números no quadrante 2
        quadrant_q3: Números no quadrante 3
        quadrant_q4: Números no quadrante 4
        entropy_spatial: Entropia espacial
        dispersion_index: Índice de dispersão
        pattern_regularity: Regularidade do padrão
    """
    
    id = Column(Integer, primary_key=True, index=True)
    draw_id = Column(Integer, ForeignKey('draws.id'), nullable=False, unique=True, index=True)
    
    # Features básicas (15)
    mean_distance = Column(Float, comment="Distância média entre números")
    std_distance = Column(Float, comment="Desvio padrão das distâncias")
    min_distance = Column(Float, comment="Distância mínima")
    max_distance = Column(Float, comment="Distância máxima")
    mean_row = Column(Float, comment="Linha média")
    std_row = Column(Float, comment="Desvio padrão das linhas")
    mean_col = Column(Float, comment="Coluna média")
    std_col = Column(Float, comment="Desvio padrão das colunas")
    spread_row = Column(Integer, comment="Amplitude das linhas")
    spread_col = Column(Integer, comment="Amplitude das colunas")
    count_top_half = Column(Integer, comment="Números metade superior")
    count_bottom_half = Column(Integer, comment="Números metade inferior")
    count_left_half = Column(Integer, comment="Números metade esquerda")
    count_right_half = Column(Integer, comment="Números metade direita")
    count_border = Column(Integer, comment="Números nas bordas")
    
    # Features avançadas (12)
    spatial_autocorr = Column(Float, comment="I de Moran")
    cluster_coefficient = Column(Float, comment="Coef. clustering")
    mean_nearest_neighbor = Column(Float, comment="Dist. vizinho próximo")
    convex_hull_area = Column(Float, comment="Área polígono convexo")
    centroid_distance = Column(Float, comment="Distância do centro")
    quadrant_q1 = Column(Integer, comment="Números quadrante 1")
    quadrant_q2 = Column(Integer, comment="Números quadrante 2")
    quadrant_q3 = Column(Integer, comment="Números quadrante 3")
    quadrant_q4 = Column(Integer, comment="Números quadrante 4")
    entropy_spatial = Column(Float, comment="Entropia espacial")
    dispersion_index = Column(Float, comment="Índice de dispersão")
    pattern_regularity = Column(Float, comment="Regularidade do padrão")
    
    # Relacionamentos
    draw = relationship("Draw", back_populates="features")
    
    def __repr__(self) -> str:
        return f"<DrawFeature(id={self.id}, draw_id={self.draw_id})>"


# Import necessário no topo do arquivo
from sqlalchemy import Boolean
