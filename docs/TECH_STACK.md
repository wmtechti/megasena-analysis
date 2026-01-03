# Stack Tecnológico - LoteriaTech

> **Decisões Técnicas e Justificativas**

**Versão**: 1.0  
**Data**: Janeiro 2026

---

## 🎯 Premissas de Decisão

### Critérios de Seleção
1. **Mobile-First**: Um código para Web + iOS + Android
2. **Performance**: Latência < 200ms, bundle < 500KB
3. **Developer Experience**: Produtividade e manutenibilidade
4. **Custo**: Otimização de infraestrutura (bootstrap friendly)
5. **Ecossistema**: Comunidade ativa, bibliotecas maduras
6. **Escalabilidade**: Preparado para 10k+ usuários

---

## 🎨 Frontend Stack

### Next.js 14 ✅

**Por quê?**
- ✅ **SSR + SSG**: SEO perfeito, performance
- ✅ **App Router**: Roteamento moderno, server components
- ✅ **API Routes**: Backend leve embutido
- ✅ **Image Optimization**: Lazy loading automático
- ✅ **Vercel Deploy**: Deploy grátis (até certo ponto)

**Alternativas Consideradas**:
- ❌ Create React App: Sem SSR, obsoleto
- ❌ Remix: Menos maduro, ecossistema menor
- ⚠️ Astro: Ótimo, mas menos suporte mobile

```bash
# Instalação
npx create-next-app@latest frontend --typescript --tailwind --app
```

### TypeScript ✅

**Por quê?**
- ✅ **Type Safety**: Menos bugs em runtime
- ✅ **IntelliSense**: Autocomplete, refactoring
- ✅ **Documentação**: Tipos como contrato
- ✅ **Escalabilidade**: Essencial para times

**Configuração**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Tailwind CSS ✅

**Por quê?**
- ✅ **Utility-First**: Desenvolvimento rápido
- ✅ **Mobile-First**: Breakpoints nativos
- ✅ **Bundle Small**: PurgeCSS automático
- ✅ **Design System**: Fácil padronização
- ✅ **Dark Mode**: Suporte nativo

**Alternativas**:
- ❌ styled-components: Runtime overhead
- ❌ CSS Modules: Menos flexível
- ⚠️ Chakra UI: Bom, mas bundle maior

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  content: ['./app/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#6366f1',
        secondary: '#ec4899'
      }
    }
  }
}
```

### shadcn/ui ✅

**Por quê?**
- ✅ **Copy-Paste**: Sem dependência npm
- ✅ **Customizável**: Código fonte visível
- ✅ **Acessibilidade**: Radix UI por baixo
- ✅ **Beautiful**: Design moderno, polido

**Componentes Usados**:
```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add select
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add toast
```

### Zustand (State Management) ✅

**Por quê?**
- ✅ **Simples**: 1KB, sem boilerplate
- ✅ **Performático**: Re-renders otimizados
- ✅ **DevTools**: Redux DevTools compatível
- ✅ **TypeScript**: First-class support

**Alternativas**:
- ❌ Redux Toolkit: Muito boilerplate
- ❌ Context API: Performance issues
- ⚠️ Jotai: Bom, mas atômico demais

```typescript
// stores/app-store.ts
import { create } from 'zustand'

interface AppState {
  currentLottery: string
  setCurrentLottery: (lottery: string) => void
}

export const useAppStore = create<AppState>((set) => ({
  currentLottery: 'megasena',
  setCurrentLottery: (lottery) => set({ currentLottery: lottery })
}))
```

### React Query (TanStack Query) ✅

**Por quê?**
- ✅ **Data Fetching**: Cache, retry, refetch
- ✅ **Mutations**: Otimistic updates
- ✅ **Offline**: Persist state
- ✅ **DevTools**: Debug excelente

```typescript
// hooks/use-lottery-data.ts
import { useQuery } from '@tanstack/react-query'

export function useLotteryData(lottery: string) {
  return useQuery({
    queryKey: ['lottery', lottery],
    queryFn: () => fetch(`/api/lotteries/${lottery}`).then(r => r.json()),
    staleTime: 5 * 60 * 1000, // 5 min
    cacheTime: 10 * 60 * 1000 // 10 min
  })
}
```

### Framer Motion ✅

**Por quê?**
- ✅ **Animações**: Smooth, declarativo
- ✅ **Gestos**: Drag, swipe para mobile
- ✅ **Layout Animations**: Automático
- ✅ **Performance**: GPU-accelerated

```typescript
import { motion } from 'framer-motion'

export function LotteryCard({ lottery }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      {/* conteúdo */}
    </motion.div>
  )
}
```

---

## 📱 Mobile Stack

### Capacitor 5 ✅

**Por quê?**
- ✅ **Web-to-Native**: Reutiliza Next.js 100%
- ✅ **Performance**: 95% de app nativo
- ✅ **Plugins**: Acesso APIs nativas
- ✅ **Live Updates**: Sem review de loja
- ✅ **Comunidade**: Ionic backing

**Alternativas**:
- ❌ React Native: Código separado
- ❌ Flutter: Dart (outra linguagem)
- ❌ Cordova: Desatualizado
- ⚠️ Tauri: Novo demais

```bash
# Setup
npm install @capacitor/core @capacitor/cli
npx cap init
npx cap add ios
npx cap add android

# Sync
npx cap sync

# Open IDEs
npx cap open ios
npx cap open android
```

### Capacitor Plugins Essenciais

```bash
npm install @capacitor/push-notifications
npm install @capacitor/share
npm install @capacitor/haptics
npm install @capacitor/status-bar
npm install @capacitor/splash-screen
npm install @capacitor/app
npm install @capacitor/keyboard
```

### PWA (Progressive Web App) ✅

```bash
npm install next-pwa
```

**Benefícios**:
- ✅ Instalável (Add to Home Screen)
- ✅ Offline-first (Service Worker)
- ✅ Push notifications (web)
- ✅ App-like experience

---

## ⚙️ Backend Stack

### FastAPI (Python 3.11+) ✅

**Por quê?**
- ✅ **Performance**: Async, rápido como Node.js
- ✅ **Type Hints**: Validação automática (Pydantic)
- ✅ **OpenAPI**: Documentação automática
- ✅ **Async**: Suporta WebSockets
- ✅ **Reutilização**: Aproveita código existente!

**Alternativas**:
- ❌ Django: Muito pesado
- ❌ Flask: Sem async nativo
- ❌ Node.js: Melhor usar Python (já temos código)

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="LoteriaTech API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.loteriatech.com.br"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### SQLAlchemy 2.0 ✅

**Por quê?**
- ✅ **ORM Maduro**: Python padrão
- ✅ **Type Safety**: Com Pydantic
- ✅ **Migrations**: Alembic integrado
- ✅ **Performance**: Lazy loading, eager loading

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    subscriptions = relationship("Subscription", back_populates="user")
```

### Pydantic v2 ✅

**Por quê?**
- ✅ **Validação**: Automática, declarativa
- ✅ **Serialização**: JSON automático
- ✅ **Type Hints**: Python nativo
- ✅ **Performance**: Rust-powered (v2)

```python
# app/schemas/lottery.py
from pydantic import BaseModel, Field
from typing import List

class LotteryBase(BaseModel):
    slug: str = Field(..., pattern="^[a-z]+$")
    name: str = Field(..., min_length=3)
    grid_rows: int = Field(..., gt=0)
    grid_cols: int = Field(..., gt=0)

class LotteryCreate(LotteryBase):
    pass

class LotteryRead(LotteryBase):
    id: int
    
    class Config:
        from_attributes = True  # v2 (era orm_mode)
```

### Celery + Redis ✅

**Por quê?**
- ✅ **Tasks Assíncronas**: Monte Carlo, scraping
- ✅ **Scheduled Jobs**: Cron-like
- ✅ **Escalável**: Múltiplos workers
- ✅ **Retry**: Automático

```python
# app/workers/celery_app.py
from celery import Celery

celery_app = Celery(
    "loteriatech",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

@celery_app.task
def run_monte_carlo(lottery_id: int, n_simulations: int):
    # Simular em background
    result = simulate_monte_carlo(lottery_id, n_simulations)
    return result
```

### Alembic (Migrations) ✅

```bash
# Inicializar
alembic init alembic

# Criar migration
alembic revision --autogenerate -m "create users table"

# Aplicar
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 💾 Database Stack

### PostgreSQL 15+ ✅

**Por quê?**
- ✅ **Confiável**: Padrão industria
- ✅ **JSONB**: Flexibilidade NoSQL
- ✅ **Full-Text Search**: Busca avançada
- ✅ **Performance**: Índices, particionamento
- ✅ **Extensões**: PostGIS (geo), pg_trgm

**Alternativas**:
- ❌ MySQL: Menos features
- ❌ MongoDB: Não relacional (não ideal)
- ⚠️ Supabase: Ótimo (PostgreSQL managed)

```sql
-- Exemplo: Índice para busca rápida
CREATE INDEX idx_draws_lottery_date 
ON draws(lottery_id, draw_date DESC);

-- JSONB para features
CREATE TABLE draw_features (
    id SERIAL PRIMARY KEY,
    draw_id INTEGER,
    features JSONB,
    centroid_row FLOAT GENERATED ALWAYS AS ((features->>'centroid_row')::float) STORED
);

-- Índice em JSONB
CREATE INDEX idx_features_centroid ON draw_features USING btree(centroid_row);
```

### Redis 7+ ✅

**Por quê?**
- ✅ **Cache**: Sub-ms latency
- ✅ **Queue**: Celery broker
- ✅ **Sessions**: JWT blacklist
- ✅ **Rate Limiting**: Contador

```python
import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

# Cache
redis_client.setex('analysis:megasena:123', 3600, json.dumps(data))

# Rate limiting
key = f'ratelimit:{user_id}:analysis'
count = redis_client.incr(key)
if count == 1:
    redis_client.expire(key, 60)  # 60 requests/min
if count > 60:
    raise RateLimitExceeded()
```

---

## 🔐 Autenticação & Segurança

### JWT (JSON Web Tokens) ✅

```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "seu-secret-super-seguro"
ALGORITHM = "HS256"

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=30),
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

### Bcrypt (Password Hashing) ✅

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

---

## 💳 Pagamentos

### Stripe ✅

**Por quê?**
- ✅ **Global**: Aceita internacional
- ✅ **Documentação**: Excelente
- ✅ **Webhooks**: Confiáveis
- ✅ **Customer Portal**: Self-service

```python
import stripe

stripe.api_key = "sk_test_..."

# Criar checkout
checkout_session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': 'price_xxx',  # Plano Individual
        'quantity': 1
    }],
    mode='subscription',
    success_url='https://app.loteriatech.com.br/success',
    cancel_url='https://app.loteriatech.com.br/cancel'
)
```

### Mercado Pago (Alternativa Brasil) ⚠️

Para clientes que preferem Pix, boleto.

---

## 🚀 Deploy & Infraestrutura

### Vercel (Frontend) ✅

- ✅ Free tier generoso
- ✅ Deploy automático (git push)
- ✅ Edge functions
- ✅ CDN global

### Railway (Backend) ✅

- ✅ $5/mês (starter)
- ✅ PostgreSQL incluso
- ✅ Auto-deploy
- ✅ Environment variables

**Alternativa**: Render.com

### Upstash (Redis) ✅

- ✅ Serverless Redis
- ✅ Pay-per-request
- ✅ Tier grátis

---

## 📦 Resumo da Stack

```
Frontend:
├─ Next.js 14 (React 18)
├─ TypeScript
├─ Tailwind CSS
├─ shadcn/ui
├─ Zustand (state)
├─ React Query (data)
└─ Framer Motion (animations)

Mobile:
├─ Capacitor 5
└─ PWA (next-pwa)

Backend:
├─ FastAPI (Python 3.11+)
├─ SQLAlchemy 2.0
├─ Pydantic v2
├─ Celery + Redis
└─ Alembic (migrations)

Database:
├─ PostgreSQL 15
└─ Redis 7

Deploy:
├─ Vercel (frontend)
├─ Railway (backend)
└─ Upstash (redis)

Payments:
├─ Stripe
└─ Mercado Pago (opcional)

Monitoring:
├─ Sentry (errors)
├─ Plausible (analytics)
└─ UptimeRobot (uptime)
```

---

**Última atualização**: Janeiro 2026
