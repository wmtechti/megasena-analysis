"""
Módulo para visualizações da análise espacial.

Gera gráficos para heatmaps, distribuições, comparações e validações.
"""

from typing import List, Optional, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from .spatial import num_to_pos


def plot_heatmap_density(
    df: pd.DataFrame,
    title: str = "Densidade de Frequência no Volante",
    output_path: Optional[str] = None,
    show_numbers: bool = True
):
    """
    Cria heatmap de densidade de frequência das células.
    
    Args:
        df: DataFrame com colunas bola_1...bola_6
        title: Título do gráfico
        output_path: Caminho para salvar (opcional)
        show_numbers: Se True, mostra números nas células
    """
    # Matriz 10x6 para frequências
    freq_matrix = np.zeros((10, 6))
    
    # Conta frequências
    for _, row in df.iterrows():
        for i in range(1, 7):
            num = row[f"bola_{i}"]
            r, c = num_to_pos(num)
            freq_matrix[r, c] += 1
    
    # Normaliza (frequência relativa)
    freq_matrix /= len(df)
    
    # Cria figura
    fig, ax = plt.subplots(figsize=(10, 14))
    
    # Heatmap
    sns.heatmap(
        freq_matrix,
        annot=show_numbers,
        fmt='.3f',
        cmap='YlOrRd',
        cbar_kws={'label': 'Frequência Relativa'},
        linewidths=0.5,
        ax=ax
    )
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Coluna', fontsize=12)
    ax.set_ylabel('Linha', fontsize=12)
    
    # Adiciona linha horizontal mostrando frequência esperada
    expected_freq = 6 / 60
    ax.text(
        6.5, 5,
        f'Frequência esperada\n(uniforme): {expected_freq:.3f}',
        fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Heatmap salvo: {output_path}")
    
    plt.close()


def plot_dispersion_comparison(
    observed_df: pd.DataFrame,
    simulated_df: pd.DataFrame,
    title: str = "Distribuição de Dispersão: Observado vs Simulado",
    output_path: Optional[str] = None
):
    """
    Compara distribuição de dispersão observada vs simulada.
    
    Args:
        observed_df: DataFrame com features observadas
        simulated_df: DataFrame com features simuladas
        title: Título do gráfico
        output_path: Caminho para salvar (opcional)
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Histogramas
    ax.hist(
        simulated_df['dispersion'],
        bins=50,
        alpha=0.5,
        color='gray',
        label='Simulado (baseline)',
        density=True
    )
    
    ax.hist(
        observed_df['dispersion'],
        bins=30,
        alpha=0.7,
        color='steelblue',
        label='Observado',
        density=True
    )
    
    # Médias
    obs_mean = observed_df['dispersion'].mean()
    sim_mean = simulated_df['dispersion'].mean()
    
    ax.axvline(obs_mean, color='blue', linestyle='--', linewidth=2, label=f'Média obs: {obs_mean:.2f}')
    ax.axvline(sim_mean, color='red', linestyle='--', linewidth=2, label=f'Média sim: {sim_mean:.2f}')
    
    # IC 95%
    ci_lower = np.percentile(simulated_df.groupby('simulation_id')['dispersion'].mean(), 2.5)
    ci_upper = np.percentile(simulated_df.groupby('simulation_id')['dispersion'].mean(), 97.5)
    
    ax.axvspan(ci_lower, ci_upper, alpha=0.2, color='yellow', label=f'IC 95%: [{ci_lower:.2f}, {ci_upper:.2f}]')
    
    ax.set_xlabel('Dispersão (distância Manhattan média)', fontsize=12)
    ax.set_ylabel('Densidade', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico de dispersão salvo: {output_path}")
    
    plt.close()


def plot_centroid_scatter(
    df: pd.DataFrame,
    baseline_stats: Optional[pd.DataFrame] = None,
    title: str = "Distribuição de Centroides",
    output_path: Optional[str] = None
):
    """
    Scatter plot dos centroides de todos os sorteios.
    
    Args:
        df: DataFrame com features (centroid_row, centroid_col)
        baseline_stats: Estatísticas do baseline (opcional)
        title: Título do gráfico
        output_path: Caminho para salvar (opcional)
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Scatter dos centroides
    ax.scatter(
        df['centroid_col'],
        df['centroid_row'],
        alpha=0.3,
        s=20,
        c='steelblue',
        label='Concursos'
    )
    
    # Média observada
    mean_row = df['centroid_row'].mean()
    mean_col = df['centroid_col'].mean()
    
    ax.scatter(
        mean_col, mean_row,
        color='red',
        s=200,
        marker='X',
        edgecolors='black',
        linewidths=2,
        label=f'Média: ({mean_col:.2f}, {mean_row:.2f})',
        zorder=5
    )
    
    # Baseline (se fornecido)
    if baseline_stats is not None:
        baseline_row = baseline_stats.loc['centroid_row', 'mean']
        baseline_col = baseline_stats.loc['centroid_col', 'mean']
        
        ax.scatter(
            baseline_col, baseline_row,
            color='orange',
            s=200,
            marker='P',
            edgecolors='black',
            linewidths=2,
            label=f'Baseline: ({baseline_col:.2f}, {baseline_row:.2f})',
            zorder=5
        )
    
    # Centro teórico do volante
    ax.scatter(
        2.5, 4.5,
        color='green',
        s=200,
        marker='s',
        edgecolors='black',
        linewidths=2,
        label='Centro volante: (2.5, 4.5)',
        zorder=5
    )
    
    ax.set_xlabel('Centroid Col', fontsize=12)
    ax.set_ylabel('Centroid Row', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 9.5)
    ax.invert_yaxis()  # Inverte Y para corresponder ao volante
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Scatter de centroides salvo: {output_path}")
    
    plt.close()


def plot_feature_comparison(
    validation_df: pd.DataFrame,
    top_n: int = 15,
    title: str = "Comparação: Observado vs Baseline",
    output_path: Optional[str] = None
):
    """
    Gráfico de barras comparando features observadas vs baseline.
    
    Args:
        validation_df: DataFrame com resultados da validação
        top_n: Número de features a mostrar
        title: Título do gráfico
        output_path: Caminho para salvar (opcional)
    """
    # Seleciona top N por tamanho de efeito
    top_features = validation_df.nlargest(top_n, 'effect_size')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = np.arange(len(top_features))
    width = 0.35
    
    # Barras
    bars1 = ax.bar(
        x - width/2,
        top_features['observed_mean'],
        width,
        label='Observado',
        color='steelblue',
        alpha=0.8
    )
    
    bars2 = ax.bar(
        x + width/2,
        top_features['simulated_mean'],
        width,
        label='Baseline',
        color='orange',
        alpha=0.8
    )
    
    # Marca features significativas
    for i, (idx, row) in enumerate(top_features.iterrows()):
        if row['significant']:
            ax.text(
                i, max(row['observed_mean'], row['simulated_mean']) * 1.05,
                '★',
                ha='center',
                fontsize=16,
                color='red'
            )
    
    ax.set_xlabel('Feature', fontsize=12)
    ax.set_ylabel('Valor Médio', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(top_features['feature'], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Nota sobre significância
    ax.text(
        0.98, 0.98,
        '★ = Significativo (FDR < 0.05)',
        transform=ax.transAxes,
        ha='right',
        va='top',
        fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Comparação de features salva: {output_path}")
    
    plt.close()


def plot_effect_size_distribution(
    validation_df: pd.DataFrame,
    title: str = "Distribuição do Tamanho de Efeito",
    output_path: Optional[str] = None
):
    """
    Histograma do tamanho de efeito (effect size) das features.
    
    Args:
        validation_df: DataFrame com resultados da validação
        title: Título do gráfico
        output_path: Caminho para salvar (opcional)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Histograma
    ax.hist(
        validation_df['effect_size'],
        bins=30,
        color='steelblue',
        alpha=0.7,
        edgecolor='black'
    )
    
    # Linhas para classificação
    ax.axvline(0.2, color='orange', linestyle='--', linewidth=2, label='Efeito pequeno (0.2)')
    ax.axvline(0.5, color='red', linestyle='--', linewidth=2, label='Efeito grande (0.5)')
    
    ax.set_xlabel('Tamanho de Efeito (|z-score|)', fontsize=12)
    ax.set_ylabel('Frequência', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Estatísticas
    stats_text = (
        f"Média: {validation_df['effect_size'].mean():.3f}\n"
        f"Mediana: {validation_df['effect_size'].median():.3f}\n"
        f"Máximo: {validation_df['effect_size'].max():.3f}"
    )
    
    ax.text(
        0.98, 0.98,
        stats_text,
        transform=ax.transAxes,
        ha='right',
        va='top',
        fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Distribuição de effect size salva: {output_path}")
    
    plt.close()


def generate_all_visualizations(
    observed_df: pd.DataFrame,
    simulated_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    baseline_stats: pd.DataFrame,
    output_dir: str = "reports"
):
    """
    Gera todas as visualizações de uma vez.
    
    Args:
        observed_df: Features observadas
        simulated_df: Features simuladas
        validation_df: Resultados da validação
        baseline_stats: Estatísticas do baseline
        output_dir: Diretório de saída
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("\nGerando visualizações...")
    
    # 1. Heatmap de densidade
    plot_heatmap_density(
        observed_df,
        output_path=str(output_path / "heatmap_density.png")
    )
    
    # 2. Dispersão
    plot_dispersion_comparison(
        observed_df,
        simulated_df,
        output_path=str(output_path / "dispersion_comparison.png")
    )
    
    # 3. Centroides
    plot_centroid_scatter(
        observed_df,
        baseline_stats,
        output_path=str(output_path / "centroid_scatter.png")
    )
    
    # 4. Comparação de features
    plot_feature_comparison(
        validation_df,
        output_path=str(output_path / "feature_comparison.png")
    )
    
    # 5. Effect size
    plot_effect_size_distribution(
        validation_df,
        output_path=str(output_path / "effect_size_distribution.png")
    )
    
    print(f"\n✓ Todas as visualizações salvas em: {output_dir}/")
