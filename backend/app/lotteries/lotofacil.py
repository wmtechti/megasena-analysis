"""
Implementação da Lotofácil.

Grade 5×5 com numeração de 01 a 25.
"""

from typing import List, Tuple
from app.lotteries.base import LotteryBase


class Lotofacil(LotteryBase):
    """
    Loteria Lotofácil.
    
    - 25 números (1-25)
    - Volante: 5 linhas × 5 colunas
    - Sorteio: 15 números
    """
    
    @property
    def slug(self) -> str:
        return "lotofacil"
    
    @property
    def name(self) -> str:
        return "Lotofácil"
    
    @property
    def grid_rows(self) -> int:
        return 5
    
    @property
    def grid_cols(self) -> int:
        return 5
    
    @property
    def total_numbers(self) -> int:
        return 25
    
    @property
    def draw_size(self) -> int:
        return 15
    
    @property
    def min_number(self) -> int:
        return 1
    
    @property
    def max_number(self) -> int:
        return 25
    
    def num_to_pos(self, num: int) -> Tuple[int, int]:
        """
        Converte número (1-25) para posição no volante 5×5.
        
        Organização do volante:
        ```
        Col:   0    1    2    3    4
        Row:
         0 |  01   06   11   16   21
         1 |  02   07   12   17   22
         2 |  03   08   13   18   23
         3 |  04   09   14   19   24
         4 |  05   10   15   20   25
        ```
        
        Args:
            num: Número entre 1 e 25
            
        Returns:
            Tupla (row, col) com índices 0-based
            
        Raises:
            ValueError: Se número fora do intervalo
            
        Examples:
            >>> lotofacil = Lotofacil()
            >>> lotofacil.num_to_pos(1)
            (0, 0)
            >>> lotofacil.num_to_pos(25)
            (4, 4)
            >>> lotofacil.num_to_pos(13)
            (2, 2)
        """
        if not (1 <= num <= 25):
            raise ValueError(f"Número {num} fora do intervalo [1, 25]")
        
        col = (num - 1) // 5
        row = (num - 1) % 5
        
        return (row, col)
    
    def pos_to_num(self, row: int, col: int) -> int:
        """
        Converte posição (row, col) para número.
        
        Args:
            row: Linha (0-4)
            col: Coluna (0-4)
            
        Returns:
            Número entre 1 e 25
            
        Raises:
            ValueError: Se posição inválida
            
        Examples:
            >>> lotofacil = Lotofacil()
            >>> lotofacil.pos_to_num(0, 0)
            1
            >>> lotofacil.pos_to_num(4, 4)
            25
            >>> lotofacil.pos_to_num(2, 2)
            13
        """
        if not (0 <= row < 5 and 0 <= col < 5):
            raise ValueError(f"Posição ({row}, {col}) inválida")
        
        num = col * 5 + row + 1
        
        return num


# Instância global (singleton pattern)
lotofacil = Lotofacil()
