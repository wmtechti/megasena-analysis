"""
Serviço de sorteios.

Lógica de negócio para operações com sorteios (draws).
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from app.models.lottery import Lottery, Draw, DrawFeature
from app.schemas.lottery import DrawCreate
from app.lotteries import lottery_registry


class DrawService:
    """Serviço para operações com sorteios."""
    
    @staticmethod
    def get_by_lottery(
        db: Session,
        lottery_id: int,
        skip: int = 0,
        limit: int = 100,
        order_desc: bool = True
    ) -> List[Draw]:
        """
        Lista sorteios de uma loteria (paginado).
        
        Args:
            db: Sessão do banco
            lottery_id: ID da loteria
            skip: Quantos registros pular
            limit: Máximo de registros
            order_desc: Ordenar por concurso decrescente
            
        Returns:
            Lista de sorteios
        """
        query = db.query(Draw).filter(Draw.lottery_id == lottery_id)
        
        if order_desc:
            query = query.order_by(desc(Draw.contest_number))
        else:
            query = query.order_by(Draw.contest_number)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_contest(
        db: Session,
        lottery_id: int,
        contest_number: int
    ) -> Optional[Draw]:
        """
        Busca sorteio específico por número do concurso.
        
        Args:
            db: Sessão do banco
            lottery_id: ID da loteria
            contest_number: Número do concurso
            
        Returns:
            Sorteio encontrado ou None
        """
        return db.query(Draw).filter(
            and_(
                Draw.lottery_id == lottery_id,
                Draw.contest_number == contest_number
            )
        ).first()
    
    @staticmethod
    def create(db: Session, draw_data: DrawCreate) -> Draw:
        """
        Cria novo sorteio.
        
        Args:
            db: Sessão do banco
            draw_data: Dados do sorteio
            
        Returns:
            Sorteio criado
        """
        draw = Draw(**draw_data.model_dump())
        db.add(draw)
        db.commit()
        db.refresh(draw)
        return draw
    
    @staticmethod
    def calculate_features(db: Session, draw: Draw) -> DrawFeature:
        """
        Calcula features espaciais de um sorteio.
        
        Args:
            db: Sessão do banco
            draw: Sorteio para calcular features
            
        Returns:
            Features calculadas
        """
        # Buscar loteria
        lottery = db.query(Lottery).filter(Lottery.id == draw.lottery_id).first()
        if not lottery:
            raise ValueError(f"Lottery {draw.lottery_id} not found")
        
        # Obter classe da loteria do registry
        lottery_class = lottery_registry.get(lottery.slug)
        if not lottery_class:
            raise ValueError(f"Lottery class for '{lottery.slug}' not found in registry")
        
        # Calcular features
        features_dict = lottery_class.calculate_features(draw.numbers)
        
        # Criar modelo de features
        features = DrawFeature(
            draw_id=draw.id,
            **features_dict
        )
        
        db.add(features)
        db.commit()
        db.refresh(features)
        
        return features
    
    @staticmethod
    def bulk_import(
        db: Session,
        lottery_id: int,
        draws_data: List[dict],
        calculate_features: bool = True
    ) -> int:
        """
        Importação em massa de sorteios.
        
        Args:
            db: Sessão do banco
            lottery_id: ID da loteria
            draws_data: Lista de dicionários com dados dos sorteios
            calculate_features: Se deve calcular features automaticamente
            
        Returns:
            Quantidade de sorteios importados
        """
        imported = 0
        
        for data in draws_data:
            # Verificar se já existe
            existing = DrawService.get_by_contest(
                db,
                lottery_id,
                data["contest_number"]
            )
            
            if existing:
                continue
            
            # Criar sorteio
            draw = Draw(
                lottery_id=lottery_id,
                contest_number=data["contest_number"],
                draw_date=data["draw_date"],
                numbers=data["numbers"],
                prize_value=data.get("prize_value"),
                winners=data.get("winners"),
            )
            
            db.add(draw)
            db.flush()  # Para obter o ID
            
            # Calcular features se solicitado
            if calculate_features:
                try:
                    DrawService.calculate_features(db, draw)
                except Exception as e:
                    print(f"⚠️  Erro ao calcular features do concurso {data['contest_number']}: {e}")
            
            imported += 1
            
            # Commit a cada 100 registros
            if imported % 100 == 0:
                db.commit()
                print(f"  → {imported} sorteios importados...")
        
        db.commit()
        return imported
