"""
Módulo para ingestão de dados da Mega-Sena.

Lê o arquivo Excel com histórico de sorteios e converte para formato estruturado.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np


def ingest_raw_data(
    input_path: str = "data/raw/Mega-Sena.xlsx",
    output_path: Optional[str] = None
) -> pd.DataFrame:
    """
    Lê o arquivo Excel da Mega-Sena e retorna um DataFrame limpo.
    
    Espera-se que o arquivo tenha as colunas:
    - Concurso: número do concurso
    - Data do Sorteio: data do sorteio
    - Bola1, Bola2, Bola3, Bola4, Bola5, Bola6: números sorteados
    
    Args:
        input_path: Caminho para o arquivo Excel
        output_path: Caminho opcional para salvar CSV limpo
        
    Returns:
        DataFrame com os dados limpos
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        ValueError: Se o formato do arquivo estiver incorreto
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {input_path}\n"
            f"Certifique-se de colocar o arquivo Mega-Sena.xlsx em data/raw/"
        )
    
    # Lê o arquivo Excel
    df = pd.read_excel(input_file)
    
    # Valida colunas esperadas
    required_cols = ["Concurso", "Data do Sorteio"]
    ball_cols = [f"Bola{i}" for i in range(1, 7)]
    expected_cols = required_cols + ball_cols
    
    missing_cols = set(expected_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Colunas ausentes no arquivo: {missing_cols}\n"
            f"Colunas encontradas: {list(df.columns)}"
        )
    
    # Seleciona e renomeia colunas
    df = df[expected_cols].copy()
    
    # Converte data para datetime (formato brasileiro: DD/MM/YYYY)
    df["Data do Sorteio"] = pd.to_datetime(df["Data do Sorteio"], format='mixed', dayfirst=True)
    
    # Renomeia para formato mais conveniente
    df = df.rename(columns={
        "Concurso": "concurso",
        "Data do Sorteio": "data"
    })
    
    for i, col in enumerate(ball_cols, 1):
        df = df.rename(columns={col: f"bola_{i}"})
    
    # Ordena por concurso
    df = df.sort_values("concurso").reset_index(drop=True)
    
    # Valida que todos os números estão entre 1 e 60
    ball_columns = [f"bola_{i}" for i in range(1, 7)]
    for col in ball_columns:
        invalid = df[~df[col].between(1, 60)]
        if len(invalid) > 0:
            raise ValueError(
                f"Números inválidos encontrados na coluna {col}:\n"
                f"{invalid[['concurso', col]]}"
            )
    
    # Salva CSV se solicitado
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False)
        print(f"Dados salvos em: {output_file}")
    
    print(f"✓ Dados carregados: {len(df)} concursos")
    print(f"✓ Período: {df['data'].min()} a {df['data'].max()}")
    
    return df


def get_draw_numbers(df: pd.DataFrame, concurso: int) -> list:
    """
    Retorna os números sorteados em um concurso específico.
    
    Args:
        df: DataFrame com os dados
        concurso: Número do concurso
        
    Returns:
        Lista com os 6 números sorteados
        
    Raises:
        ValueError: Se o concurso não existir
    """
    row = df[df["concurso"] == concurso]
    
    if len(row) == 0:
        raise ValueError(f"Concurso {concurso} não encontrado")
    
    numbers = [
        row[f"bola_{i}"].iloc[0]
        for i in range(1, 7)
    ]
    
    return numbers


def validate_data_integrity(df: pd.DataFrame) -> bool:
    """
    Valida a integridade dos dados.
    
    Verifica:
    - Não há valores nulos
    - Todos os números estão entre 1 e 60
    - Não há números duplicados em um mesmo concurso
    - Concursos estão em ordem crescente
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        True se os dados estão íntegros
        
    Raises:
        ValueError: Se houver problemas de integridade
    """
    # Verifica valores nulos
    if df.isnull().any().any():
        raise ValueError("Dados contêm valores nulos")
    
    # Verifica números no intervalo válido
    ball_columns = [f"bola_{i}" for i in range(1, 7)]
    for col in ball_columns:
        if not df[col].between(1, 60).all():
            raise ValueError(f"Coluna {col} contém números fora do intervalo 1-60")
    
    # Verifica duplicatas em concursos
    for idx, row in df.iterrows():
        numbers = [row[f"bola_{i}"] for i in range(1, 7)]
        if len(numbers) != len(set(numbers)):
            raise ValueError(
                f"Concurso {row['concurso']} tem números duplicados: {numbers}"
            )
    
    # Verifica ordem dos concursos
    if not df["concurso"].is_monotonic_increasing:
        raise ValueError("Concursos não estão em ordem crescente")
    
    print("✓ Validação de integridade: OK")
    return True
