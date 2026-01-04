"""
Implementação da Mega-Sena.

Migrado do código original em src/spatial.py para nova arquitetura.
"""

from typing import List, Tuple
from app.lotteries.base import LotteryBase


class MegaSena(LotteryBase):
    """
    Loteria Mega-Sena.
    
    - 60 números (1-60)
    - Volante: 10 linhas × 6 colunas
    - Sorteio: 6 números
    """
    
    @property
    def slug(self) -> str:
        return "megasena"
    
    @property
    def name(self) -> str:
        return "Mega-Sena"
    
    @property
    def grid_rows(self) -> int:
        return 10
    
    @property
    def grid_cols(self) -> int:
        return 6
    
    @property
    def total_numbers(self) -> int:
        return 60
    
    @property
    def draw_size(self) -> int:
        return 6
    
    @property
    def min_number(self) -> int:
        return 1
    
    @property
    def max_number(self) -> int:
        return 60
    
    def num_to_pos(self, num: int) -> Tuple[int, int]:
        """
        Converte número (1-60) para posição no volante 10×6.
        
        Organização do volante:
        ```
        Col:   0    1    2    3    4    5
        Row:
         0 |  01   11   21   31   41   51
         1 |  02   12   22   32   42   52
         2 |  03   13   23   33   43   53
         3 |  04   14   24   34   44   54
         4 |  05   15   25   35   45   55
         5 |  06   16   26   36   46   56
         6 |  07   17   27   37   47   57
         7 |  08   18   28   38   48   58
         8 |  09   19   29   39   49   59
         9 |  10   20   30   40   50   60
        ```
        
        Args:
            num: Número entre 1 e 60
            
        Returns:
            Tupla (row, col) com índices 0-based
            
        Raises:
            ValueError: Se número fora do intervalo
            
        Examples:
            >>> megasena = MegaSena()
            >>> megasena.num_to_pos(1)
            (0, 0)
            >>> megasena.num_to_pos(60)
            (9, 5)
            >>> megasena.num_to_pos(23)
            (2, 2)
        """
        if not (1 <= num <= 60):
            raise ValueError(f"Número {num} fora do intervalo [1, 60]")
        
        col = (num - 1) // 10
        row = (num - 1) % 10
        
        return (row, col)
    
    def pos_to_num(self, row: int, col: int) -> int:
        """
        Converte posição (row, col) para número.
        
        Args:
            row: Linha (0-9)
            col: Coluna (0-5)
            
        Returns:
            Número entre 1 e 60
            
        Raises:
            ValueError: Se posição inválida
            
        Examples:
            >>> megasena = MegaSena()
            >>> megasena.pos_to_num(0, 0)
            1
            >>> megasena.pos_to_num(9, 5)
            60
            >>> megasena.pos_to_num(2, 2)
            23
        """
        if not (0 <= row < 10 and 0 <= col < 6):
            raise ValueError(f"Posição ({row}, {col}) inválida")
        
        num = col * 10 + row + 1
        
        return num


# Instância global (singleton pattern)
megasena = MegaSena()
