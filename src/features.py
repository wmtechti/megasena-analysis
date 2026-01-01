"""
Módulo para extração de features espaciais dos sorteios da Mega-Sena.

Gera features baseadas na distribuição espacial dos números no volante 10x6.
"""

from typing import List, Tuple, Dict
import numpy as np
import pandas as pd
from pathlib import Path

from .spatial import (
    nums_to_positions,
    nums_to_binary_vector,
    get_quadrant,
    is_border,
    is_corner
)


def compute_centroid(positions: List[Tuple[int, int]]) -> Tuple[float, float]:
    """
    Calcula o centroide (centro de massa) das posições.
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Tupla (mean_row, mean_col)
    """
    rows = [pos[0] for pos in positions]
    cols = [pos[1] for pos in positions]
    
    return (np.mean(rows), np.mean(cols))


def compute_dispersion(positions: List[Tuple[int, int]]) -> float:
    """
    Calcula a dispersão média usando distância Manhattan entre pares.
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Distância Manhattan média entre todos os pares
    """
    n = len(positions)
    if n <= 1:
        return 0.0
    
    total_distance = 0.0
    count = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            r1, c1 = positions[i]
            r2, c2 = positions[j]
            distance = abs(r1 - r2) + abs(c1 - c2)
            total_distance += distance
            count += 1
    
    return total_distance / count if count > 0 else 0.0


def compute_quadrant_counts(positions: List[Tuple[int, int]]) -> Dict[str, int]:
    """
    Conta quantas posições estão em cada quadrante.
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Dicionário com contagens por quadrante (q1, q2, q3, q4)
    """
    counts = {"q1": 0, "q2": 0, "q3": 0, "q4": 0}
    
    for row, col in positions:
        quad = get_quadrant(row, col)
        counts[f"q{quad + 1}"] += 1
    
    return counts


def compute_border_count(positions: List[Tuple[int, int]]) -> int:
    """
    Conta quantas posições estão na borda do volante.
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Número de posições na borda
    """
    return sum(1 for row, col in positions if is_border(row, col))


def compute_corner_count(positions: List[Tuple[int, int]]) -> int:
    """
    Conta quantas posições estão nos cantos do volante.
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Número de posições nos cantos
    """
    return sum(1 for row, col in positions if is_corner(row, col))


def compute_row_col_distribution(positions: List[Tuple[int, int]]) -> Dict[str, float]:
    """
    Calcula estatísticas da distribuição por linhas e colunas.
    
    Args:
        positions: Lista de tuplas (row, col)
        
    Returns:
        Dicionário com estatísticas de distribuição
    """
    rows = [pos[0] for pos in positions]
    cols = [pos[1] for pos in positions]
    
    return {
        "row_std": np.std(rows),
        "col_std": np.std(cols),
        "row_min": min(rows),
        "row_max": max(rows),
        "col_min": min(cols),
        "col_max": max(cols),
    }


def extract_features_for_draw(numbers: List[int]) -> Dict[str, float]:
    """
    Extrai todas as features espaciais para um sorteio.
    
    Args:
        numbers: Lista com os 6 números sorteados
        
    Returns:
        Dicionário com todas as features
    """
    # Converte números para posições
    positions = nums_to_positions(numbers)
    
    # Centroide
    centroid_row, centroid_col = compute_centroid(positions)
    
    # Dispersão
    dispersion = compute_dispersion(positions)
    
    # Quadrantes
    quadrant_counts = compute_quadrant_counts(positions)
    
    # Borda e cantos
    border_count = compute_border_count(positions)
    corner_count = compute_corner_count(positions)
    
    # Distribuição
    distribution = compute_row_col_distribution(positions)
    
    # Combina tudo
    features = {
        "centroid_row": centroid_row,
        "centroid_col": centroid_col,
        "dispersion": dispersion,
        "border_count": border_count,
        "corner_count": corner_count,
        **quadrant_counts,
        **distribution
    }
    
    return features


def build_features_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Constrói dataset completo de features para todos os concursos.
    
    Args:
        df: DataFrame com colunas concurso, data, bola_1, ..., bola_6
        
    Returns:
        DataFrame com features espaciais para cada concurso
    """
    features_list = []
    
    for idx, row in df.iterrows():
        # Extrai números do sorteio
        numbers = [row[f"bola_{i}"] for i in range(1, 7)]
        
        # Extrai features
        features = extract_features_for_draw(numbers)
        
        # Adiciona metadados
        features["concurso"] = row["concurso"]
        features["data"] = row["data"]
        
        features_list.append(features)
    
    # Cria DataFrame
    features_df = pd.DataFrame(features_list)
    
    # Reordena colunas
    cols = ["concurso", "data"] + [
        col for col in features_df.columns
        if col not in ["concurso", "data"]
    ]
    features_df = features_df[cols]
    
    print(f"✓ Features extraídas: {len(features_df)} concursos, {len(cols)-2} features")
    
    return features_df


def build_vectors_dataset(df: pd.DataFrame) -> np.ndarray:
    """
    Constrói dataset de vetores binários para todos os concursos.
    
    Args:
        df: DataFrame com colunas concurso, data, bola_1, ..., bola_6
        
    Returns:
        Array numpy com shape (n_concursos, 60)
    """
    vectors = []
    
    for idx, row in df.iterrows():
        numbers = [row[f"bola_{i}"] for i in range(1, 7)]
        vector = nums_to_binary_vector(numbers)
        vectors.append(vector)
    
    vectors_array = np.array(vectors, dtype=np.int8)
    
    print(f"✓ Vetores criados: shape {vectors_array.shape}")
    
    return vectors_array


def save_features(
    features_df: pd.DataFrame,
    vectors: np.ndarray,
    df_original: pd.DataFrame,
    features_path: str = "data/processed/draws_features.parquet",
    vectors_path: str = "data/processed/draws_vectors.npz"
):
    """
    Salva features em Parquet e vetores em NPZ.
    
    Args:
        features_df: DataFrame com features
        vectors: Array numpy com vetores binários
        df_original: DataFrame original com concursos
        features_path: Caminho para salvar features
        vectors_path: Caminho para salvar vetores
    """
    # Cria diretórios se necessário
    Path(features_path).parent.mkdir(parents=True, exist_ok=True)
    Path(vectors_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Salva features em Parquet
    features_df.to_parquet(features_path, index=False)
    print(f"✓ Features salvas em: {features_path}")
    
    # Salva vetores e metadados em NPZ
    concursos = df_original["concurso"].values
    np.savez_compressed(
        vectors_path,
        vectors=vectors,
        concursos=concursos
    )
    print(f"✓ Vetores salvos em: {vectors_path}")
