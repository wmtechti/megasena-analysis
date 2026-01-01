# Plano Técnico de Validação Estatística
## Análise Espacial da Mega-Sena

**Objetivo**: Estabelecer metodologia rigorosa para distinguir **padrões reais** de **aleatoriedade** na distribuição espacial dos sorteios da Mega-Sena.

---

## 1. Definição Formal do Mapeamento

### 1.1 Espaço de Estados

O volante da Mega-Sena é representado como um grafo espacial **G = (V, E)** onde:

- **V**: Conjunto de 60 vértices (células) organizados em grade 10×6
- **E**: Conjunto de arestas definindo relações de vizinhança

### 1.2 Mapeamento Número → Célula

Função bijetiva **φ: {1,...,60} → {0,...,9} × {0,...,5}**

```
φ(n) = (row, col) onde:
  - col = ⌊(n-1) / 10⌋
  - row = (n-1) mod 10
```

**Inversa**: φ⁻¹(r,c) = c × 10 + r + 1

**Propriedades**:
- Preserva ordenação vertical (mesma coluna = números consecutivos mod 10)
- Cada coluna contém exatamente 10 números consecutivos

### 1.3 Definição de Vizinhança

#### Vizinhança 4-conectada (Von Neumann)
Células adjacentes horizontal ou verticalmente:

```
N₄(r,c) = {(r±1,c), (r,c±1)} ∩ V
```

Máximo 4 vizinhos, mínimo 2 (cantos).

#### Vizinhança 8-conectada (Moore)
Inclui diagonais:

```
N₈(r,c) = {(r+i,c+j) : i,j ∈ {-1,0,1}, (i,j)≠(0,0)} ∩ V
```

Máximo 8 vizinhos, mínimo 3 (cantos).

### 1.4 Topologia da Grade

**Bordas**:
- Superior: row = 0
- Inferior: row = 9
- Esquerda: col = 0
- Direita: col = 5

**Cantos**: {(0,0), (0,5), (9,0), (9,5)}

**Células internas**: |N₈| = 8 (total: 32 células)

---

## 2. Features Espaciais Recomendadas

### 2.1 Features Centrais (já implementadas)

#### Centroide
```
C = (r̄, c̄) onde r̄ = (1/6)Σrᵢ, c̄ = (1/6)Σcᵢ
```
**Interpretação**: "Centro de massa" do sorteio no volante.

#### Dispersão (Manhattan Média)
```
D = (1/15) Σᵢ<ⱼ |rᵢ-rⱼ| + |cᵢ-cⱼ|
```
**Range**: [1, 14] (mínimo = 6 números adjacentes, máximo = cantos opostos)

### 2.2 Features Estruturais (a implementar)

#### Densidade Local (Hotspot)
Para cada célula c ∈ V, conta frequência histórica:
```
ρ(c) = (# sorteios com número em c) / (# total de sorteios)
```
**Teste**: χ² para H₀: ρ uniforme = 6/60 = 0.1

#### Compacidade (Razão Área/Perímetro)
```
Compactness = (#células ocupadas) / (#células na borda convexa)
```
Sorteios mais "compactos" têm valor maior.

#### Conectividade
```
K₄ = # componentes conexas usando N₄
K₈ = # componentes conexas usando N₈
```
**Range**: [1, 6]
- K=1: todas as bolas formam cluster conectado
- K=6: todas as bolas isoladas

### 2.3 Features Geométricas Avançadas

#### Momento de Inércia
```
I = Σᵢ [(rᵢ-r̄)² + (cᵢ-c̄)²]
```
Mede "espalhamento" em torno do centroide.

#### Excentricidade (Razão Aspectual)
```
E = σ_row / σ_col
```
Detecta alongamento vertical (E>1) ou horizontal (E<1).

#### Adjacências
```
A₄ = # pares de bolas adjacentes (N₄)
A₈ = # pares de bolas adjacentes (N₈)
```
**Range A₄**: [0, 5], **Range A₈**: [0, 15]

#### Simetria
```
S_vertical = |#{c < 2.5} - #{c ≥ 2.5}|
S_horizontal = |#{r < 4.5} - #{r ≥ 4.5}|
```
Mede desequilíbrio entre metades do volante.

### 2.4 Features por Região

#### Quadrantes (já implementado)
Q₁, Q₂, Q₃, Q₄ com threshold em (r=4.5, c=2.5)

#### Anéis Concêntricos
Distância do centro (4.5, 2.5):
```
Ring₁: d ≤ 2
Ring₂: 2 < d ≤ 4
Ring₃: d > 4
```

---

## 3. Testes Estatísticos

### 3.1 Simulação Monte Carlo

#### Protocolo
1. Gerar **N = 10.000** conjuntos de sorteios aleatórios
2. Cada conjunto tem **M** sorteios (M = # concursos históricos)
3. Cada sorteio = amostra sem reposição de 6 números de {1,...,60}
4. Calcular **todas as features** para cada sorteio simulado

#### Baseline Nulo
Para cada feature F:
```
μ_null = média das médias dos conjuntos simulados
σ_null = desvio padrão das médias
```

### 3.2 P-values e Intervalos de Confiança

#### Teste Bilateral
Para feature F observada nos dados reais:
```
F_obs = média(F) nos dados históricos

p-value = 2 × min(P(F_sim ≤ F_obs), P(F_sim ≥ F_obs))
```

#### Intervalo de Confiança 95%
```
IC₉₅% = [μ_null - 1.96σ_null, μ_null + 1.96σ_null]
```

**Decisão**: Se F_obs ∉ IC₉₅%, rejeitar H₀ (padrão significativo).

### 3.3 Testes Específicos

#### Hotspot (Teste χ²)
```
H₀: Todas as 60 células têm probabilidade uniforme 6/60
χ² = Σc (Oc - Ec)² / Ec
df = 59
```
Onde Oc = frequência observada, Ec = frequência esperada.

#### Adjacência
```
H₀: A₄ segue distribuição nula
Testar se A₄_obs > percentil 95% de A₄_sim
```

#### Compactação vs Dispersão
Comparar distribuições:
- **KS test** (Kolmogorov-Smirnov): Dist(D_obs) vs Dist(D_sim)
- **Mann-Whitney U**: Mediana(D_obs) vs Mediana(D_sim)

### 3.4 Correção para Múltiplas Hipóteses

#### Problema
Testar k features → inflar taxa de erro tipo I (falsos positivos).

#### Correção de Bonferroni (conservadora)
```
α_corrigido = α / k
Exemplo: α=0.05, k=15 features → α'=0.0033
```

#### False Discovery Rate (FDR) - Benjamini-Hochberg (recomendado)
1. Ordenar p-values: p₁ ≤ p₂ ≤ ... ≤ pₖ
2. Encontrar maior i tal que: pᵢ ≤ (i/k)α
3. Rejeitar H₀ para todos os testes j ≤ i

**Vantagem**: Mais poder estatístico que Bonferroni.

### 3.5 Bootstrap para Intervalos de Confiança

Alternativa ao Monte Carlo para features complexas:

1. Reamostragem com reposição dos concursos históricos (B=10.000)
2. Calcular feature em cada amostra bootstrap
3. Percentis 2.5% e 97.5% = IC₉₅%

---

## 4. Critérios de Sucesso: Sinal vs Ruído

### 4.1 Definição de "Sinal"

Um padrão é considerado **sinal** se:

1. **Significância Estatística**
   - p-value < 0.05 após correção FDR
   - F_obs fora do IC₉₅% do baseline Monte Carlo

2. **Tamanho de Efeito (Effect Size)**
   ```
   d = |F_obs - μ_null| / σ_null
   ```
   - d < 0.2: efeito pequeno (ruído)
   - 0.2 ≤ d < 0.5: efeito médio
   - d ≥ 0.5: efeito grande (**sinal**)

3. **Replicabilidade**
   - Padrão se mantém em:
     - Análise de janelas temporais (primeiros 50% vs últimos 50%)
     - Validação cruzada (k-fold com k=5)

### 4.2 Definição de "Ruído"

Padrões **não confiáveis** (ruído):

- p-value > 0.05 após correção
- d < 0.2
- Padrão se inverte em subconjuntos temporais
- Alta variância bootstrap (IC muito largo)

### 4.3 Checklist de Validação

- [ ] Feature passa no teste Monte Carlo (p < 0.05)
- [ ] Correção FDR aplicada
- [ ] Tamanho de efeito d > 0.5
- [ ] Padrão estável em janela móvel (últimos N concursos)
- [ ] Interpretação física plausível
- [ ] Não confunde correlação com causalidade

---

## 5. Recomendações de Visualizações

### 5.1 Heatmap de Densidade (Hotspot)

**Tipo**: Matriz 10×6 com escala de cores

**Dados**: Frequência relativa de cada célula

**Camadas**:
1. Base: frequência observada
2. Overlay: contorno do IC₉₅% do baseline
3. Marcadores: células significativamente "quentes" ou "frias"

**Ferramentas**: `matplotlib.pyplot.imshow`, `seaborn.heatmap`

```python
import seaborn as sns
import numpy as np

# Matriz 10x6 com frequências
freq_matrix = np.zeros((10, 6))
for concurso in dados:
    for num in concurso:
        r, c = num_to_pos(num)
        freq_matrix[r, c] += 1
freq_matrix /= len(dados)

sns.heatmap(freq_matrix, annot=True, fmt='.3f', cmap='YlOrRd')
```

### 5.2 Distribuição de Dispersão

**Tipo**: Histograma + KDE sobreposto

**Dados**:
- Dispersão observada (azul)
- Dispersão simulada Monte Carlo (cinza, α=0.3)

**Elementos**:
- Linha vertical: média observada
- Área sombreada: IC₉₅% do baseline

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.hist(dispersion_sim, bins=50, alpha=0.3, label='Baseline')
ax.hist(dispersion_obs, bins=50, alpha=0.7, label='Observado')
ax.axvline(mean_obs, color='red', linestyle='--')
ax.fill_betweenx([0, max_y], ic_lower, ic_upper, alpha=0.2)
```

### 5.3 Scatter Plot: Centroide

**Eixos**: (mean_row, mean_col)

**Pontos**:
- Cada concurso histórico (pequeno, α=0.5)
- Centroide do baseline (cruz vermelha grande)

**Overlay**: Elipse de confiança 95%

### 5.4 Série Temporal de Features

**Eixo X**: Número do concurso (ou data)

**Eixo Y**: Valor da feature (e.g., dispersão, A₄)

**Elementos**:
- Linha: valor observado
- Banda: IC₉₅% do baseline (horizontal)
- Marcadores: pontos fora do IC

**Objetivo**: Detectar tendências temporais ou quebras estruturais.

### 5.5 Grafo de Conectividade

**Tipo**: Network plot

**Nós**: Células ocupadas em um sorteio

**Arestas**: Conexões N₄ ou N₈

**Cor**: 
- Verde: componente conexa grande (≥4 nós)
- Vermelho: nós isolados

**Métrica**: Mostrar K₄ e K₈ no título

### 5.6 Matriz de Correlação de Features

**Tipo**: Heatmap triangular

**Dados**: Correlação de Pearson entre todas as features

**Objetivo**: Identificar redundância (|r| > 0.8) ou independência

```python
corr_matrix = features_df.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, cmap='coolwarm', center=0)
```

### 5.7 Box Plot Comparativo

**Grupos**: Observado vs Simulado

**Features**: Dispersão, A₄, Conectividade, etc.

**Elementos**: Outliers, quartis, mediana

---

## 6. Pipeline de Validação

### Workflow Proposto

```
1. INGESTÃO
   └─> data/raw/Mega-Sena.xlsx
   └─> validação de integridade

2. FEATURES OBSERVADAS
   └─> calcular todas as features
   └─> salvar draws_features.parquet

3. SIMULAÇÃO MONTE CARLO
   └─> gerar N=10.000 conjuntos aleatórios
   └─> calcular features para cada conjunto
   └─> salvar baseline_features.parquet

4. TESTES ESTATÍSTICOS
   └─> p-values para cada feature
   └─> correção FDR
   └─> tamanho de efeito
   └─> salvar validation_report.json

5. VISUALIZAÇÕES
   └─> gerar todos os gráficos
   └─> salvar em reports/

6. RELATÓRIO FINAL
   └─> markdown com conclusões
   └─> tabela de features significativas
```

### Entrega Esperada

#### Arquivos de Dados
- [x] `data/processed/draws_features.parquet` (features observadas)
- [ ] `data/processed/draws_vectors.npz` (vetores 60D)
- [ ] `data/processed/baseline_features.parquet` (Monte Carlo)
- [ ] `data/processed/validation_results.json`

#### Código
- [x] `src/spatial.py` (mapeamento)
- [x] `src/features.py` (features básicas)
- [ ] `src/features_advanced.py` (conectividade, simetria, etc.)
- [ ] `src/monte_carlo.py` (simulação)
- [ ] `src/validation.py` (testes estatísticos)
- [ ] `src/visualization.py` (gráficos)

#### Testes
- [x] `tests/test_spatial.py`
- [x] `tests/test_features.py`
- [ ] `tests/test_monte_carlo.py`
- [ ] `tests/test_validation.py`

#### Documentação
- [x] `README.md`
- [x] `docs/validation_plan.md` (este documento)
- [ ] `reports/validation_report.md` (resultados)

---

## 7. Métricas de Qualidade do Pipeline

### 7.1 Reprodutibilidade
- Seed fixo para RNG: `np.random.seed(42)`
- Versionamento de dados e código (git)
- Requisitos explícitos (`requirements.txt`)

### 7.2 Performance
- Monte Carlo com N=10.000: ~30s (otimizar com NumPy vetorizado)
- Features por concurso: <1ms
- Pipeline completo: <2min

### 7.3 Cobertura de Testes
- Alvo: >80% de code coverage
- Testes unitários para todas as funções puras
- Testes de integração para pipeline completo

---

## 8. Limitações e Vieses a Evitar

### 8.1 P-hacking
**Risco**: Testar múltiplas hipóteses até encontrar p<0.05

**Mitigação**: 
- Pré-registrar hipóteses
- Aplicar correção FDR
- Reportar TODOS os testes, não só os significativos

### 8.2 Overfitting Temporal
**Risco**: Padrões válidos apenas no passado, não generalizam

**Mitigação**:
- Validação cruzada temporal (train/test split cronológico)
- Janela móvel para detectar mudanças de regime

### 8.3 Correlação Espúria
**Risco**: Variáveis correlacionadas por acaso

**Mitigação**:
- Exigir mecanismo causal plausível
- Testar estabilidade em subamostras
- Comparar com baseline permutado

### 8.4 Viés de Sobrevivência
**Risco**: Considerar apenas estratégias que "funcionaram" no passado

**Mitigação**:
- Não usar dados históricos para validar estratégias derivadas deles
- Backtest em dados out-of-sample

---

## 9. Referências Metodológicas

### Estatística Espacial
- Anselin, L. (1995). *Local Indicators of Spatial Association—LISA*
- Getis & Ord (1992). *The Analysis of Spatial Association*

### Correção de Hipóteses Múltiplas
- Benjamini & Hochberg (1995). *Controlling the False Discovery Rate*

### Simulação Monte Carlo
- Metropolis & Ulam (1949). *The Monte Carlo Method*
- Robert & Casella (2004). *Monte Carlo Statistical Methods*

### Análise de Redes Espaciais
- Newman (2010). *Networks: An Introduction*

---

## 10. Próximas Etapas (após validação)

Uma vez estabelecido o baseline:

1. **Hotspot Analysis**: Identificar células sistematicamente superutilizadas
2. **Clustering Espacial**: DBSCAN, K-means nas posições (r,c)
3. **Análise de Grafos**: Pagerank, centralidade, comunidades
4. **Set Cover Otimizado**: Minimizar apostas para cobrir padrões
5. **Machine Learning**: Features → probabilidade de saída
6. **Meta-análise**: Combinar múltiplos sinais (ensemble)

**Importante**: Nenhuma dessas etapas deve prosseguir sem **validação estatística rigorosa** da etapa anterior.

---

**Status**: Plano definido ✅  
**Próximo passo**: Implementar `src/monte_carlo.py` e `src/validation.py`
