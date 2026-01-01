"""
Testes unitários para o módulo spatial.
"""

import pytest
import numpy as np
from src.spatial import (
    num_to_pos,
    pos_to_num,
    nums_to_positions,
    nums_to_binary_vector,
    get_quadrant,
    is_border,
    is_corner
)


class TestNumToPos:
    """Testes para conversão de número para posição."""
    
    def test_first_number(self):
        """Testa o primeiro número (1)."""
        assert num_to_pos(1) == (0, 0)
    
    def test_last_of_first_column(self):
        """Testa o último número da primeira coluna (10)."""
        assert num_to_pos(10) == (9, 0)
    
    def test_first_of_second_column(self):
        """Testa o primeiro número da segunda coluna (11)."""
        assert num_to_pos(11) == (0, 1)
    
    def test_last_number(self):
        """Testa o último número (60)."""
        assert num_to_pos(60) == (9, 5)
    
    def test_middle_number(self):
        """Testa um número no meio (35)."""
        assert num_to_pos(35) == (4, 3)
    
    def test_invalid_number_zero(self):
        """Testa número inválido (0)."""
        with pytest.raises(ValueError):
            num_to_pos(0)
    
    def test_invalid_number_negative(self):
        """Testa número negativo."""
        with pytest.raises(ValueError):
            num_to_pos(-5)
    
    def test_invalid_number_too_large(self):
        """Testa número maior que 60."""
        with pytest.raises(ValueError):
            num_to_pos(61)


class TestPosToNum:
    """Testes para conversão de posição para número."""
    
    def test_first_position(self):
        """Testa a primeira posição (0, 0)."""
        assert pos_to_num(0, 0) == 1
    
    def test_last_of_first_column(self):
        """Testa a última posição da primeira coluna."""
        assert pos_to_num(9, 0) == 10
    
    def test_first_of_second_column(self):
        """Testa a primeira posição da segunda coluna."""
        assert pos_to_num(0, 1) == 11
    
    def test_last_position(self):
        """Testa a última posição (9, 5)."""
        assert pos_to_num(9, 5) == 60
    
    def test_invalid_row_negative(self):
        """Testa row negativo."""
        with pytest.raises(ValueError):
            pos_to_num(-1, 0)
    
    def test_invalid_row_too_large(self):
        """Testa row maior que 9."""
        with pytest.raises(ValueError):
            pos_to_num(10, 0)
    
    def test_invalid_col_negative(self):
        """Testa col negativo."""
        with pytest.raises(ValueError):
            pos_to_num(0, -1)
    
    def test_invalid_col_too_large(self):
        """Testa col maior que 5."""
        with pytest.raises(ValueError):
            pos_to_num(0, 6)


class TestRoundTrip:
    """Testa conversão ida e volta."""
    
    def test_all_numbers(self):
        """Testa que todos os números fazem round-trip corretamente."""
        for num in range(1, 61):
            pos = num_to_pos(num)
            assert pos_to_num(*pos) == num


class TestNumsToPositions:
    """Testes para conversão de lista de números para posições."""
    
    def test_multiple_numbers(self):
        """Testa conversão de múltiplos números."""
        numbers = [1, 10, 20, 30, 40, 50]
        positions = nums_to_positions(numbers)
        
        assert len(positions) == 6
        assert positions[0] == (0, 0)  # 1
        assert positions[1] == (9, 0)  # 10
        assert positions[2] == (9, 1)  # 20
        assert positions[3] == (9, 2)  # 30
        assert positions[4] == (9, 3)  # 40
        assert positions[5] == (9, 4)  # 50


class TestNumsToBinaryVector:
    """Testes para conversão de números para vetor binário."""
    
    def test_single_number(self):
        """Testa vetor binário com um único número."""
        vec = nums_to_binary_vector([1])
        assert len(vec) == 60
        assert vec[0] == 1
        assert vec.sum() == 1
    
    def test_multiple_numbers(self):
        """Testa vetor binário com múltiplos números."""
        vec = nums_to_binary_vector([1, 10, 20, 30, 40, 50])
        assert len(vec) == 60
        assert vec[0] == 1   # 1
        assert vec[9] == 1   # 10
        assert vec[19] == 1  # 20
        assert vec[29] == 1  # 30
        assert vec[39] == 1  # 40
        assert vec[49] == 1  # 50
        assert vec.sum() == 6
    
    def test_invalid_number(self):
        """Testa número inválido."""
        with pytest.raises(ValueError):
            nums_to_binary_vector([61])
    
    def test_dtype(self):
        """Testa que o dtype é int8."""
        vec = nums_to_binary_vector([1, 2, 3, 4, 5, 6])
        assert vec.dtype == np.int8


class TestGetQuadrant:
    """Testes para determinação de quadrante."""
    
    def test_quadrant_1(self):
        """Testa quadrante 1 (superior esquerdo)."""
        assert get_quadrant(0, 0) == 0
        assert get_quadrant(4, 2) == 0
    
    def test_quadrant_2(self):
        """Testa quadrante 2 (superior direito)."""
        assert get_quadrant(0, 3) == 1
        assert get_quadrant(4, 5) == 1
    
    def test_quadrant_3(self):
        """Testa quadrante 3 (inferior esquerdo)."""
        assert get_quadrant(5, 0) == 2
        assert get_quadrant(9, 2) == 2
    
    def test_quadrant_4(self):
        """Testa quadrante 4 (inferior direito)."""
        assert get_quadrant(5, 3) == 3
        assert get_quadrant(9, 5) == 3


class TestIsBorder:
    """Testes para verificação de borda."""
    
    def test_top_border(self):
        """Testa borda superior."""
        assert is_border(0, 3) is True
    
    def test_bottom_border(self):
        """Testa borda inferior."""
        assert is_border(9, 3) is True
    
    def test_left_border(self):
        """Testa borda esquerda."""
        assert is_border(5, 0) is True
    
    def test_right_border(self):
        """Testa borda direita."""
        assert is_border(5, 5) is True
    
    def test_not_border(self):
        """Testa posição que não é borda."""
        assert is_border(5, 3) is False
        assert is_border(3, 2) is False


class TestIsCorner:
    """Testes para verificação de canto."""
    
    def test_top_left_corner(self):
        """Testa canto superior esquerdo."""
        assert is_corner(0, 0) is True
    
    def test_top_right_corner(self):
        """Testa canto superior direito."""
        assert is_corner(0, 5) is True
    
    def test_bottom_left_corner(self):
        """Testa canto inferior esquerdo."""
        assert is_corner(9, 0) is True
    
    def test_bottom_right_corner(self):
        """Testa canto inferior direito."""
        assert is_corner(9, 5) is True
    
    def test_not_corner(self):
        """Testa posições que não são cantos."""
        assert is_corner(0, 3) is False  # borda mas não canto
        assert is_corner(5, 0) is False  # borda mas não canto
        assert is_corner(5, 3) is False  # nem borda nem canto
