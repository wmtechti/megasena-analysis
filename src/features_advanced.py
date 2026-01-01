"""
Módulo para features espaciais avançadas.

Implementa features de conectividade, simetria, adjacência e geometria.
"""

from typing import List, Tuple, Dict, Set
import numpy as np
from collections import deque

from .spatial import nums_to_positions, get_quadrant


def get_neighbors_4(row: int, col: int) -> List[Tuple[int, int]]:
    """
    Retorna vizinhos 4-conectados (Von Neumann) de uma posição.
    
    Args:
        row: Linha (0-9)
        col: Coluna (0-5)
        
    Returns:
        Lista de tuplas (row, col) dos vizinhos válidos
    """
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r <= 9 and 0 <= c <= 5:
            neighbors.append((r, c))
    return neighbors


def get_neighbors_8(row: int, col: int) -> List[Tuple[int, int]]:
    """
    Retorna vizinhos 8-conectados (Moore) de uma posição.
    
    Args:
        row: Linha (0-9)
        col: Coluna (0-5)
        
    Returns:
        Lista de tuplas (row, col) dos vizinhos válidos
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r <= 9 and 0 <= c <= 5:
                neighbors.append((r, c))
    return neighbors


def count_adjacencies_4(positions: List[Tuple[int, int]]) -> int:
    """
    Conta pares de posições adjacentes (4-conectadas).
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Número de pares adjacentes
    """
    pos_set = set(positions)
    count = 0
    
    for row, col in positions:
        neighbors = get_neighbors_4(row, col)
        for n_row, n_col in neighbors:
            if (n_row, n_col) in pos_set:
                count += 1
    
    # Divide por 2 porque cada par foi contado duas vezes
    return count // 2


def count_adjacencies_8(positions: List[Tuple[int, int]]) -> int:
    """
    Conta pares de posições adjacentes (8-conectadas).
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Número de pares adjacentes
    """
    pos_set = set(positions)
    count = 0
    
    for row, col in positions:
        neighbors = get_neighbors_8(row, col)
        for n_row, n_col in neighbors:
            if (n_row, n_col) in pos_set:
                count += 1
    
    return count // 2


def compute_connected_components_4(positions: List[Tuple[int, int]]) -> int:
    """
    Calcula número de componentes conexas (4-conectadas).
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Número de componentes conexas (1-6)
    """
    if not positions:
        return 0
    
    pos_set = set(positions)
    visited = set()
    components = 0
    
    for start_pos in positions:
        if start_pos in visited:
            continue
        
        # BFS para explorar componente
        queue = deque([start_pos])
        visited.add(start_pos)
        components += 1
        
        while queue:
            row, col = queue.popleft()
            neighbors = get_neighbors_4(row, col)
            
            for n_row, n_col in neighbors:
                neighbor = (n_row, n_col)
                if neighbor in pos_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    return components


def compute_connected_components_8(positions: List[Tuple[int, int]]) -> int:
    """
    Calcula número de componentes conexas (8-conectadas).
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Número de componentes conexas (1-6)
    """
    if not positions:
        return 0
    
    pos_set = set(positions)
    visited = set()
    components = 0
    
    for start_pos in positions:
        if start_pos in visited:
            continue
        
        queue = deque([start_pos])
        visited.add(start_pos)
        components += 1
        
        while queue:
            row, col = queue.popleft()
            neighbors = get_neighbors_8(row, col)
            
            for n_row, n_col in neighbors:
                neighbor = (n_row, n_col)
                if neighbor in pos_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    return components


def compute_inertia(positions: List[Tuple[int, int]]) -> float:
    """
    Calcula momento de inércia em torno do centroide.
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Momento de inércia
    """
    if not positions:
        return 0.0
    
    rows = [pos[0] for pos in positions]
    cols = [pos[1] for pos in positions]
    
    mean_row = np.mean(rows)
    mean_col = np.mean(cols)
    
    inertia = sum(
        (r - mean_row)**2 + (c - mean_col)**2
        for r, c in positions
    )
    
    return inertia


def compute_eccentricity(positions: List[Tuple[int, int]]) -> float:
    """
    Calcula excentricidade (razão aspectual).
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Razão σ_row / σ_col (com proteção para divisão por zero)
    """
    if len(positions) <= 1:
        return 1.0
    
    rows = [pos[0] for pos in positions]
    cols = [pos[1] for pos in positions]
    
    std_row = np.std(rows)
    std_col = np.std(cols)
    
    # Proteção para divisão por zero
    if std_col == 0:
        return float('inf') if std_row > 0 else 1.0
    
    return std_row / std_col


def compute_symmetry(positions: List[Tuple[int, int]]) -> Dict[str, int]:
    """
    Calcula medidas de simetria vertical e horizontal.
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Dicionário com simetrias vertical e horizontal
    """
    rows = [pos[0] for pos in positions]
    cols = [pos[1] for pos in positions]
    
    # Simetria horizontal (divide em row < 4.5 e row >= 4.5)
    upper = sum(1 for r in rows if r < 4.5)
    lower = sum(1 for r in rows if r >= 4.5)
    sym_horizontal = abs(upper - lower)
    
    # Simetria vertical (divide em col < 2.5 e col >= 2.5)
    left = sum(1 for c in cols if c < 2.5)
    right = sum(1 for c in cols if c >= 2.5)
    sym_vertical = abs(left - right)
    
    return {
        "symmetry_horizontal": sym_horizontal,
        "symmetry_vertical": sym_vertical
    }


def compute_ring_distribution(positions: List[Tuple[int, int]]) -> Dict[str, int]:
    """
    Calcula distribuição por anéis concêntricos a partir do centro.
    
    Centro do volante: (4.5, 2.5)
    Ring1: distância <= 2
    Ring2: 2 < distância <= 4
    Ring3: distância > 4
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Dicionário com contagens por anel
    """
    center_row, center_col = 4.5, 2.5
    
    rings = {"ring1": 0, "ring2": 0, "ring3": 0}
    
    for row, col in positions:
        distance = np.sqrt((row - center_row)**2 + (col - center_col)**2)
        
        if distance <= 2:
            rings["ring1"] += 1
        elif distance <= 4:
            rings["ring2"] += 1
        else:
            rings["ring3"] += 1
    
    return rings


def compute_compactness(positions: List[Tuple[int, int]]) -> float:
    """
    Calcula compacidade como razão área/perímetro.
    
    Aproximação simples: # células ocupadas / # células na borda do bounding box
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Medida de compacidade
    """
    if not positions:
        return 0.0
    
    rows = [pos[0] for pos in positions]
    cols = [pos[1] for pos in positions]
    
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    # Área do bounding box
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    # Perímetro
    perimeter = 2 * (height + width)
    
    # Compacidade
    if perimeter == 0:
        return 0.0
    
    return len(positions) / perimeter


def extract_advanced_features(numbers: List[int]) -> Dict[str, float]:
    """
    Extrai todas as features avançadas para um sorteio.
    
    Args:
        numbers: Lista com os 6 números sorteados
        
    Returns:
        Dicionário com features avançadas
    """
    positions = nums_to_positions(numbers)
    
    # Adjacências
    adj_4 = count_adjacencies_4(positions)
    adj_8 = count_adjacencies_8(positions)
    
    # Conectividade
    conn_4 = compute_connected_components_4(positions)
    conn_8 = compute_connected_components_8(positions)
    
    # Geometria
    inertia = compute_inertia(positions)
    eccentricity = compute_eccentricity(positions)
    compactness = compute_compactness(positions)
    
    # Simetria
    symmetry = compute_symmetry(positions)
    
    # Anéis
    rings = compute_ring_distribution(positions)
    
    # Combina tudo
    features = {
        "adjacencies_4": adj_4,
        "adjacencies_8": adj_8,
        "connectivity_4": conn_4,
        "connectivity_8": conn_8,
        "inertia": inertia,
        "eccentricity": eccentricity,
        "compactness": compactness,
        **symmetry,
        **rings
    }
    
    return features
