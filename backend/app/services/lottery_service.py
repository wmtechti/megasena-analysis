"""
Serviço de loterias.

Lógica de negócio para operações com loterias.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.lottery import Lottery, Draw
from app.schemas.lottery import LotteryCreate
from app.lotteries import lottery_registry


class LotteryService:
    """Serviço para operações com loterias."""
    
    @staticmethod
    def get_all(db: Session, only_active: bool = True) -> List[Lottery]:
        """
        Lista todas as loterias.
        
        Args:
            db: Sessão do banco
            only_active: Retornar apenas loterias ativas
            
        Returns:
            Lista de loterias
        """
        query = db.query(Lottery)
        if only_active:
            query = query.filter(Lottery.is_active == True)
        return query.all()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Lottery]:
        """
        Busca loteria por slug.
        
        Args:
            db: Sessão do banco
            slug: Identificador da loteria (ex: 'megasena')
            
        Returns:
            Loteria encontrada ou None
        """
        return db.query(Lottery).filter(Lottery.slug == slug).first()
    
    @staticmethod
    def get_by_id(db: Session, lottery_id: int) -> Optional[Lottery]:
        """
        Busca loteria por ID.
        
        Args:
            db: Sessão do banco
            lottery_id: ID da loteria
            
        Returns:
            Loteria encontrada ou None
        """
        return db.query(Lottery).filter(Lottery.id == lottery_id).first()
    
    @staticmethod
    def create(db: Session, lottery_data: LotteryCreate) -> Lottery:
        """
        Cria nova loteria.
        
        Args:
            db: Sessão do banco
            lottery_data: Dados da loteria
            
        Returns:
            Loteria criada
        """
        lottery = Lottery(**lottery_data.model_dump())
        db.add(lottery)
        db.commit()
        db.refresh(lottery)
        return lottery
    
    @staticmethod
    def ensure_lotteries_exist(db: Session) -> None:
        """
        Garante que as loterias base existem no banco.
        
        Cria Mega-Sena e Lotofácil se não existirem.
        
        Args:
            db: Sessão do banco
        """
        # Mega-Sena
        if not LotteryService.get_by_slug(db, "megasena"):
            megasena = Lottery(
                slug="megasena",
                name="Mega-Sena",
                total_numbers=60,
                draw_size=6,
                grid_rows=10,
                grid_cols=6,
                is_active=True,
            )
            db.add(megasena)
            print("✅ Criada loteria: Mega-Sena")
        
        # Lotofácil
        if not LotteryService.get_by_slug(db, "lotofacil"):
            lotofacil = Lottery(
                slug="lotofacil",
                name="Lotofácil",
                total_numbers=25,
                draw_size=15,
                grid_rows=5,
                grid_cols=5,
                is_active=True,
            )
            db.add(lotofacil)
            print("✅ Criada loteria: Lotofácil")
        
        db.commit()
    
    @staticmethod
    def get_stats(db: Session, slug: str) -> dict:
        """
        Estatísticas gerais de uma loteria.
        
        Args:
            db: Sessão do banco
            slug: Slug da loteria
            
        Returns:
            Dicionário com estatísticas
        """
        lottery = LotteryService.get_by_slug(db, slug)
        if not lottery:
            return {}
        
        # Contagem de sorteios
        total_draws = db.query(func.count(Draw.id)).filter(
            Draw.lottery_id == lottery.id
        ).scalar()
        
        # Último sorteio
        last_draw = db.query(Draw).filter(
            Draw.lottery_id == lottery.id
        ).order_by(Draw.contest_number.desc()).first()
        
        return {
            "lottery": {
                "slug": lottery.slug,
                "name": lottery.name,
                "total_numbers": lottery.total_numbers,
                "draw_size": lottery.draw_size,
            },
            "total_draws": total_draws or 0,
            "last_contest": last_draw.contest_number if last_draw else None,
            "last_draw_date": last_draw.draw_date.isoformat() if last_draw else None,
            "last_numbers": last_draw.numbers if last_draw else None,
        }
    
    @staticmethod
    def get_frequency(db: Session, slug: str) -> dict:
        """
        Frequência de números sorteados.
        
        Args:
            db: Sessão do banco
            slug: Slug da loteria
            
        Returns:
            Dicionário com frequência de cada número
        """
        lottery = LotteryService.get_by_slug(db, slug)
        if not lottery:
            return {}
        
        # Buscar todos os sorteios
        draws = db.query(Draw.numbers).filter(
            Draw.lottery_id == lottery.id
        ).all()
        
        # Contar frequência
        frequency = {}
        for i in range(1, lottery.total_numbers + 1):
            frequency[i] = 0
        
        for (numbers,) in draws:
            for num in numbers:
                if num in frequency:
                    frequency[num] += 1
        
        # Ordenar por frequência
        sorted_freq = sorted(
            frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "lottery": lottery.slug,
            "total_draws": len(draws),
            "frequency": [
                {"number": num, "count": count, "percentage": round(count / len(draws) * 100, 2) if draws else 0}
                for num, count in sorted_freq
            ]
        }
