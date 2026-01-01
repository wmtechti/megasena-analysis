# Guia Rápido de Início

## 🚀 Quick Start (5 minutos)

### 1. Preparação do Ambiente

```powershell
# Navegue até o diretório do projeto
cd f:\projetos\2026\megasena

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
.\venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt
```

### 2. Adicione os Dados

Coloque o arquivo `Mega-Sena.xlsx` em `data/raw/`

O arquivo deve ter as colunas:
- `Concurso`
- `Data do Sorteio`
- `Bola1`, `Bola2`, `Bola3`, `Bola4`, `Bola5`, `Bola6`

### 3. Execute o Pipeline Completo

```powershell
# Opção mais simples: executa tudo de uma vez
python -m src.pipeline run-all
```

Isso vai:
1. ✅ Carregar e validar dados
2. ✅ Gerar features espaciais (básicas + avançadas)
3. ✅ Simular 10.000 sorteios aleatórios (baseline)
4. ✅ Validar features estatisticamente
5. ✅ Gerar visualizações

**Tempo estimado**: ~2-5 minutos (depende do número de concursos)

### 4. Verifique os Resultados

```powershell
# Veja o status
python -m src.pipeline info
```

## 📂 Arquivos Gerados

Após executar o pipeline, você terá:

### `data/processed/`
- `draws_features.parquet` - Features de cada concurso
- `draws_vectors.npz` - Vetores binários 60D
- `monte_carlo_simulation.parquet` - Simulação completa
- `baseline_statistics.parquet` - Estatísticas do baseline
- `validation_results.parquet` - Resultados dos testes
- `validation_summary.json` - Resumo da validação
- `significant_features.csv` - Features significativas

### `reports/`
- `heatmap_density.png` - Mapa de calor do volante
- `dispersion_comparison.png` - Observado vs simulado
- `centroid_scatter.png` - Distribuição de centroides
- `feature_comparison.png` - Top features
- `effect_size_distribution.png` - Tamanho de efeito

## 🔍 Explorando os Resultados

### No Python

```python
import pandas as pd
import numpy as np

# Carrega features observadas
features = pd.read_parquet("data/processed/draws_features.parquet")
print(features.head())

# Carrega validação
validation = pd.read_parquet("data/processed/validation_results.parquet")

# Features significativas
significant = validation[validation["significant"]]
print(significant[["feature", "effect_size", "p_value_adjusted"]])

# Vetores binários
data = np.load("data/processed/draws_vectors.npz")
vectors = data["vectors"]
print(f"Shape: {vectors.shape}")  # (n_concursos, 60)
```

### Interpretando a Validação

Abra `data/processed/validation_summary.json`:

```json
{
  "n_features_tested": 25,
  "n_significant": 3,
  "significant_features": ["dispersion", "connectivity_4", "inertia"],
  ...
}
```

- **n_significant > 0**: Existem padrões estatisticamente significativos
- **significant_features**: Lista das features que passaram no teste
- **top_5_by_effect_size**: Maiores diferenças vs baseline

## 📊 Visualizações

Abra os arquivos em `reports/`:

1. **heatmap_density.png**: Mostra se certas células do volante são mais frequentes
2. **dispersion_comparison.png**: Compara dispersão real vs aleatória
3. **centroid_scatter.png**: Onde ficam os "centros" dos sorteios
4. **feature_comparison.png**: Quais features diferem do acaso
5. **effect_size_distribution.png**: Magnitude das diferenças

## 🎯 Próximos Passos

### Análise Exploratória

```powershell
# Crie um notebook Jupyter
jupyter notebook
```

Use os dados em `data/processed/` para:
- Explorar correlações entre features
- Identificar clusters de sorteios
- Testar hipóteses específicas

### Executar Etapas Individuais

Se quiser rodar apenas parte do pipeline:

```powershell
# Apenas ingestão
python -m src.pipeline ingest

# Apenas features
python -m src.pipeline build-features

# Apenas simulação (mais rápida com menos simulações)
python -m src.pipeline simulate --n-simulations 1000

# Apenas validação
python -m src.pipeline validate

# Apenas visualizações
python -m src.pipeline visualize
```

### Rodar Testes

```powershell
# Testes unitários
pytest -v

# Com cobertura
pytest --cov=src tests/
```

## ⚠️ Troubleshooting

### Erro: "Arquivo não encontrado"

Certifique-se de que `Mega-Sena.xlsx` está em `data/raw/`

### Erro: "Módulo não encontrado"

```powershell
# Reinstale as dependências
pip install -r requirements.txt
```

### Simulação muito lenta

Reduza o número de simulações:

```powershell
python -m src.pipeline simulate --n-simulations 1000
```

### Memória insuficiente

A simulação completa pode usar ~2-4 GB de RAM. Se necessário:
- Reduza `n_simulations`
- Ou execute em lotes menores

## 📚 Documentação Completa

- [README.md](README.md) - Visão geral do projeto
- [docs/validation_plan.md](docs/validation_plan.md) - Plano técnico de validação
- Comentários no código fonte (docstrings)

## 🤔 Interpretação dos Resultados

### Se houver features significativas:

✅ **Bom sinal**: Existem padrões espaciais além do acaso  
⚠️ **Cuidado**: Isso NÃO significa que você pode prever sorteios futuros  
📊 **Use para**: Entender distribuições históricas, não para apostas

### Se NÃO houver features significativas:

✅ **Esperado**: Sorteios são aleatórios (como deveriam ser)  
✅ **Pipeline funciona**: Validação estatística está detectando ausência de padrões  
📊 **Conclusão**: Distribuição espacial é uniforme

## 💡 Lembre-se

> **A loteria é aleatória por design. Padrões históricos não garantem resultados futuros.**

Este projeto é para:
- ✅ Aprendizado de análise espacial
- ✅ Validação estatística rigorosa
- ✅ Visualização de dados
- ❌ **NÃO** para prever sorteios futuros
- ❌ **NÃO** para estratégias de apostas "garantidas"

---

**Dúvidas?** Consulte a documentação completa ou abra uma issue no GitHub.
