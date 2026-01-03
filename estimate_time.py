"""
Script para estimar tempo de execução da simulação Monte Carlo e validação estatística.

Executa uma amostra pequena e extrapola para o número total de simulações.
"""

import time
import argparse
from pathlib import Path
import sys

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.monte_carlo import simulate_monte_carlo
from src.ingest import ingest_raw_data
from src.features import build_features_dataset
from src.features_advanced import extract_advanced_features
from src.validation import validate_features
import pandas as pd


def format_time(seconds: float) -> str:
    """
    Formata tempo em segundos para formato legível.
    
    Args:
        seconds: Tempo em segundos
        
    Returns:
        String formatada (ex: "2h 15min 30s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}min")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def estimate_monte_carlo_time(
    n_simulations: int = 10000,
    sample_size: int = 10,
    input_path: str = "data/raw/Mega-Sena.xlsx",
    include_validation: bool = True
):
    """
    Estima tempo de execução da simulação Monte Carlo e validação estatística.
    
    Args:
        n_simulations: Número total de simulações desejadas
        sample_size: Tamanho da amostra para teste
        input_path: Caminho para o arquivo de dados
        include_validation: Se True, inclui estimativa de validação
    """
    print("=" * 70)
    print("ESTIMATIVA DE TEMPO - PIPELINE COMPLETO")
    print("=" * 70)
    
    # Carrega dados para determinar n_draws
    print(f"\nCarregando dados de: {input_path}")
    try:
        df = ingest_raw_data(input_path)
        n_draws = len(df)
        print(f"✓ {n_draws} concursos carregados")
    except Exception as e:
        print(f"✗ Erro ao carregar dados: {e}")
        return
    
    print(f"\nParâmetros:")
    print(f"  - Simulações totais: {n_simulations:,}")
    print(f"  - Sorteios por simulação: {n_draws:,}")
    print(f"  - Total de sorteios: {n_simulations * n_draws:,}")
    print(f"  - Amostra de teste: {sample_size} simulações")
    if include_validation:
        print(f"  - Incluir validação estatística: Sim")
    else:
        print(f"  - Incluir validação estatística: Não")
    
    # Executa amostra de simulação
    print(f"\n{'─' * 70}")
    print(f"Executando amostra de {sample_size} simulações...")
    print(f"{'─' * 70}")
    
    start_time = time.time()
    
    try:
        simulate_monte_carlo(
            n_simulations=sample_size,
            n_draws_per_sim=n_draws,
            seed=42,
            include_advanced=True,
            verbose=True
        )
    except KeyboardInterrupt:
        print("\n\n⚠ Teste interrompido pelo usuário")
        return
    except Exception as e:
        print(f"\n✗ Erro durante teste: {e}")
        return
    
    elapsed_simulation = time.time() - start_time
    
    # Calcula estimativas de simulação
    time_per_simulation = elapsed_simulation / sample_size
    estimated_simulation_total = time_per_simulation * n_simulations
    
    # Estima tempo de validação estatística
    estimated_validation_total = 0
    if include_validation:
        print(f"\n{'─' * 70}")
        print("Estimando tempo de validação estatística...")
        print(f"{'─' * 70}")
        
        start_validation = time.time()
        
        try:
            # Gera features observadas (pequena amostra)
            print("Gerando features observadas...")
            features_df = build_features_dataset(df.head(100))
            
            advanced_list = []
            for _, row in df.head(100).iterrows():
                numbers = [row[f"bola_{i}"] for i in range(1, 7)]
                advanced = extract_advanced_features(numbers)
                advanced["concurso"] = row["concurso"]
                advanced_list.append(advanced)
            
            advanced_df = pd.DataFrame(advanced_list)
            features_df = features_df.merge(advanced_df, on="concurso")
            
            # Simula para validação
            print("Simulando para validação...")
            sim_df = simulate_monte_carlo(
                n_simulations=sample_size,
                n_draws_per_sim=100,
                seed=42,
                include_advanced=True,
                verbose=False
            )
            
            # Executa validação
            print("Executando validação...")
            validate_features(features_df, sim_df, correction_method="fdr")
            
            validation_time = time.time() - start_validation
            
            # Estima tempo total de validação
            # Validação escala aproximadamente linear com número de features
            validation_factor = len(df) / 100  # Ajusta para dataset completo
            estimated_validation_total = validation_time * validation_factor
            
            print(f"✓ Validação de amostra concluída em {format_time(validation_time)}")
            
        except Exception as e:
            print(f"⚠ Não foi possível estimar validação: {e}")
            estimated_validation_total = 0
    
    # Total
    estimated_total = estimated_simulation_total + estimated_validation_total
    
    print(f"\n{'═' * 70}")
    print("RESULTADOS DA ESTIMATIVA")
    print(f"{'═' * 70}")
    
    print(f"\n📊 Tempo da amostra (simulação):")
    print(f"   {format_time(elapsed_simulation)} ({elapsed_simulation:.2f}s)")
    
    print(f"\n⚡ Tempo médio por simulação:")
    print(f"   {time_per_simulation:.3f}s")
    
    print(f"\n⏱️  Tempo estimado total - SIMULAÇÃO:")
    print(f"   {format_time(estimated_simulation_total)}")
    print(f"   ({estimated_simulation_total:.2f}s)")
    
    if include_validation and estimated_validation_total > 0:
        print(f"\n⏱️  Tempo estimado - VALIDAÇÃO ESTATÍSTICA:")
        print(f"   {format_time(estimated_validation_total)}")
        print(f"   ({estimated_validation_total:.2f}s)")
        
        print(f"\n⏱️  TEMPO TOTAL ESTIMADO (Simulação + Validação):")
        print(f"   {format_time(estimated_total)}")
        print(f"   ({estimated_total:.2f}s)")
    else:
        print(f"\n⏱️  Tempo estimado total ({n_simulations:,} simulações):")
        print(f"   {format_time(estimated_total)}")
        print(f"   ({estimated_total:.2f}s)")
    
    # Estimativas em diferentes escalas
    print(f"\n📈 Estimativas para diferentes quantidades:")
    print(f"{'─' * 70}")
    
    if include_validation and estimated_validation_total > 0:
        print(f"{'Simulações':>15} | {'Simulação':>18} | {'Validação':>18} | {'Total':>18}")
        print(f"{'─' * 70}")
        
        for n_sim in [100, 500, 1000, 5000, 10000, 50000]:
            est_sim = time_per_simulation * n_sim
            # Validação não escala com n_simulations, apenas com dataset
            est_val = estimated_validation_total
            est_total = est_sim + est_val
            print(f"{n_sim:>15,} | {format_time(est_sim):>18} | {format_time(est_val):>18} | {format_time(est_total):>18}")
    else:
        print(f"{'Simulações':>15} | {'Tempo Estimado':>20} | {'Sorteios Totais':>20}")
        print(f"{'─' * 70}")
        
        for n_sim in [100, 500, 1000, 5000, 10000, 50000]:
            est_time = time_per_simulation * n_sim
            total_draws = n_sim * n_draws
            print(f"{n_sim:>15,} | {format_time(est_time):>20} | {total_draws:>20,}")
    
    print(f"{'─' * 70}")
    
    # Recomendações
    print(f"\n💡 Recomendações:")
    
    if estimated_total < 60:  # < 1 minuto
        print(f"   ✓ Tempo muito rápido - pode aumentar n_simulations")
    elif estimated_total < 600:  # < 10 minutos
        print(f"   ✓ Tempo razoável para execução local")
    elif estimated_total < 3600:  # < 1 hora
        print(f"   ⚠ Tempo moderado - considere executar em background")
    elif estimated_total < 14400:  # < 4 horas
        print(f"   ⚠ Tempo longo - execute overnight ou em servidor")
    else:
        print(f"   ⚠ Tempo muito longo - considere reduzir n_simulations")
        recommended = int(3600 / time_per_simulation)
        print(f"   💡 Sugestão: {recommended:,} simulações (~1 hora)")
    
    print(f"\n{'═' * 70}")
    print(f"Para executar a simulação completa, use:")
    print(f"  python -m src.pipeline simulate --n-simulations {n_simulations}")
    if include_validation:
        print(f"  python -m src.pipeline validate --correction fdr")
    print(f"{'═' * 70}\n")


def main():
    """Entry point do script."""
    parser = argparse.ArgumentParser(
        description="Estima tempo de execução da simulação Monte Carlo e validação estatística"
    )
    
    parser.add_argument(
        "--n-simulations", "-n",
        type=int,
        default=10000,
        help="Número total de simulações desejadas (padrão: 10000)"
    )
    
    parser.add_argument(
        "--sample-size", "-s",
        type=int,
        default=10,
        help="Tamanho da amostra para teste (padrão: 10)"
    )
    
    parser.add_argument(
        "--input", "-i",
        type=str,
        default="data/raw/Mega-Sena.xlsx",
        help="Caminho para o arquivo Excel (padrão: data/raw/Mega-Sena.xlsx)"
    )
    
    parser.add_argument(
        "--no-validation",
        action="store_true",
        help="Não incluir estimativa de validação estatística"
    )
    
    args = parser.parse_args()
    
    estimate_monte_carlo_time(
        n_simulations=args.n_simulations,
        sample_size=args.sample_size,
        input_path=args.input,
        include_validation=not args.no_validation
    )


if __name__ == "__main__":
    main()
