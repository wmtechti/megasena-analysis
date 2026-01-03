"""
Módulo para simulação Monte Carlo de sorteios aleatórios.

Gera baseline nulo para comparação estatística com dados observados.
"""

from typing import List, Tuple
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from .features import extract_features_for_draw
from .features_advanced import extract_advanced_features


def generate_random_draw(seed: int = None) -> List[int]:
    """
    Gera um sorteio aleatório de 6 números únicos entre 1 e 60.
    
    Args:
        seed: Seed para reprodutibilidade
        
    Returns:
        Lista com 6 números únicos sorteados aleatoriamente
    """
    if seed is not None:
        np.random.seed(seed)
    
    return sorted(np.random.choice(range(1, 61), size=6, replace=False).tolist())


def generate_random_draws(n_draws: int, seed: int = None) -> List[List[int]]:
    """
    Gera múltiplos sorteios aleatórios.
    
    Args:
        n_draws: Número de sorteios a gerar
        seed: Seed base para reprodutibilidade
        
    Returns:
        Lista de sorteios, cada um com 6 números
    """
    if seed is not None:
        np.random.seed(seed)
    
    draws = []
    for i in range(n_draws):
        draw = sorted(np.random.choice(range(1, 61), size=6, replace=False).tolist())
        draws.append(draw)
    
    return draws


def simulate_monte_carlo(
    n_simulations: int = 10000,
    n_draws_per_sim: int = 100,
    seed: int = 42,
    include_advanced: bool = True,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Executa simulação Monte Carlo completa.
    
    Gera n_simulations conjuntos de sorteios aleatórios, cada um com
    n_draws_per_sim sorteios. Calcula features para cada sorteio.
    
    Args:
        n_simulations: Número de simulações independentes
        n_draws_per_sim: Número de sorteios por simulação
        seed: Seed para reprodutibilidade
        include_advanced: Se True, inclui features avançadas
        verbose: Se True, exibe progresso
        
    Returns:
        DataFrame com todas as features de todos os sorteios simulados
    """
    np.random.seed(seed)
    
    all_features = []
    
    iterator = range(n_simulations)
    if verbose:
        iterator = tqdm(iterator, desc="Monte Carlo")
    
    for sim_id in iterator:
        # Gera sorteios para esta simulação
        draws = generate_random_draws(n_draws_per_sim, seed=seed + sim_id)
        
        # Calcula features para cada sorteio
        for draw_id, numbers in enumerate(draws):
            # Features básicas
            features = extract_features_for_draw(numbers)
            
            # Features avançadas
            if include_advanced:
                advanced = extract_advanced_features(numbers)
                features.update(advanced)
            
            # Adiciona metadados
            features["simulation_id"] = sim_id
            features["draw_id"] = draw_id
            
            all_features.append(features)
    
    # Converte para DataFrame
    df = pd.DataFrame(all_features)
    
    if verbose:
        print(f"\n✓ Simulação concluída:")
        print(f"  - {n_simulations} simulações")
        print(f"  - {n_draws_per_sim} sorteios por simulação")
        print(f"  - {len(df)} sorteios totais")
        print(f"  - {len([c for c in df.columns if c not in ['simulation_id', 'draw_id']])} features")
    
    return df


def compute_baseline_statistics(
    simulation_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula estatísticas do baseline Monte Carlo.
    
    Para cada feature, calcula:
    - Média das médias por simulação
    - Desvio padrão das médias
    - Percentis 2.5%, 50%, 97.5%
    
    Args:
        simulation_df: DataFrame com resultados da simulação
        
    Returns:
        DataFrame com estatísticas do baseline
    """
    # Remove colunas de metadados
    feature_cols = [
        col for col in simulation_df.columns
        if col not in ["simulation_id", "draw_id"]
    ]
    
    # Agrupa por simulação e calcula média (ignora NaN)
    sim_means = simulation_df.groupby("simulation_id")[feature_cols].mean()
    
    # Estatísticas do baseline (skipna=True para ignorar NaN)
    stats = pd.DataFrame({
        "mean": sim_means.mean(skipna=True),
        "std": sim_means.std(skipna=True),
        "percentile_2.5": sim_means.quantile(0.025),
        "percentile_50": sim_means.quantile(0.50),
        "percentile_97.5": sim_means.quantile(0.975),
        "min": sim_means.min(skipna=True),
        "max": sim_means.max(skipna=True)
    })
    
    # Substitui inf por NaN para evitar problemas
    stats = stats.replace([np.inf, -np.inf], np.nan)
    
    return stats


def save_simulation_results(
    simulation_df: pd.DataFrame,
    baseline_stats: pd.DataFrame,
    output_dir: str = "data/processed"
):
    """
    Salva resultados da simulação.
    
    Args:
        simulation_df: DataFrame com todas as features simuladas
        baseline_stats: DataFrame com estatísticas do baseline
        output_dir: Diretório para salvar arquivos
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Salva simulação completa (comprimido)
    sim_file = output_path / "monte_carlo_simulation.parquet"
    simulation_df.to_parquet(sim_file, index=False)
    print(f"✓ Simulação salva: {sim_file}")
    
    # Salva estatísticas do baseline
    stats_file = output_path / "baseline_statistics.parquet"
    baseline_stats.to_parquet(stats_file)
    print(f"✓ Estatísticas salvas: {stats_file}")


def load_baseline_statistics(
    file_path: str = "data/processed/baseline_statistics.parquet"
) -> pd.DataFrame:
    """
    Carrega estatísticas do baseline.
    
    Args:
        file_path: Caminho para o arquivo de estatísticas
        
    Returns:
        DataFrame com estatísticas do baseline
    """
    return pd.read_parquet(file_path)


def compare_with_baseline(
    observed_df: pd.DataFrame,
    baseline_stats: pd.DataFrame
) -> pd.DataFrame:
    """
    Compara features observadas com baseline Monte Carlo.
    
    Args:
        observed_df: DataFrame com features observadas
        baseline_stats: DataFrame com estatísticas do baseline
        
    Returns:
        DataFrame com comparações e flags de significância
    """
    # Remove colunas não-feature
    feature_cols = [
        col for col in observed_df.columns
        if col not in ["concurso", "data", "simulation_id", "draw_id"]
    ]
    
    # Calcula médias observadas
    observed_means = observed_df[feature_cols].mean()
    
    results = []
    
    for feature in feature_cols:
        obs_mean = observed_means[feature]
        baseline_mean = baseline_stats.loc[feature, "mean"]
        baseline_std = baseline_stats.loc[feature, "std"]
        ci_lower = baseline_stats.loc[feature, "percentile_2.5"]
        ci_upper = baseline_stats.loc[feature, "percentile_97.5"]
        
        # Calcula z-score (tamanho de efeito)
        if baseline_std > 0:
            z_score = (obs_mean - baseline_mean) / baseline_std
        else:
            z_score = 0
        
        # Verifica se está fora do IC 95%
        outside_ci = obs_mean < ci_lower or obs_mean > ci_upper
        
        results.append({
            "feature": feature,
            "observed_mean": obs_mean,
            "baseline_mean": baseline_mean,
            "baseline_std": baseline_std,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "z_score": z_score,
            "effect_size": abs(z_score),
            "outside_ci_95": outside_ci,
            "difference": obs_mean - baseline_mean,
            "difference_pct": ((obs_mean - baseline_mean) / baseline_mean * 100) if baseline_mean != 0 else 0
        })
    
    comparison_df = pd.DataFrame(results)
    
    # Ordena por tamanho de efeito
    comparison_df = comparison_df.sort_values("effect_size", ascending=False)
    
    return comparison_df
