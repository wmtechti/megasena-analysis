"""
Interface de linha de comando (CLI) para o pipeline de análise da Mega-Sena.

Comandos disponíveis:
- ingest: Carrega e valida os dados brutos
- build-features: Gera features espaciais e vetores
- simulate: Executa simulação Monte Carlo
- validate: Valida features contra baseline
- visualize: Gera visualizações
- run-all: Executa pipeline completo
"""

from pathlib import Path
import typer
from typing import Optional
import pandas as pd

from .ingest import ingest_raw_data, validate_data_integrity
from .features import (
    build_features_dataset,
    build_vectors_dataset,
    save_features
)
from .features_advanced import extract_advanced_features
from .monte_carlo import (
    simulate_monte_carlo,
    compute_baseline_statistics,
    save_simulation_results,
    load_baseline_statistics,
    compare_with_baseline
)
from .validation import (
    validate_features,
    summarize_validation,
    save_validation_results,
    print_validation_report
)
from .visualization import generate_all_visualizations


app = typer.Typer(
    help="Pipeline de análise espacial da Mega-Sena",
    add_completion=False
)


@app.command()
def ingest(
    input_path: str = typer.Option(
        "data/raw/Mega-Sena.xlsx",
        "--input", "-i",
        help="Caminho para o arquivo Excel da Mega-Sena"
    ),
    validate: bool = typer.Option(
        True,
        "--validate/--no-validate",
        help="Executar validação de integridade"
    )
):
    """
    Carrega e valida os dados brutos da Mega-Sena.
    
    Este comando:
    1. Lê o arquivo Excel
    2. Valida o formato e integridade dos dados
    3. Exibe estatísticas básicas
    """
    typer.echo("=" * 60)
    typer.echo("INGESTÃO DE DADOS")
    typer.echo("=" * 60)
    
    try:
        # Carrega dados
        df = ingest_raw_data(input_path)
        
        # Valida se solicitado
        if validate:
            typer.echo("\nValidando integridade dos dados...")
            validate_data_integrity(df)
        
        # Exibe estatísticas
        typer.echo("\n" + "=" * 60)
        typer.echo("ESTATÍSTICAS")
        typer.echo("=" * 60)
        typer.echo(f"Total de concursos: {len(df)}")
        typer.echo(f"Primeiro concurso: {df['concurso'].min()}")
        typer.echo(f"Último concurso: {df['concurso'].max()}")
        typer.echo(f"Período: {df['data'].min().date()} a {df['data'].max().date()}")
        
        typer.secho("\n✓ Ingestão concluída com sucesso!", fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f"\n✗ Erro: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


@app.command()
def build_features(
    input_path: str = typer.Option(
        "data/raw/Mega-Sena.xlsx",
        "--input", "-i",
        help="Caminho para o arquivo Excel da Mega-Sena"
    ),
    features_output: str = typer.Option(
        "data/processed/draws_features.parquet",
        "--features-output", "-f",
        help="Caminho para salvar as features (Parquet)"
    ),
    vectors_output: str = typer.Option(
        "data/processed/draws_vectors.npz",
        "--vectors-output", "-v",
        help="Caminho para salvar os vetores (NPZ)"
    )
):
    """
    Gera features espaciais e vetores binários para todos os sorteios.
    
    Este comando:
    1. Carrega os dados brutos
    2. Calcula features espaciais (centroide, dispersão, quadrantes, etc.)
    3. Gera vetores binários de 60 posições
    4. Salva tudo em formato otimizado (Parquet + NPZ)
    """
    typer.echo("=" * 60)
    typer.echo("CONSTRUÇÃO DE FEATURES")
    typer.echo("=" * 60)
    
    try:
        # Carrega dados
        typer.echo(f"\nCarregando dados de: {input_path}")
        df = ingest_raw_data(input_path)
        
        # Constrói features
        typer.echo("\nExtraindo features espaciais...")
        features_df = build_features_dataset(df)
        
        # Constrói vetores
        typer.echo("\nGerando vetores binários...")
        vectors = build_vectors_dataset(df)
        
        # Salva
        typer.echo("\nSalvando resultados...")
        save_features(
            features_df=features_df,
            vectors=vectors,
            df_original=df,
            features_path=features_output,
            vectors_path=vectors_output
        )
        
        # Exibe resumo das features
        typer.echo("\n" + "=" * 60)
        typer.echo("RESUMO DAS FEATURES")
        typer.echo("=" * 60)
        typer.echo(f"Concursos processados: {len(features_df)}")
        typer.echo(f"Features por concurso: {len(features_df.columns) - 2}")
        typer.echo(f"\nFeatures disponíveis:")
        feature_cols = [col for col in features_df.columns if col not in ["concurso", "data"]]
        for col in sorted(feature_cols):
            typer.echo(f"  - {col}")
        
        typer.secho("\n✓ Features construídas com sucesso!", fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f"\n✗ Erro: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


@app.command()
def simulate(
    n_simulations: int = typer.Option(
        10000,
        "--n-simulations", "-n",
        help="Número de simulações Monte Carlo"
    ),
    n_draws: int = typer.Option(
        None,
        "--n-draws", "-d",
        help="Número de sorteios por simulação (padrão: igual ao observado)"
    ),
    seed: int = typer.Option(
        42,
        "--seed", "-s",
        help="Seed para reprodutibilidade"
    ),
    input_path: str = typer.Option(
        "data/raw/Mega-Sena.xlsx",
        "--input", "-i",
        help="Caminho para arquivo Excel (para determinar n_draws)"
    )
):
    """
    Executa simulação Monte Carlo para gerar baseline nulo.
    
    Gera sorteios aleatórios e calcula features para comparação
    com os dados observados.
    """
    typer.echo("=" * 60)
    typer.echo("SIMULAÇÃO MONTE CARLO")
    typer.echo("=" * 60)
    
    try:
        # Determina n_draws se não fornecido
        if n_draws is None:
            df = ingest_raw_data(input_path)
            n_draws = len(df)
            typer.echo(f"\nNúmero de sorteios por simulação: {n_draws} (igual ao observado)")
        
        # Executa simulação
        typer.echo(f"\nExecutando {n_simulations} simulações...")
        simulation_df = simulate_monte_carlo(
            n_simulations=n_simulations,
            n_draws_per_sim=n_draws,
            seed=seed,
            include_advanced=True,
            verbose=True
        )
        
        # Calcula estatísticas do baseline
        typer.echo("\nCalculando estatísticas do baseline...")
        baseline_stats = compute_baseline_statistics(simulation_df)
        
        # Salva resultados
        save_simulation_results(simulation_df, baseline_stats)
        
        typer.secho("\n✓ Simulação concluída com sucesso!", fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f"\n✗ Erro: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


@app.command()
def validate(
    features_path: str = typer.Option(
        "data/processed/draws_features.parquet",
        "--features", "-f",
        help="Caminho para features observadas"
    ),
    simulation_path: str = typer.Option(
        "data/processed/monte_carlo_simulation.parquet",
        "--simulation", "-s",
        help="Caminho para simulação Monte Carlo"
    ),
    alpha: float = typer.Option(
        0.05,
        "--alpha", "-a",
        help="Nível de significância"
    ),
    correction: str = typer.Option(
        "fdr",
        "--correction", "-c",
        help="Método de correção (fdr, bonferroni, none)"
    )
):
    """
    Valida features contra baseline Monte Carlo.
    
    Executa testes estatísticos e aplica correção para múltiplas
    hipóteses (FDR ou Bonferroni).
    """
    typer.echo("=" * 60)
    typer.echo("VALIDAÇÃO ESTATÍSTICA")
    typer.echo("=" * 60)
    
    try:
        # Carrega dados
        typer.echo(f"\nCarregando features observadas: {features_path}")
        observed_df = pd.read_parquet(features_path)
        
        typer.echo(f"Carregando simulação: {simulation_path}")
        simulation_df = pd.read_parquet(simulation_path)
        
        # Valida features
        typer.echo(f"\nExecutando testes estatísticos (α={alpha}, correção={correction})...")
        validation_df = validate_features(
            observed_df,
            simulation_df,
            alpha=alpha,
            correction_method=correction
        )
        
        # Gera resumo
        summary = summarize_validation(validation_df)
        
        # Salva resultados
        save_validation_results(validation_df, summary)
        
        # Imprime relatório
        print_validation_report(validation_df, summary)
        
        typer.secho("\n✓ Validação concluída!", fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f"\n✗ Erro: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


@app.command()
def visualize(
    features_path: str = typer.Option(
        "data/processed/draws_features.parquet",
        "--features", "-f",
        help="Caminho para features observadas"
    ),
    simulation_path: str = typer.Option(
        "data/processed/monte_carlo_simulation.parquet",
        "--simulation", "-s",
        help="Caminho para simulação"
    ),
    validation_path: str = typer.Option(
        "data/processed/validation_results.parquet",
        "--validation", "-v",
        help="Caminho para validação"
    ),
    baseline_path: str = typer.Option(
        "data/processed/baseline_statistics.parquet",
        "--baseline", "-b",
        help="Caminho para estatísticas do baseline"
    ),
    output_dir: str = typer.Option(
        "reports",
        "--output", "-o",
        help="Diretório para salvar gráficos"
    )
):
    """
    Gera visualizações (heatmaps, distribuições, comparações).
    """
    typer.echo("=" * 60)
    typer.echo("GERAÇÃO DE VISUALIZAÇÕES")
    typer.echo("=" * 60)
    
    try:
        # Carrega dados
        typer.echo("\nCarregando dados...")
        observed_df = pd.read_parquet(features_path)
        simulation_df = pd.read_parquet(simulation_path)
        validation_df = pd.read_parquet(validation_path)
        baseline_stats = pd.read_parquet(baseline_path)
        
        # Gera visualizações
        generate_all_visualizations(
            observed_df,
            simulation_df,
            validation_df,
            baseline_stats,
            output_dir
        )
        
        typer.secho(f"\n✓ Visualizações geradas em: {output_dir}/", fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f"\n✗ Erro: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


@app.command()
def run_all(
    input_path: str = typer.Option(
        "data/raw/Mega-Sena.xlsx",
        "--input", "-i",
        help="Caminho para arquivo Excel"
    ),
    n_simulations: int = typer.Option(
        10000,
        "--n-simulations", "-n",
        help="Número de simulações Monte Carlo"
    )
):
    """
    Executa pipeline completo: ingest → features → simulate → validate → visualize.
    """
    typer.echo("=" * 60)
    typer.echo("PIPELINE COMPLETO")
    typer.echo("=" * 60)
    
    try:
        # 1. Ingestão
        typer.echo("\n[1/5] Ingestão de dados...")
        df = ingest_raw_data(input_path)
        validate_data_integrity(df)
        
        # 2. Features (básicas + avançadas)
        typer.echo("\n[2/5] Construção de features...")
        features_df = build_features_dataset(df)
        
        # Adiciona features avançadas
        typer.echo("Extraindo features avançadas...")
        advanced_list = []
        for _, row in df.iterrows():
            numbers = [row[f"bola_{i}"] for i in range(1, 7)]
            advanced = extract_advanced_features(numbers)
            advanced["concurso"] = row["concurso"]
            advanced_list.append(advanced)
        
        advanced_df = pd.DataFrame(advanced_list)
        features_df = features_df.merge(advanced_df, on="concurso")
        
        vectors = build_vectors_dataset(df)
        save_features(features_df, vectors, df)
        
        # 3. Simulação
        typer.echo(f"\n[3/5] Simulação Monte Carlo ({n_simulations} simulações)...")
        simulation_df = simulate_monte_carlo(
            n_simulations=n_simulations,
            n_draws_per_sim=len(df),
            seed=42,
            include_advanced=True
        )
        baseline_stats = compute_baseline_statistics(simulation_df)
        save_simulation_results(simulation_df, baseline_stats)
        
        # 4. Validação
        typer.echo("\n[4/5] Validação estatística...")
        validation_df = validate_features(features_df, simulation_df, correction_method="fdr")
        summary = summarize_validation(validation_df)
        save_validation_results(validation_df, summary)
        print_validation_report(validation_df, summary)
        
        # 5. Visualizações
        typer.echo("\n[5/5] Geração de visualizações...")
        generate_all_visualizations(
            features_df,
            simulation_df,
            validation_df,
            baseline_stats
        )
        
        typer.secho("\n" + "=" * 60, fg=typer.colors.GREEN, bold=True)
        typer.secho("✓ PIPELINE COMPLETO EXECUTADO COM SUCESSO!", fg=typer.colors.GREEN, bold=True)
        typer.secho("=" * 60, fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f"\n✗ Erro: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


@app.command()
def info():
    """
    Exibe informações sobre o projeto e os arquivos processados.
    """
    typer.echo("=" * 60)
    typer.echo("INFORMAÇÕES DO PROJETO")
    typer.echo("=" * 60)
    
    # Verifica arquivos
    files_to_check = {
        "Dados brutos": "data/raw/Mega-Sena.xlsx",
        "Features": "data/processed/draws_features.parquet",
        "Vetores": "data/processed/draws_vectors.npz",
        "Simulação": "data/processed/monte_carlo_simulation.parquet",
        "Baseline": "data/processed/baseline_statistics.parquet",
        "Validação": "data/processed/validation_results.parquet"
    }
    
    typer.echo("\nArquivos:")
    for name, path in files_to_check.items():
        file_path = Path(path)
        if file_path.exists():
            size_kb = file_path.stat().st_size // 1024
            typer.secho(f"  ✓ {name}: {path} ({size_kb} KB)", fg=typer.colors.GREEN)
        else:
            typer.secho(f"  ✗ {name}: {path} (não encontrado)", fg=typer.colors.YELLOW)
    
    typer.echo("\nComandos disponíveis:")
    typer.echo("  - ingest: Carrega e valida dados brutos")
    typer.echo("  - build-features: Gera features espaciais")
    typer.echo("  - simulate: Executa simulação Monte Carlo")
    typer.echo("  - validate: Valida features contra baseline")
    typer.echo("  - visualize: Gera visualizações")
    typer.echo("  - run-all: Executa pipeline completo")
    typer.echo("  - info: Exibe esta mensagem")


def main():
    """Entry point para o CLI."""
    app()


if __name__ == "__main__":
    main()
