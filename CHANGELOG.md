# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-01-03

### 🎉 Release Inicial

#### Adicionado
- **Pipeline completo de análise espacial** da Mega-Sena
- **Mapeamento espacial** dos números em grade 10×6 (volante)
- **27 features espaciais**:
  - Básicas: centroide, dispersão, quadrantes, bordas, cantos
  - Avançadas: adjacências, conectividade, inércia, excentricidade, compacidade, simetria, anéis
- **Simulação Monte Carlo** com baseline aleatório (configurável, padrão: 10.000 runs)
- **Validação estatística robusta**:
  - Testes Mann-Whitney U e Kolmogorov-Smirnov
  - Correção para múltiplas comparações (FDR e Bonferroni)
  - Cálculo de effect size e intervalos de confiança
- **Visualizações**:
  - Heatmap de densidade do volante
  - Comparação de dispersão observado vs simulado
  - Scatter plot de centroides
  - Comparação de features
  - Distribuição de tamanhos de efeito
- **CLI interativa** com 7 comandos:
  - `ingest`: Carrega e valida dados brutos
  - `build-features`: Gera features espaciais
  - `simulate`: Executa Monte Carlo
  - `validate`: Validação estatística
  - `visualize`: Gera gráficos
  - `run-all`: Pipeline completo
  - `info`: Informações do sistema
- **Notebook interativo** (`analise_resultados.ipynb`) para exploração visual
- **Script de estimativa de tempo** (`estimate_time.py`) para planejamento de execução
- **Documentação completa**:
  - README.md com guia de instalação e uso
  - QUICKSTART.md para início rápido
  - docs/validation_plan.md com metodologia detalhada
  - docs/git_guide.md para controle de versão
- **Testes unitários** para funções críticas (spatial, features)
- **Suporte a ambientes virtuais** (venv)

#### Resultados Científicos
- ✅ **Conclusão**: Sorteios da Mega-Sena são compatíveis com aleatoriedade pura
- 📊 **Dados**: 2.954 concursos analisados (1996-2025)
- 🧪 **Validação**: 5.000 simulações × 2.954 sorteios = 14.770.000 sorteios aleatórios
- 📉 **Achados**: 0 features significativas (p < 0.05 após correção FDR)
- 🎯 **Effect sizes**: Todos < 0.05 (desprezíveis)

#### Tecnologias
- Python 3.11+
- pandas, numpy, scipy (análise)
- matplotlib, seaborn (visualização)
- typer (CLI)
- pytest (testes)
- pyarrow/parquet (armazenamento eficiente)

### Correções Aplicadas
- Tratamento de datas brasileiras (formato dd/mm/yyyy)
- Prevenção de valores `inf` e `NaN` em features avançadas
- Correção de bug no script de estimativa de tempo
- Adição de dados brutos para geração de heatmap

### Notas Técnicas
- Tempo estimado de execução (5000 simulações): ~2h
- Arquivos de saída em formato Parquet (compressão eficiente)
- Reprodutibilidade garantida via seeds aleatórias

---

## Formato de Versionamento

- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções de bugs compatíveis

Exemplo: v1.2.3
- 1 = MAJOR
- 2 = MINOR  
- 3 = PATCH
