# Mega-Sena: Análise Espacial

Pipeline de análise dos sorteios da Mega-Sena com foco na **distribuição espacial** dos números no volante 10x6.

## 📋 Visão Geral

Este projeto implementa um pipeline completo para:

1. **Ingestão de dados** históricos da Mega-Sena
2. **Mapeamento espacial** dos números (1-60) para posições no volante (10 linhas × 6 colunas)
3. **Extração de features espaciais** (centroide, dispersão, quadrantes, bordas, etc.)
4. **Validações estatísticas** e geração de datasets otimizados

## 🎯 Conceito: Volante 10×6

O volante da Mega-Sena é organizado como uma **grade de 10 linhas e 6 colunas**:

```
Col:    0      1      2      3      4      5
Row: +------+------+------+------+------+------+
  0  |  01  |  11  |  21  |  31  |  41  |  51  |
  1  |  02  |  12  |  22  |  32  |  42  |  52  |
  2  |  03  |  13  |  23  |  33  |  43  |  53  |
  3  |  04  |  14  |  24  |  34  |  44  |  54  |
  4  |  05  |  15  |  25  |  35  |  45  |  55  |
  5  |  06  |  16  |  26  |  36  |  46  |  56  |
  6  |  07  |  17  |  27  |  37  |  47  |  57  |
  7  |  08  |  18  |  28  |  38  |  48  |  58  |
  8  |  09  |  19  |  29  |  39  |  49  |  59  |
  9  |  10  |  20  |  30  |  40  |  50  |  60  |
     +------+------+------+------+------+------+
```

**Mapeamento**: número `n` → posição `(row, col)` onde:
- `col = (n - 1) // 10`
- `row = (n - 1) % 10`

## 🗂️ Estrutura do Projeto

```
megasena/
├── src/
│   ├── __init__.py
│   ├── __main__.py          # Entry point para CLI
│   ├── spatial.py           # Mapeamento espacial do volante
│   ├── ingest.py            # Ingestão e validação de dados
│   ├── features.py          # Extração de features espaciais
│   └── pipeline.py          # CLI (Typer)
├── data/
│   ├── raw/
│   │   └── Mega-Sena.xlsx   # Arquivo histórico (não versionado)
│   └── processed/
│       ├── draws_features.parquet  # Features espaciais
│       └── draws_vectors.npz       # Vetores binários
├── notebooks/               # Análises exploratórias
├── reports/                 # Relatórios e visualizações
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_spatial.py      # Testes do mapeamento espacial
│   └── test_features.py     # Testes das features
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

## 🚀 Instalação

### 1. Clone o repositório

```bash
cd f:\projetos\2026\megasena
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou instale o projeto em modo desenvolvimento:

```bash
pip install -e .
```

### 4. Adicione o arquivo de dados

Coloque o arquivo `Mega-Sena.xlsx` na pasta `data/raw/`.

O arquivo deve ter as colunas:
- `Concurso`: número do concurso
- `Data do Sorteio`: data do sorteio
- `Bola1`, `Bola2`, `Bola3`, `Bola4`, `Bola5`, `Bola6`: números sorteados

## 📦 Features Espaciais

### Features Básicas

Para cada sorteio, são extraídas as seguintes features:

#### Centroide
- `centroid_row`: média das linhas (0-9)
- `centroid_col`: média das colunas (0-5)

#### Dispersão
- `dispersion`: distância Manhattan média entre todos os pares de números

#### Quadrantes (4 regiões)
- `q1`: contagem no quadrante 1 (superior esquerdo)
- `q2`: contagem no quadrante 2 (superior direito)
- `q3`: contagem no quadrante 3 (inferior esquerdo)
- `q4`: contagem no quadrante 4 (inferior direito)

#### Bordas e Cantos
- `border_count`: quantidade de números nas bordas do volante
- `corner_count`: quantidade de números nos 4 cantos

#### Distribuição por Linha/Coluna
- `row_std`: desvio padrão das linhas
- `col_std`: desvio padrão das colunas
- `row_min`, `row_max`: limites das linhas ocupadas
- `col_min`, `col_max`: limites das colunas ocupadas

### Features Avançadas

#### Adjacências e Conectividade
- `adjacencies_4`: número de pares adjacentes (4-conectados)
- `adjacencies_8`: número de pares adjacentes (8-conectados)
- `connectivity_4`: componentes conexas (4-conectadas)
- `connectivity_8`: componentes conexas (8-conectadas)

#### Geometria
- `inertia`: momento de inércia em torno do centroide
- `eccentricity`: razão aspectual (σ_row / σ_col)
- `compactness`: medida de compacidade (área/perímetro)

#### Simetria
- `symmetry_horizontal`: desequilíbrio superior/inferior
- `symmetry_vertical`: desequilíbrio esquerda/direita

#### Anéis Concêntricos
- `ring1`: números próximos ao centro (d ≤ 2)
- `ring2`: números médios (2 < d ≤ 4)
- `ring3`: números distantes (d > 4)

## 💻 Uso da CLI

O projeto usa **Typer** para interface de linha de comando.

### Comandos Disponíveis

#### 1. Ingestão de Dados

Carrega e valida os dados brutos:

```bash
python -m src.pipeline ingest
```

#### 2. Construção de Features

Gera features espaciais (básicas + avançadas) e vetores binários:

```bash
python -m src.pipeline build-features
```

#### 3. Simulação Monte Carlo

Gera baseline nulo com sorteios aleatórios:

```bash
python -m src.pipeline simulate --n-simulations 10000
```

Opções:
- `--n-simulations`, `-n`: Número de simulações (padrão: 10000)
- `--n-draws`, `-d`: Sorteios por simulação (padrão: igual ao observado)
- `--seed`, `-s`: Seed para reprodutibilidade (padrão: 42)

#### 4. Validação Estatística

Valida features contra baseline com correção para múltiplas hipóteses:

```bash
python -m src.pipeline validate
```

Opções:
- `--alpha`, `-a`: Nível de significância (padrão: 0.05)
- `--correction`, `-c`: Método de correção (`fdr`, `bonferroni`, `none`)

#### 5. Visualizações

Gera todos os gráficos (heatmaps, distribuições, comparações):

```bash
python -m src.pipeline visualize
```

#### 6. Pipeline Completo

Executa todas as etapas de uma vez:

```bash
python -m src.pipeline run-all
```

#### 7. Informações

Verifica status dos arquivos:

```bash
python -m src.pipeline info
```

### Workflow Recomendado

```bash
# Opção 1: Pipeline completo (recomendado para primeira execução)
python -m src.pipeline run-all

# Opção 2: Passo a passo
python -m src.pipeline ingest
python -m src.pipeline build-features
python -m src.pipeline simulate
python -m src.pipeline validate
python -m src.pipeline visualize
```

## 🧪 Testes

Execute os testes unitários com pytest:

```bash
# Executar todos os testes
pytest

# Executar com verbosidade
pytest -v

# 25+ colunas de features espaciais (básicas + avançadas)

```python
import pandas as pd
df = pd.read_parquet("data/processed/draws_features.parquet")
print(df.head())
```

### 2. Vetores Binários (NPZ)

`data/processed/draws_vectors.npz`

Array NumPy comprimido com:
- `vectors`: matriz (n_concursos × 60) com 1 se o número saiu, 0 caso contrário
- `concursos`: array com números dos concursos

```python
import numpy as np
data = np.load("data/processed/draws_vectors.npz")
vectors = data["vectors"]
concursos = data["concursos"]
print(vectors.shape)  # (n_concursos, 60)
```

### 3. Simulação Monte Carlo (Parquet)

`data/processed/monte_carlo_simulation.parquet`

DataFrame com features de 10.000 simulações × N sorteios cada.

### 4. Estatísticas do Baseline (Parquet)

`data/processed/baseline_statistics.parquet`

Estatísticas (média, std, percentis) de cada feature no baseline nulo.

### 5. Validação (Parquet + JSON)

`data/processed/validation_results.parquet`

Resultados dos testes estatísticos com p-values, tamanho de efeito, etc.

`data/processed/validation_summary.json`

Resumo executivo da validação.

### 6. Visualizações (PNG)

`reports/`

Gráficos gerados:
- `heatmap_density.png`: Densidade de frequência no volante
- `dispersion_comparison.png`: Observado vs simulado
- `centroid_scatter.png`: Distribuição de centroides
- `feature_comparison.png`: Top features por tamanho de efeito
- `effect_size_distribution.png`: Histograma de effect sizesconcurso`: número do concurso
- `data`: data do sorteio
- 14 colunas de features espaciais

```python
import pandas as pd
df = pd.read_parquet("data/processed/draws_features.parquet")
print(df.head())
```

- **scipy** ≥ 1.11.0: Testes estatísticos
- **matplotlib** ≥ 3.7.0: Visualizações
- **seaborn** ≥ 0.12.0: Visualizações estatísticas
- **tqdm** ≥ 4.66.0: Barras de progresso

## 🔬 Validação Estatística

O projeto implementa validação rigorosa para evitar **autoengano** e distinguir padrões reais de ruído:

### Simulação Monte Carlo
- 10.000 conjuntos de sorteios aleatórios
- Cada conjunto tem o mesmo número de sorteios que os dados reais
- Gera **baseline nulo** para comparação

### Testes Aplicados
- **P-values bilaterais**: Via Monte Carlo
- **Tamanho de efeito**: Z-score (Cohen's d)
- **Intervalos de confiança**: Percentis 2.5% e 97.5%
- **Correção FDR**: Benjamini-Hochberg para múltiplas hipóteses
- **Testes auxiliares**: Kolmogorov-Smirnov, Mann-Whitney U

### Critérios de Significância

Um padrão é considerado **sinal** (não ruído) se:
1. P-value ajustado < 0.05 (após correção FDR)
2. Tamanho de efeito ≥ 0.5 (grande)
3. Valor observado fora do IC 95% do baseline

Veja detalhes em: [docs/validation_plan.md](docs/validation_plan.md)
### 2. Vetores Binários (NPZ)

`data/processed/draws_vectors.npz`

Array NumPy comprimido com:
- `vectors`: matriz (n_concursos × 60) com 1 se o número saiu, 0 caso contrário
- `concursos`: array com números dos concursos

```python
import numpy as np
data = np.load("data/processed/draws_vectors.npz")
vectors = data["vectors"]
concursos = data["concursos"]
print(vectors.shape)  # (n_concursos, 60)
```

## 📈 Próximos Passos

Com o pipeline montado, você pode:

1. **Análise Exploratória**: Criar notebooks para visualizar padrões espaciais
2. **Validações Estatísticas**: Testar hipóteses sobre distribuição espacial
3. **Modelagem ML**: Treinar modelos preditivos usando as features
4. **Otimização**: Desenvolver estratégias de seleção de números

## 📝 Dependências

- **pandas** ≥ 2.0.0: Manipulação de dados
- **numpy** ≥ 1.24.0: Operações numéricas
- **openpyxl** ≥ 3.1.0: Leitura de arquivos Excel
- **pyarrow** ≥ 12.0.0: Formato Parquet
- **typer** ≥ 0.9.0: Interface CLI
- **pytest** ≥ 7.4.0: Testes unitários

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto para fins educacionais e de pesquisa.

## 🔗 Referências

- [Mega-Sena - Caixa Econômica Federal](https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NumPy Documentation](https://numpy.org/)
- [Typer Documentation](https://typer.tiangolo.com/)

---

**Autor**: Projeto de Análise Espacial da Mega-Sena  
**Data**: Janeiro de 2026
