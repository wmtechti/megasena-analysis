# Backend - LoteriaTech API

## 🗄️ Suporte Multi-Database

Este backend suporta **3 tipos de banco de dados**:
- ✅ **PostgreSQL** (local ou cloud)
- ✅ **Supabase** (PostgreSQL gerenciado)
- ✅ **MS SQL Server** (para clientes enterprise)

## 📦 Instalação

### 1. Criar ambiente virtual

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar banco de dados

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite `.env` e escolha seu banco:

#### Opção A: PostgreSQL Local
```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@localhost:5432/loteriatech
```

#### Opção B: Supabase
```env
DATABASE_TYPE=supabase
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
SUPABASE_URL=https://[PROJECT].supabase.co
SUPABASE_KEY=your-anon-key
```

#### Opção C: MS SQL Server
```env
DATABASE_TYPE=mssql
DATABASE_URL=mssql+pyodbc://user:password@server:1433/loteriatech?driver=ODBC+Driver+17+for+SQL+Server
```

### 4. Executar migrations

```bash
alembic upgrade head
```

### 5. Iniciar servidor

```bash
# Desenvolvimento (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🧪 Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Específico
pytest tests/test_lotteries.py
```

## 📚 Documentação API

Após iniciar o servidor:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 Scripts Úteis

```bash
# Criar nova migration
alembic revision --autogenerate -m "descrição"

# Ver status das migrations
alembic current

# Reverter última migration
alembic downgrade -1

# Popular banco com dados históricos
python scripts/seed_data.py
```

## 🗂️ Estrutura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configurações (multi-DB)
│   │
│   ├── core/                   # Lógica compartilhada
│   │   ├── spatial.py          # Análise espacial
│   │   ├── monte_carlo.py      # Simulação
│   │   └── features.py         # Extração de features
│   │
│   ├── lotteries/              # Implementações por loteria
│   │   ├── base.py             # Classe abstrata
│   │   ├── megasena.py         # Mega-Sena
│   │   └── lotofacil.py        # Lotofácil
│   │
│   ├── api/                    # Endpoints REST
│   │   ├── deps.py             # Dependencies
│   │   └── v1/
│   │       ├── lotteries.py
│   │       └── analysis.py
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── base.py
│   │   ├── lottery.py
│   │   └── draw.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   └── lottery.py
│   │
│   └── db/                     # Database utilities
│       ├── base.py
│       └── session.py
│
├── alembic/                    # Migrations
├── tests/
├── requirements.txt
└── .env
```

## 🌍 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_TYPE` | Tipo de banco (postgresql, supabase, mssql) | postgresql |
| `DATABASE_URL` | Connection string | - |
| `SECRET_KEY` | Chave JWT | - |
| `ENVIRONMENT` | dev, staging, production | dev |
| `CORS_ORIGINS` | URLs permitidas (separadas por vírgula) | http://localhost:3000 |

## 📊 Performance

- **Latência média**: < 50ms (cache ativo)
- **Throughput**: 1000 req/s (single worker)
- **Cache**: Redis (opcional, recomendado para produção)

## 🔒 Segurança

- ✅ HTTPS obrigatório (produção)
- ✅ CORS configurável
- ✅ Rate limiting
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Validação de entrada (Pydantic)
