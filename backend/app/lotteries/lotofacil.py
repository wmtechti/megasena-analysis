"""
Implementação da Lotofácil.

Grade 5×5 com numeração de 01 a 25.
"""

from typing import List, Tuple, Dict
import numpy as np
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
    
    def calculate_features(self, numbers: List[int]) -> Dict:
        """
        Calcula features espaciais e estatísticas dos números sorteados.
        
        Args:
            numbers: Lista de números sorteados
            
        Returns:
            Dict com features calculadas (mapeadas para colunas do modelo DrawFeature)
        """
        if not self.validate_numbers(numbers):
            raise ValueError(f"Números inválidos: {numbers}")
        
        # Converte números para posições
        positions = [self.num_to_pos(n) for n in numbers]
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        # Calcula distâncias entre todos os pares de números
        from scipy.spatial import distance
        import numpy as np
        
        coords = np.array(positions)
        distances = distance.pdist(coords, metric='euclidean')
        
        # Features básicas mapeadas para o modelo
        features = {
            # Distâncias
            'mean_distance': float(np.mean(distances)) if len(distances) > 0 else 0.0,
            'std_distance': float(np.std(distances)) if len(distances) > 0 else 0.0,
            'min_distance': float(np.min(distances)) if len(distances) > 0 else 0.0,
            'max_distance': float(np.max(distances)) if len(distances) > 0 else 0.0,
            
            # Posições
            'mean_row': float(np.mean(rows)),
            'std_row': float(np.std(rows)),
            'mean_col': float(np.mean(cols)),
            'std_col': float(np.std(cols)),
            'spread_row': int(max(rows) - min(rows)),
            'spread_col': int(max(cols) - min(cols)),
            
            # Distribuição espacial
            'count_top_half': sum(1 for r in rows if r < self.grid_rows / 2),
            'count_bottom_half': sum(1 for r in rows if r >= self.grid_rows / 2),
            'count_left_half': sum(1 for c in cols if c < self.grid_cols / 2),
            'count_right_half': sum(1 for c in cols if c >= self.grid_cols / 2),
            'count_border': sum(1 for pos in positions if self.is_border(pos[0], pos[1])),
        }
        
        # Features avançadas
        quadrants = self.get_quadrants()
        features['quadrant_q1'] = sum(1 for pos in positions if pos in quadrants['q1'])
        features['quadrant_q2'] = sum(1 for pos in positions if pos in quadrants['q2'])
        features['quadrant_q3'] = sum(1 for pos in positions if pos in quadrants['q3'])
        features['quadrant_q4'] = sum(1 for pos in positions if pos in quadrants['q4'])
        
        # Centróide e distância do centro
        centroid_row = np.mean(rows)
        centroid_col = np.mean(cols)
        center_row = self.grid_rows / 2 - 0.5
        center_col = self.grid_cols / 2 - 0.5
        features['centroid_distance'] = float(np.sqrt((centroid_row - center_row)**2 + (centroid_col - center_col)**2))
        
        # Features avançadas (simplificadas por ora, podem ser melhoradas depois)
        features['spatial_autocorr'] = 0.0  # TODO: Implementar I de Moran
        features['cluster_coefficient'] = 0.0  # TODO: Implementar clustering
        features['mean_nearest_neighbor'] = float(np.mean([np.min(distance.cdist([p], coords, metric='euclidean')[0][1:]) for p in coords])) if len(coords) > 1 else 0.0
        features['convex_hull_area'] = 0.0  # TODO: Implementar convex hull
        features['entropy_spatial'] = 0.0  # TODO: Implementar entropia
        features['dispersion_index'] = float(np.std(distances) / np.mean(distances)) if np.mean(distances) > 0 else 0.0
        features['pattern_regularity'] = 0.0  # TODO: Implementar regularidade
        
        return features


# Instância global (singleton pattern)
lotofacil = Lotofacil()
