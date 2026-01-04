"""
Script de teste das implementações de loteria.

Testa as classes MegaSena e Lotofacil sem necessidade de banco de dados.
"""

import sys
from pathlib import Path

# Adiciona backend ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.lotteries import megasena, lotofacil, list_lotteries


def test_megasena():
    """Testa implementação da Mega-Sena."""
    print("=" * 60)
    print("🎰 MEGA-SENA")
    print("=" * 60)
    
    print(f"Nome: {megasena.name}")
    print(f"Slug: {megasena.slug}")
    print(f"Grid: {megasena.grid_rows}x{megasena.grid_cols}")
    print(f"Total números: {megasena.total_numbers}")
    print(f"Tamanho sorteio: {megasena.draw_size}")
    
    print("\n📍 Testes de mapeamento:")
    test_cases = [1, 10, 11, 20, 23, 30, 50, 60]
    for num in test_cases:
        row, col = megasena.num_to_pos(num)
        back = megasena.pos_to_num(row, col)
        print(f"  {num:2d} → ({row}, {col}) → {back:2d} ✅" if back == num else f"  ERRO!")
    
    print("\n🎲 Validação de números:")
    valid = [1, 5, 12, 23, 45, 60]
    invalid_range = [0, 5, 12, 23, 45, 60]  # número 0 fora do range
    invalid_count = [1, 2, 3]  # apenas 3 números
    
    try:
        megasena.validate_numbers(valid)
        print(f"  {valid} → Válido ✅")
    except Exception as e:
        print(f"  ERRO: {e}")
    
    try:
        megasena.validate_numbers(invalid_count)
        print(f"  {invalid_count} → Deveria ter falhado!")
    except ValueError as e:
        print(f"  {invalid_count} → Inválido ✅ (quantidade errada)")
    
    try:
        megasena.validate_numbers(invalid_range)
        print(f"  {invalid_range} → Deveria ter falhado!")
    except ValueError as e:
        print(f"  {invalid_range} → Inválido ✅ (número 0 fora do range)")


def test_lotofacil():
    """Testa implementação da Lotofácil."""
    print("\n" + "=" * 60)
    print("🎰 LOTOFÁCIL")
    print("=" * 60)
    
    print(f"Nome: {lotofacil.name}")
    print(f"Slug: {lotofacil.slug}")
    print(f"Grid: {lotofacil.grid_rows}x{lotofacil.grid_cols}")
    print(f"Total números: {lotofacil.total_numbers}")
    print(f"Tamanho sorteio: {lotofacil.draw_size}")
    
    print("\n📍 Testes de mapeamento:")
    test_cases = [1, 5, 6, 10, 13, 15, 20, 25]
    for num in test_cases:
        row, col = lotofacil.num_to_pos(num)
        back = lotofacil.pos_to_num(row, col)
        print(f"  {num:2d} → ({row}, {col}) → {back:2d} ✅" if back == num else f"  ERRO!")


def test_neighbors():
    """Testa cálculo de vizinhos."""
    print("\n" + "=" * 60)
    print("👥 VIZINHOS (Mega-Sena número 23)")
    print("=" * 60)
    
    # Número 23 da Mega-Sena
    row, col = megasena.num_to_pos(23)
    neighbors_4 = megasena.get_neighbors_4(row, col)
    neighbors_8 = megasena.get_neighbors_8(row, col)
    
    print(f"Número 23 está em: ({row}, {col})")
    print(f"Vizinhos (4-conectados): {sorted(neighbors_4)}")
    print(f"Vizinhos (8-conectados): {sorted(neighbors_8)}")


def test_registry():
    """Testa registry de loterias."""
    print("\n" + "=" * 60)
    print("📋 REGISTRY DE LOTERIAS")
    print("=" * 60)
    
    lotteries = list_lotteries()
    for lottery in lotteries:
        print(f"\n{lottery['name']}:")
        print(f"  Slug: {lottery['slug']}")
        print(f"  Grid: {lottery['grid_rows']}x{lottery['grid_cols']}")
        print(f"  Números: {lottery['total_numbers']}")
        print(f"  Sorteio: {lottery['draw_size']} números")


if __name__ == "__main__":
    test_megasena()
    test_lotofacil()
    test_neighbors()
    test_registry()
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
