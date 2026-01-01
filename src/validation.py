"""
Módulo para validação estatística de features.

Implementa testes estatísticos, p-values e correção para múltiplas hipóteses.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
import json


def calculate_p_value_two_sided(
    observed_value: float,
    simulated_values: np.ndarray
) -> float:
    """
    Calcula p-value bilateral via Monte Carlo.
    
    Args:
        observed_value: Valor observado da feature
        simulated_values: Array com valores simulados
        
    Returns:
        P-value bilateral
    """
    n_sim = len(simulated_values)
    
    # Conta quantas simulações têm valor >= observado
    n_extreme_upper = np.sum(simulated_values >= observed_value)
    
    # Conta quantas simulações têm valor <= observado
    n_extreme_lower = np.sum(simulated_values <= observed_value)
    
    # P-value bilateral
    p_value = 2 * min(n_extreme_upper, n_extreme_lower) / n_sim
    
    # Garante que p-value esteja em [0, 1]
    return min(p_value, 1.0)


def benjamini_hochberg_correction(
    p_values: List[float],
    alpha: float = 0.05
) -> Tuple[List[bool], List[float]]:
    """
    Aplica correção FDR de Benjamini-Hochberg.
    
    Args:
        p_values: Lista de p-values
        alpha: Nível de significância
        
    Returns:
        Tupla (lista de booleanos indicando rejeição, p-values ajustados)
    """
    n = len(p_values)
    
    # Ordena p-values e guarda índices originais
    sorted_indices = np.argsort(p_values)
    sorted_p = np.array(p_values)[sorted_indices]
    
    # Calcula p-values ajustados
    adjusted_p = np.zeros(n)
    for i in range(n):
        adjusted_p[i] = min(sorted_p[i] * n / (i + 1), 1.0)
    
    # Garante monotonicidade
    for i in range(n - 2, -1, -1):
        adjusted_p[i] = min(adjusted_p[i], adjusted_p[i + 1])
    
    # Reordena para ordem original
    adjusted_p_original = np.zeros(n)
    adjusted_p_original[sorted_indices] = adjusted_p
    
    # Decisões de rejeição
    reject = adjusted_p_original < alpha
    
    return reject.tolist(), adjusted_p_original.tolist()


def bonferroni_correction(
    p_values: List[float],
    alpha: float = 0.05
) -> Tuple[List[bool], List[float]]:
    """
    Aplica correção de Bonferroni.
    
    Args:
        p_values: Lista de p-values
        alpha: Nível de significância
        
    Returns:
        Tupla (lista de booleanos indicando rejeição, p-values ajustados)
    """
    n = len(p_values)
    adjusted_p = [min(p * n, 1.0) for p in p_values]
    reject = [p < alpha for p in adjusted_p]
    
    return reject, adjusted_p


def validate_features(
    observed_df: pd.DataFrame,
    simulation_df: pd.DataFrame,
    alpha: float = 0.05,
    correction_method: str = "fdr"
) -> pd.DataFrame:
    """
    Executa validação estatística completa.
    
    Args:
        observed_df: DataFrame com features observadas
        simulation_df: DataFrame com features simuladas
        alpha: Nível de significância
        correction_method: Método de correção ("fdr", "bonferroni", "none")
        
    Returns:
        DataFrame com resultados da validação
    """
    # Identifica colunas de features
    feature_cols = [
        col for col in observed_df.columns
        if col not in ["concurso", "data", "simulation_id", "draw_id"]
    ]
    
    results = []
    p_values_list = []
    
    # Para cada feature, calcula estatísticas
    for feature in feature_cols:
        # Valores observados e simulados
        obs_values = observed_df[feature].values
        sim_values = simulation_df[feature].values
        
        # Médias
        obs_mean = np.mean(obs_values)
        sim_mean = np.mean(sim_values)
        sim_std = np.std(sim_values)
        
        # Calcula p-value via Monte Carlo
        # Agrupa simulações por simulation_id e calcula média de cada
        sim_means = simulation_df.groupby("simulation_id")[feature].mean().values
        p_value = calculate_p_value_two_sided(obs_mean, sim_means)
        p_values_list.append(p_value)
        
        # Z-score (tamanho de efeito)
        if sim_std > 0:
            z_score = (obs_mean - sim_mean) / sim_std
            effect_size = abs(z_score)
        else:
            z_score = 0
            effect_size = 0
        
        # Intervalo de confiança 95%
        ci_lower = np.percentile(sim_means, 2.5)
        ci_upper = np.percentile(sim_means, 97.5)
        outside_ci = obs_mean < ci_lower or obs_mean > ci_upper
        
        # Teste KS (Kolmogorov-Smirnov)
        ks_statistic, ks_p_value = stats.ks_2samp(obs_values, sim_values)
        
        # Teste Mann-Whitney U
        u_statistic, u_p_value = stats.mannwhitneyu(
            obs_values, sim_values, alternative='two-sided'
        )
        
        results.append({
            "feature": feature,
            "observed_mean": obs_mean,
            "observed_std": np.std(obs_values),
            "simulated_mean": sim_mean,
            "simulated_std": sim_std,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "difference": obs_mean - sim_mean,
            "difference_pct": ((obs_mean - sim_mean) / sim_mean * 100) if sim_mean != 0 else 0,
            "z_score": z_score,
            "effect_size": effect_size,
            "p_value": p_value,
            "outside_ci_95": outside_ci,
            "ks_statistic": ks_statistic,
            "ks_p_value": ks_p_value,
            "mann_whitney_u": u_statistic,
            "mann_whitney_p": u_p_value
        })
    
    validation_df = pd.DataFrame(results)
    
    # Aplica correção para múltiplas hipóteses
    if correction_method == "fdr":
        reject, adjusted_p = benjamini_hochberg_correction(p_values_list, alpha)
        correction_name = "FDR (Benjamini-Hochberg)"
    elif correction_method == "bonferroni":
        reject, adjusted_p = bonferroni_correction(p_values_list, alpha)
        correction_name = "Bonferroni"
    else:
        reject = [p < alpha for p in p_values_list]
        adjusted_p = p_values_list
        correction_name = "None"
    
    validation_df["p_value_adjusted"] = adjusted_p
    validation_df["significant"] = reject
    validation_df["correction_method"] = correction_name
    
    # Classifica tamanho de efeito
    validation_df["effect_interpretation"] = validation_df["effect_size"].apply(
        lambda x: "Large" if x >= 0.5 else ("Medium" if x >= 0.2 else "Small")
    )
    
    # Ordena por tamanho de efeito
    validation_df = validation_df.sort_values("effect_size", ascending=False)
    
    return validation_df


def summarize_validation(validation_df: pd.DataFrame) -> Dict:
    """
    Cria resumo executivo da validação.
    
    Args:
        validation_df: DataFrame com resultados da validação
        
    Returns:
        Dicionário com resumo
    """
    n_features = len(validation_df)
    n_significant = validation_df["significant"].sum()
    n_large_effect = (validation_df["effect_size"] >= 0.5).sum()
    n_medium_effect = ((validation_df["effect_size"] >= 0.2) & 
                       (validation_df["effect_size"] < 0.5)).sum()
    
    # Features significativas
    significant_features = validation_df[
        validation_df["significant"]
    ]["feature"].tolist()
    
    # Features com grande efeito
    large_effect_features = validation_df[
        validation_df["effect_size"] >= 0.5
    ]["feature"].tolist()
    
    summary = {
        "n_features_tested": n_features,
        "n_significant": n_significant,
        "n_large_effect": n_large_effect,
        "n_medium_effect": n_medium_effect,
        "correction_method": validation_df["correction_method"].iloc[0],
        "significant_features": significant_features,
        "large_effect_features": large_effect_features,
        "top_5_by_effect_size": validation_df.head(5)[[
            "feature", "effect_size", "p_value_adjusted", "significant"
        ]].to_dict("records")
    }
    
    return summary


def save_validation_results(
    validation_df: pd.DataFrame,
    summary: Dict,
    output_dir: str = "data/processed"
):
    """
    Salva resultados da validação.
    
    Args:
        validation_df: DataFrame com resultados detalhados
        summary: Dicionário com resumo
        output_dir: Diretório de saída
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Salva DataFrame completo
    validation_file = output_path / "validation_results.parquet"
    validation_df.to_parquet(validation_file, index=False)
    print(f"✓ Validação salva: {validation_file}")
    
    # Salva resumo em JSON
    summary_file = output_path / "validation_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"✓ Resumo salvo: {summary_file}")
    
    # Salva features significativas em CSV
    significant_df = validation_df[validation_df["significant"]]
    if len(significant_df) > 0:
        sig_file = output_path / "significant_features.csv"
        significant_df.to_csv(sig_file, index=False)
        print(f"✓ Features significativas salvas: {sig_file}")


def print_validation_report(validation_df: pd.DataFrame, summary: Dict):
    """
    Imprime relatório de validação no console.
    
    Args:
        validation_df: DataFrame com resultados
        summary: Dicionário com resumo
    """
    print("\n" + "=" * 80)
    print("RELATÓRIO DE VALIDAÇÃO ESTATÍSTICA")
    print("=" * 80)
    
    print(f"\nTotal de features testadas: {summary['n_features_tested']}")
    print(f"Features significativas: {summary['n_significant']} "
          f"({summary['n_significant']/summary['n_features_tested']*100:.1f}%)")
    print(f"Método de correção: {summary['correction_method']}")
    
    print(f"\nTamanho de efeito:")
    print(f"  - Grande (≥0.5): {summary['n_large_effect']}")
    print(f"  - Médio (0.2-0.5): {summary['n_medium_effect']}")
    
    if summary['n_significant'] > 0:
        print(f"\n{'Feature':<25} {'Effect':<8} {'P-value':<10} {'Significante'}")
        print("-" * 80)
        for feature in summary['top_5_by_effect_size']:
            sig = "✓" if feature['significant'] else "✗"
            print(f"{feature['feature']:<25} "
                  f"{feature['effect_size']:<8.3f} "
                  f"{feature['p_value_adjusted']:<10.4f} "
                  f"{sig}")
    else:
        print("\n⚠ Nenhuma feature significativa encontrada após correção.")
    
    print("\n" + "=" * 80)
