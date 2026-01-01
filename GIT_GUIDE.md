# Megasena Spatial Analysis - Guia de Versionamento Git

## Inicialização do Repositório

```bash
# Já inicializado
git init

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "Initial commit: Análise espacial Mega-Sena com validação estatística"
```

## Estrutura de Branches

```bash
# Branch principal
main (ou master)

# Branches de desenvolvimento
git checkout -b feature/nome-da-feature
git checkout -b fix/nome-do-bug
git checkout -b experiment/nome-do-experimento
```

## Comandos Úteis

### Commits Frequentes

```bash
# Adicionar arquivos específicos
git add src/
git add tests/

# Commit com mensagem
git commit -m "feat: Adiciona features avançadas de conectividade"

# Ver status
git status

# Ver histórico
git log --oneline
```

### Convenção de Commits (Conventional Commits)

```bash
# Features
git commit -m "feat: Adiciona simulação Monte Carlo"

# Correções
git commit -m "fix: Corrige formato de data brasileiro"

# Documentação
git commit -m "docs: Atualiza README com instruções de validação"

# Refatoração
git commit -m "refactor: Melhora performance do cálculo de adjacências"

# Testes
git commit -m "test: Adiciona testes para features avançadas"

# Performance
git commit -m "perf: Otimiza loop de simulação Monte Carlo"
```

## GitHub/GitLab

### Conectar a um repositório remoto

```bash
# Adicionar remote
git remote add origin https://github.com/seu-usuario/megasena-analysis.git

# Verificar remote
git remote -v

# Push inicial
git push -u origin main
```

### Workflow Recomendado

```bash
# 1. Criar branch para nova feature
git checkout -b feature/nova-analise

# 2. Fazer mudanças e commits
git add .
git commit -m "feat: Implementa análise de clusters"

# 3. Push da branch
git push origin feature/nova-analise

# 4. Criar Pull Request no GitHub/GitLab

# 5. Após merge, atualizar main
git checkout main
git pull origin main

# 6. Deletar branch local
git branch -d feature/nova-analise
```

## Arquivos Ignorados (.gitignore)

Já configurado para ignorar:
- `.venv/` - Ambiente virtual
- `__pycache__/` - Cache Python
- `data/processed/*` - Dados processados (muito grandes)
- `*.xlsx` - Arquivo de dados bruto
- `reports/*` - Visualizações geradas

**Importante**: O arquivo `Mega-Sena.xlsx` NÃO será versionado (muito grande e pode ter copyright).

## Tags para Releases

```bash
# Criar tag
git tag -a v0.1.0 -m "Release 0.1.0: Pipeline básico funcional"

# Listar tags
git tag

# Push tags
git push origin --tags
```

## .gitignore Personalizado

Se precisar ignorar mais arquivos:

```bash
# Editar .gitignore
echo "novo-arquivo.log" >> .gitignore

# Commit
git add .gitignore
git commit -m "chore: Atualiza .gitignore"
```

## Revertendo Mudanças

```bash
# Descartar mudanças não commitadas
git checkout -- arquivo.py

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Desfazer último commit (descarta mudanças)
git reset --hard HEAD~1
```

## Boas Práticas

1. **Commits pequenos e frequentes**: Melhor que commits grandes
2. **Mensagens descritivas**: Explique o "porquê", não apenas o "o quê"
3. **Teste antes de commitar**: Execute `pytest` antes de cada commit
4. **Não versione dados grandes**: Use `.gitignore` apropriadamente
5. **Use branches**: Nunca trabalhe diretamente na main
6. **Pull antes de push**: Evite conflitos

## Exemplo de Workflow Completo

```bash
# 1. Criar nova branch
git checkout -b feature/validation-fdr

# 2. Fazer mudanças
# ... editar arquivos ...

# 3. Ver o que mudou
git diff

# 4. Adicionar mudanças
git add src/validation.py tests/test_validation.py

# 5. Commit
git commit -m "feat: Implementa correção FDR para múltiplas hipóteses"

# 6. Fazer mais mudanças
# ... editar documentação ...

# 7. Commit da documentação
git add docs/validation_plan.md
git commit -m "docs: Documenta metodologia FDR"

# 8. Push da branch
git push origin feature/validation-fdr

# 9. Criar Pull Request no GitHub

# 10. Após merge, voltar para main
git checkout main
git pull origin main

# 11. Limpar branch local
git branch -d feature/validation-fdr
```

## GitHub Actions (CI/CD)

Futuramente, você pode adicionar `.github/workflows/tests.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -v
```

---

**Pronto para começar!** Execute os comandos abaixo para o primeiro commit:

```bash
git add .
git commit -m "Initial commit: Pipeline completo de análise espacial da Mega-Sena"
```
