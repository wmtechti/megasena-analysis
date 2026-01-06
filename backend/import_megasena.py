"""
Script de importação de dados históricos da Mega-Sena.

Lê dados do arquivo Excel e importa para o banco de dados.
"""

import sys
from pathlib import Path
from datetime import datetime

# Adicionar backend ao path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

import pandas as pd
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.lottery_service import LotteryService
from app.services.draw_service import DrawService


def parse_date(date_str):
    """
    Parse data do formato dd/mm/yyyy.
    
    Args:
        date_str: String com data
        
    Returns:
        datetime.date
    """
    if pd.isna(date_str):
        return None
    
    try:
        # Formato dd/mm/yyyy
        return datetime.strptime(str(date_str), "%d/%m/%Y").date()
    except:
        try:
            # Tentar outros formatos
            return pd.to_datetime(date_str).date()
        except:
            return None


def import_megasena(db: Session, excel_file: Path, limit: int = None, auto_confirm: bool = False):
    """
    Importa dados da Mega-Sena do Excel.
    
    Args:
        db: Sessão do banco
        excel_file: Caminho do arquivo Excel
        limit: Limite de registros (None = todos)
    """
    print(f"📂 Lendo arquivo: {excel_file}")
    
    # Ler Excel
    df = pd.read_excel(excel_file)
    print(f"   Encontradas {len(df)} linhas")
    
    # Verificar colunas esperadas
    expected_cols = ['Concurso', 'Data do Sorteio']
    for col in expected_cols:
        if col not in df.columns:
            print(f"❌ Coluna '{col}' não encontrada no arquivo")
            print(f"   Colunas disponíveis: {', '.join(df.columns)}")
            return
    
    print(f"   Colunas encontradas: {', '.join(df.columns[:15])}...")
    
    # Buscar loteria Mega-Sena
    lottery = LotteryService.get_by_slug(db, "megasena")
    if not lottery:
        print("❌ Loteria 'megasena' não encontrada no banco")
        return
    
    print(f"\n🎲 Importando para: {lottery.name} (ID: {lottery.id})")
    
    # Preparar dados
    draws_data = []
    
    for idx, row in df.iterrows():
        if limit and idx >= limit:
            break
        
        # Número do concurso
        contest_number = int(row['Concurso'])
        
        # Data do sorteio
        draw_date = parse_date(row['Data do Sorteio'])
        if not draw_date:
            print(f"⚠️  Concurso {contest_number}: data inválida, pulando...")
            continue
        
        # Números sorteados (colunas 3 a 8, ou nomes específicos)
        numbers = []
        
        # Tentar por nome de coluna
        for i in range(1, 7):
            col_name = f'Bola{i}'
            if col_name in row and not pd.isna(row[col_name]):
                numbers.append(int(row[col_name]))
        
        # Se não encontrou por nome, tentar por posição (colunas 2-7)
        if len(numbers) == 0:
            try:
                # Assumir que números estão nas colunas após Data do Sorteio
                cols = df.columns.tolist()
                data_idx = cols.index('Data do Sorteio')
                for i in range(1, 7):
                    col_idx = data_idx + i
                    if col_idx < len(cols) and not pd.isna(row.iloc[col_idx]):
                        numbers.append(int(row.iloc[col_idx]))
            except:
                pass
        
        # Validar números
        if len(numbers) != 6:
            print(f"⚠️  Concurso {contest_number}: esperados 6 números, encontrados {len(numbers)}, pulando...")
            continue
        
        # Ordenar números
        numbers.sort()
        
        # Valor do prêmio (se disponível)
        prize_value = None
        if 'Rateio 6 acertos' in row and not pd.isna(row['Rateio 6 acertos']):
            try:
                prize_value = float(row['Rateio 6 acertos'])
            except:
                pass
        
        # Quantidade de ganhadores (se disponível)
        winners = None
        if 'Ganhadores 6 acertos' in row and not pd.isna(row['Ganhadores 6 acertos']):
            try:
                winners = int(row['Ganhadores 6 acertos'])
            except:
                pass
        
        draws_data.append({
            "contest_number": contest_number,
            "draw_date": draw_date,
            "numbers": numbers,
            "prize_value": prize_value,
            "winners": winners,
        })
    
    print(f"\n✅ Preparados {len(draws_data)} sorteios para importação")
    
    if len(draws_data) == 0:
        print("❌ Nenhum sorteio válido encontrado")
        return
    
    # Confirmar antes de importar
    print(f"\n📊 Exemplo do primeiro sorteio:")
    first = draws_data[0]
    print(f"   Concurso: {first['contest_number']}")
    print(f"   Data: {first['draw_date']}")
    print(f"   Números: {first['numbers']}")
    
    if not auto_confirm:
        response = input(f"\n❓ Confirma importação de {len(draws_data)} sorteios? (s/n): ")
        if response.lower() != 's':
            print("❌ Importação cancelada")
            return
    else:
        print(f"\n✅ Auto-confirmado (--yes)")
    
    # Importar
    print(f"\n🚀 Iniciando importação...")
    imported = DrawService.bulk_import(
        db,
        lottery_id=lottery.id,
        draws_data=draws_data,
        calculate_features=True
    )
    
    print(f"\n✅ Importação concluída!")
    print(f"   Sorteios importados: {imported}")
    print(f"   Sorteios pulados (já existentes): {len(draws_data) - imported}")


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Importar dados da Mega-Sena")
    parser.add_argument(
        "--file",
        type=str,
        default="../data/raw/Mega-Sena.xlsx",
        help="Caminho do arquivo Excel (padrão: ../data/raw/Mega-Sena.xlsx)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limite de registros para teste (None = todos)"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Confirmar automaticamente sem perguntar"
    )
    
    args = parser.parse_args()
    
    # Resolver caminho do arquivo
    excel_file = Path(__file__).parent / args.file
    if not excel_file.exists():
        print(f"❌ Arquivo não encontrado: {excel_file}")
        return
    
    # Criar sessão do banco
    db = SessionLocal()
    
    try:
        import_megasena(db, excel_file, limit=args.limit, auto_confirm=args.yes)
    except Exception as e:
        print(f"\n❌ Erro durante importação: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
