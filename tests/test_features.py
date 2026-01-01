"""
Testes unitários para o módulo features.
"""

import pytest
import numpy as np
from src.features import (
    compute_centroid,
    compute_dispersion,
    compute_quadrant_counts,
    compute_border_count,
    compute_corner_count,
    compute_row_col_distribution,
    extract_features_for_draw
)


class TestComputeCentroid:
    """Testes para cálculo do centroide."""
    
    def test_single_position(self):
        """Testa centroide de uma única posição."""
        positions = [(5, 3)]
        centroid = compute_centroid(positions)
        assert centroid == (5.0, 3.0)
    
    def test_two_positions(self):
        """Testa centroide de duas posições."""
        positions = [(0, 0), (4, 2)]
        centroid = compute_centroid(positions)
        assert centroid == (2.0, 1.0)
    
    def test_symmetric_positions(self):
        """Testa centroide de posições simétricas."""
        positions = [(0, 0), (9, 5)]
        centroid = compute_centroid(positions)
        assert centroid == (4.5, 2.5)


class TestComputeDispersion:
    """Testes para cálculo da dispersão."""
    
    def test_single_position(self):
        """Testa dispersão de uma única posição."""
        positions = [(5, 3)]
        dispersion = compute_dispersion(positions)
        assert dispersion == 0.0
    
    def test_two_adjacent_positions(self):
        """Testa dispersão de duas posições adjacentes."""
        positions = [(0, 0), (1, 0)]
        dispersion = compute_dispersion(positions)
        assert dispersion == 1.0
    
    def test_two_distant_positions(self):
        """Testa dispersão de duas posições distantes."""
        positions = [(0, 0), (9, 5)]
        dispersion = compute_dispersion(positions)
        assert dispersion == 14.0  # |9-0| + |5-0| = 14


class TestComputeQuadrantCounts:
    """Testes para contagem de quadrantes."""
    
    def test_all_in_q1(self):
        """Testa todas as posições no quadrante 1."""
        positions = [(0, 0), (1, 1), (2, 2)]
        counts = compute_quadrant_counts(positions)
        assert counts == {"q1": 3, "q2": 0, "q3": 0, "q4": 0}
    
    def test_distributed(self):
        """Testa posições distribuídas."""
        positions = [
            (0, 0),  # Q1
            (0, 5),  # Q2
            (9, 0),  # Q3
            (9, 5),  # Q4
        ]
        counts = compute_quadrant_counts(positions)
        assert counts == {"q1": 1, "q2": 1, "q3": 1, "q4": 1}


class TestComputeBorderCount:
    """Testes para contagem de bordas."""
    
    def test_no_border(self):
        """Testa posições sem borda."""
        positions = [(5, 3), (4, 2)]
        count = compute_border_count(positions)
        assert count == 0
    
    def test_all_border(self):
        """Testa todas as posições na borda."""
        positions = [(0, 3), (9, 3), (5, 0), (5, 5)]
        count = compute_border_count(positions)
        assert count == 4
    
    def test_mixed(self):
        """Testa posições mistas."""
        positions = [(0, 0), (5, 3), (9, 5)]
        count = compute_border_count(positions)
        assert count == 2  # (0,0) e (9,5) são bordas


class TestComputeCornerCount:
    """Testes para contagem de cantos."""
    
    def test_no_corner(self):
        """Testa posições sem canto."""
        positions = [(0, 3), (5, 3), (9, 3)]
        count = compute_corner_count(positions)
        assert count == 0
    
    def test_all_corners(self):
        """Testa todos os cantos."""
        positions = [(0, 0), (0, 5), (9, 0), (9, 5)]
        count = compute_corner_count(positions)
        assert count == 4
    
    def test_mixed(self):
        """Testa posições mistas."""
        positions = [(0, 0), (5, 3), (9, 5)]
        count = compute_corner_count(positions)
        assert count == 2


class TestComputeRowColDistribution:
    """Testes para estatísticas de distribuição."""
    
    def test_single_row_single_col(self):
        """Testa posições na mesma linha e coluna."""
        positions = [(5, 3), (5, 3)]
        dist = compute_row_col_distribution(positions)
        assert dist["row_std"] == 0.0
        assert dist["col_std"] == 0.0
        assert dist["row_min"] == 5
        assert dist["row_max"] == 5
        assert dist["col_min"] == 3
        assert dist["col_max"] == 3
    
    def test_varied_positions(self):
        """Testa posições variadas."""
        positions = [(0, 0), (9, 5)]
        dist = compute_row_col_distribution(positions)
        assert dist["row_min"] == 0
        assert dist["row_max"] == 9
        assert dist["col_min"] == 0
        assert dist["col_max"] == 5


class TestExtractFeaturesForDraw:
    """Testes para extração completa de features."""
    
    def test_extract_features(self):
        """Testa extração de features para um sorteio."""
        numbers = [1, 10, 20, 30, 40, 50]
        features = extract_features_for_draw(numbers)
        
        # Verifica que todas as features esperadas existem
        expected_keys = [
            "centroid_row", "centroid_col",
            "dispersion",
            "border_count", "corner_count",
            "q1", "q2", "q3", "q4",
            "row_std", "col_std",
            "row_min", "row_max",
            "col_min", "col_max"
        ]
        
        for key in expected_keys:
            assert key in features
        
        # Verifica que os valores são numéricos
        for key, value in features.items():
            assert isinstance(value, (int, float, np.integer, np.floating))
    
    def test_features_corner_numbers(self):
        """Testa features para números nos cantos."""
        numbers = [1, 10, 51, 60, 30, 31]  # Inclui os 4 cantos
        features = extract_features_for_draw(numbers)
        
        # Deve ter 4 cantos
        assert features["corner_count"] == 4
        
        # Todos os cantos são bordas
        assert features["border_count"] >= 4
