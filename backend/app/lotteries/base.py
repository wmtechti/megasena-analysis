"""
Classe abstrata para loterias.

Define interface comum que todas as loterias devem implementar.
Permite adicionar novas loterias facilmente mantendo consistência.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
import numpy as np


class LotteryBase(ABC):
    """
    Classe base abstrata para todas as loterias.
    
    Cada loteria (Mega-Sena, Lotofácil, etc.) deve herdar desta classe
    e implementar os métodos abstratos.
    """
    
    def __init__(self):
        """Inicializa a loteria."""
        self._validate_configuration()
    
    @property
    @abstractmethod
    def slug(self) -> str:
        """
        Identificador único da loteria (URL-friendly).
        
        Exemplos: 'megasena', 'lotofacil', 'quina'
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nome completo da loteria.
        
        Exemplos: 'Mega-Sena', 'Lotofácil', 'Quina'
        """
        pass
    
    @property
    @abstractmethod
    def grid_rows(self) -> int:
        """Número de linhas do volante."""
        pass
    
    @property
    @abstractmethod
    def grid_cols(self) -> int:
        """Número de colunas do volante."""
        pass
    
    @property
    @abstractmethod
    def total_numbers(self) -> int:
        """Total de números disponíveis (ex: 60 para Mega-Sena)."""
        pass
    
    @property
    @abstractmethod
    def draw_size(self) -> int:
        """Quantos números são sorteados (ex: 6 para Mega-Sena)."""
        pass
    
    @property
    @abstractmethod
    def min_number(self) -> int:
        """Menor número possível (geralmente 1)."""
        pass
    
    @property
    @abstractmethod
    def max_number(self) -> int:
        """Maior número possível (ex: 60 para Mega-Sena)."""
        pass
    
    # =========================================================================
    # Métodos Abstratos - Cada loteria deve implementar
    # =========================================================================
    
    @abstractmethod
    def num_to_pos(self, num: int) -> Tuple[int, int]:
        """
        Converte número para posição (row, col) no volante.
        
        Args:
            num: Número da loteria (ex: 1-60 para Mega-Sena)
            
        Returns:
            Tuple (row, col) com índices base-0
            
        Example:
            >>> lottery.num_to_pos(1)
            (0, 0)
        """
        pass
    
    @abstractmethod
    def pos_to_num(self, row: int, col: int) -> int:
        """
        Converte posição (row, col) para número.
        
        Args:
            row: Linha (0-indexed)
            col: Coluna (0-indexed)
            
        Returns:
            Número correspondente
            
        Example:
            >>> lottery.pos_to_num(0, 0)
            1
        """
        pass
    
    # =========================================================================
    # Métodos Implementados - Reutilizáveis por todas as loterias
    # =========================================================================
    
    def validate_numbers(self, numbers: List[int]) -> bool:
        """
        Valida se os números são válidos para esta loteria.
        
        Args:
            numbers: Lista de números
            
        Returns:
            True se válidos, False caso contrário
        """
        if not numbers:
            return False
        
        if len(numbers) != self.draw_size:
            return False
        
        if len(set(numbers)) != len(numbers):
            return False  # Números duplicados
        
        if not all(self.min_number <= n <= self.max_number for n in numbers):
            return False
        
        return True
    
    def get_neighbors_4(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Retorna vizinhos 4-conectados (cima, baixo, esquerda, direita).
        
        Args:
            row: Linha
            col: Coluna
            
        Returns:
            Lista de tuplas (row, col) dos vizinhos válidos
        """
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.grid_rows and 0 <= nc < self.grid_cols:
                neighbors.append((nr, nc))
        
        return neighbors
    
    def get_neighbors_8(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Retorna vizinhos 8-conectados (inclui diagonais).
        
        Args:
            row: Linha
            col: Coluna
            
        Returns:
            Lista de tuplas (row, col) dos vizinhos válidos
        """
        neighbors = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.grid_rows and 0 <= nc < self.grid_cols:
                neighbors.append((nr, nc))
        
        return neighbors
    
    def get_quadrants(self) -> Dict[str, List[Tuple[int, int]]]:
        """
        Divide o volante em 4 quadrantes.
        
        Returns:
            Dict com chaves 'q1', 'q2', 'q3', 'q4' contendo lista de posições
        """
        mid_row = self.grid_rows // 2
        mid_col = self.grid_cols // 2
        
        quadrants = {
            'q1': [],  # Superior esquerdo
            'q2': [],  # Superior direito
            'q3': [],  # Inferior esquerdo
            'q4': []   # Inferior direito
        }
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if row < mid_row and col < mid_col:
                    quadrants['q1'].append((row, col))
                elif row < mid_row and col >= mid_col:
                    quadrants['q2'].append((row, col))
                elif row >= mid_row and col < mid_col:
                    quadrants['q3'].append((row, col))
                else:
                    quadrants['q4'].append((row, col))
        
        return quadrants
    
    def is_border(self, row: int, col: int) -> bool:
        """
        Verifica se posição está na borda do volante.
        
        Args:
            row: Linha
            col: Coluna
            
        Returns:
            True se está na borda
        """
        return (
            row == 0 or row == self.grid_rows - 1 or
            col == 0 or col == self.grid_cols - 1
        )
    
    def is_corner(self, row: int, col: int) -> bool:
        """
        Verifica se posição está em um canto do volante.
        
        Args:
            row: Linha
            col: Coluna
            
        Returns:
            True se está em um canto
        """
        corners = [
            (0, 0),
            (0, self.grid_cols - 1),
            (self.grid_rows - 1, 0),
            (self.grid_rows - 1, self.grid_cols - 1)
        ]
        return (row, col) in corners
    
    def _validate_configuration(self) -> None:
        """
        Valida a configuração da loteria.
        
        Raises:
            ValueError: Se configuração inválida
        """
        if self.grid_rows <= 0 or self.grid_cols <= 0:
            raise ValueError("Dimensões do grid devem ser positivas")
        
        if self.total_numbers != self.grid_rows * self.grid_cols:
            raise ValueError(
                f"total_numbers ({self.total_numbers}) deve ser igual a "
                f"grid_rows * grid_cols ({self.grid_rows * self.grid_cols})"
            )
        
        if self.draw_size <= 0 or self.draw_size > self.total_numbers:
            raise ValueError(
                f"draw_size ({self.draw_size}) inválido para "
                f"{self.total_numbers} números"
            )
        
        if self.min_number < 1:
            raise ValueError("min_number deve ser >= 1")
        
        if self.max_number != self.total_numbers:
            raise ValueError(
                f"max_number ({self.max_number}) deve ser igual a "
                f"total_numbers ({self.total_numbers})"
            )
    
    def __repr__(self) -> str:
        """Representação string da loteria."""
        return (
            f"{self.__class__.__name__}("
            f"slug='{self.slug}', "
            f"grid={self.grid_rows}x{self.grid_cols}, "
            f"draw_size={self.draw_size})"
        )
