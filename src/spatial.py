"""
Módulo para mapeamento espacial do volante da Mega-Sena.

O volante da Mega-Sena é organizado em uma grade 10x6:
- 10 linhas (rows)
- 6 colunas (cols)
- Números de 1 a 60

Mapeamento:
- Coluna 0: números 1-10
- Coluna 1: números 11-20
- Coluna 2: números 21-30
- Coluna 3: números 31-40
- Coluna 4: números 41-50
- Coluna 5: números 51-60
"""

from typing import Tuple, List
import numpy as np


def num_to_pos(num: int) -> Tuple[int, int]:
    """
    Converte um número da Mega-Sena (1-60) para posição (row, col) no volante.
    
    Args:
        num: Número entre 1 e 60
        
    Returns:
        Tupla (row, col) onde:
        - row: linha de 0 a 9
        - col: coluna de 0 a 5
        
    Raises:
        ValueError: Se o número não estiver entre 1 e 60
        
    Examples:
        >>> num_to_pos(1)
        (0, 0)
        >>> num_to_pos(10)
        (9, 0)
        >>> num_to_pos(11)
        (0, 1)
        >>> num_to_pos(60)
        (9, 5)
    """
    if not 1 <= num <= 60:
        raise ValueError(f"Número deve estar entre 1 e 60, recebido: {num}")
    
    # Ajusta para índice 0-based
    num_idx = num - 1
    
    # Calcula coluna e linha
    col = num_idx // 10
    row = num_idx % 10
    
    return (row, col)


def pos_to_num(row: int, col: int) -> int:
    """
    Converte uma posição (row, col) do volante para o número correspondente.
    
    Args:
        row: Linha de 0 a 9
        col: Coluna de 0 a 5
        
    Returns:
        Número entre 1 e 60
        
    Raises:
        ValueError: Se row ou col estiverem fora do intervalo válido
        
    Examples:
        >>> pos_to_num(0, 0)
        1
        >>> pos_to_num(9, 0)
        10
        >>> pos_to_num(0, 1)
        11
        >>> pos_to_num(9, 5)
        60
    """
    if not 0 <= row <= 9:
        raise ValueError(f"Row deve estar entre 0 e 9, recebido: {row}")
    if not 0 <= col <= 5:
        raise ValueError(f"Col deve estar entre 0 e 5, recebido: {col}")
    
    return col * 10 + row + 1


def nums_to_positions(nums: List[int]) -> List[Tuple[int, int]]:
    """
    Converte uma lista de números para lista de posições.
    
    Args:
        nums: Lista de números entre 1 e 60
        
    Returns:
        Lista de tuplas (row, col)
    """
    return [num_to_pos(num) for num in nums]


def nums_to_binary_vector(nums: List[int]) -> np.ndarray:
    """
    Converte uma lista de números em vetor binário de 60 posições.
    
    Args:
        nums: Lista de números entre 1 e 60
        
    Returns:
        Array numpy de 60 posições com 1 onde o número saiu e 0 caso contrário
        
    Examples:
        >>> vec = nums_to_binary_vector([1, 10, 20, 30, 40, 50])
        >>> vec[0], vec[9], vec[19]
        (1, 1, 1)
        >>> vec[1], vec[2], vec[3]
        (0, 0, 0)
    """
    vector = np.zeros(60, dtype=np.int8)
    for num in nums:
        if not 1 <= num <= 60:
            raise ValueError(f"Número deve estar entre 1 e 60, recebido: {num}")
        vector[num - 1] = 1
    return vector


def get_quadrant(row: int, col: int) -> int:
    """
    Determina o quadrante de uma posição no volante.
    
    Quadrantes (divididos em 4 partes):
    - Q1 (0): rows 0-4, cols 0-2
    - Q2 (1): rows 0-4, cols 3-5
    - Q3 (2): rows 5-9, cols 0-2
    - Q4 (3): rows 5-9, cols 3-5
    
    Args:
        row: Linha de 0 a 9
        col: Coluna de 0 a 5
        
    Returns:
        Número do quadrante (0-3)
    """
    row_half = 0 if row < 5 else 1
    col_half = 0 if col < 3 else 1
    return row_half * 2 + col_half


def is_border(row: int, col: int) -> bool:
    """
    Verifica se uma posição está na borda do volante.
    
    Args:
        row: Linha de 0 a 9
        col: Coluna de 0 a 5
        
    Returns:
        True se está na borda, False caso contrário
    """
    return row == 0 or row == 9 or col == 0 or col == 5


def is_corner(row: int, col: int) -> bool:
    """
    Verifica se uma posição está em um canto do volante.
    
    Args:
        row: Linha de 0 a 9
        col: Coluna de 0 a 5
        
    Returns:
        True se está em um canto, False caso contrário
    """
    return (row == 0 or row == 9) and (col == 0 or col == 5)
