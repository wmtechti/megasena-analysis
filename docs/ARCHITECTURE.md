# Arquitetura do Sistema - LoteriaTech

> **Plataforma SaaS Multi-Loteria com Apps Nativos (iOS + Android)**

**Versão**: 1.0  
**Data**: Janeiro 2026  
**Status**: Planejamento/Documentação

---

## 📋 Sumário Executivo

### Objetivo
Plataforma completa de análise espacial estatística para todas as loterias da Caixa Econômica Federal, disponível como:
- 🌐 **Web App** (Progressive Web App)
- 📱 **iOS App** (App Store)
- 🤖 **Android App** (Google Play Store)

### Loterias Suportadas
1. ✅ **Mega-Sena** (implementado)
2. ✅ **Lotofácil** (implementado)
3. 🔲 Quina
4. 🔲 Dupla Sena
5. 🔲 Lotomania
6. 🔲 Timemania
7. 🔲 Dia de Sorte
8. 🔲 Super Sete

### Modelo de Negócio
- **SaaS (Software as a Service)**
- **Assinaturas recorrentes** (mensal/anual)
- **Freemium** (versão gratuita limitada)

---

## 🏗️ Arquitetura Geral

### Princípios Fundamentais

1. **Separação Total**: Backend ↔️ Frontend via API
2. **API-First**: Toda comunicação via REST/GraphQL
3. **Stateless Backend**: JWT para autenticação
4. **Mobile-First**: Design responsivo, PWA-ready
5. **Container Dinâmico**: Componentes modulares reutilizáveis
6. **Single Codebase**: Mesmo código para Web/iOS/Android

### Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web App    │  │   iOS App    │  │ Android App  │      │
│  │  (Next.js)   │  │ (Capacitor)  │  │ (Capacitor)  │      │
│  │     PWA      │  │  App Store   │  │  Play Store  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
│                            ▼                                │
├─────────────────────────────────────────────────────────────┤
│                       API GATEWAY                            │
│                  (Nginx / Cloudflare)                        │
│                    + Rate Limiting                           │
│                    + Load Balancer                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APLICAÇÃO                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────────────────────────────────────┐      │
│  │              Backend API (FastAPI)                 │      │
│  ├───────────────────────────────────────────────────┤      │
│  │                                                    │      │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────┐ │      │
│  │  │    Auth     │  │  Lotteries   │  │ Payments │ │      │
│  │  │  (JWT/OAuth)│  │   Engine     │  │  Stripe  │ │      │
│  │  └─────────────┘  └──────────────┘  └──────────┘ │      │
│  │                                                    │      │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────┐ │      │
│  │  │   Analysis  │  │  Monte Carlo │  │   Users  │ │      │
│  │  │   Spatial   │  │  Simulation  │  │  & Subs  │ │      │
│  │  └─────────────┘  └──────────────┘  └──────────┘ │      │
│  │                                                    │      │
│  └────────────────────────────────────────────────────┘      │
│                            │                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   CAMADA DE WORKERS                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Celery     │  │   Redis      │  │  Scheduler   │      │
│  │   Workers    │  │   Queue      │  │   (Cron)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  Jobs: Monte Carlo, Data Scraping, Email Notifications      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE DADOS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │    Redis     │  │      S3      │      │
│  │  (Primary)   │  │   (Cache)    │  │   (Files)    │      │
│  │              │  │              │  │              │      │
│  │ - Users      │  │ - Sessions   │  │ - Reports    │      │
│  │ - Draws      │  │ - Results    │  │ - Images     │      │
│  │ - Features   │  │ - Rate Limit │  │ - Exports    │      │
│  │ - Payments   │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Frontend - Mobile-First

### Stack Tecnológico

#### Opção Recomendada: **Capacitor + Next.js**

**Justificativa**:
- ✅ **Um único código** para Web + iOS + Android
- ✅ **Next.js** (React) - moderno, SEO, SSR
- ✅ **Capacitor** - bridge nativo (melhor que Cordova)
- ✅ **Deploy simples** - build uma vez, distribui 3x
- ✅ **Performance nativa** - 95% igual a React Native
- ✅ **Plugins nativos** - acesso a câmera, notificações, etc.

```
Frontend Stack:
├─ Next.js 14 (App Router)
├─ TypeScript
├─ Tailwind CSS (styling)
├─ shadcn/ui (componentes)
├─ Capacitor 5 (mobile bridge)
├─ Zustand (state management - leve!)
├─ React Query (data fetching)
└─ Framer Motion (animações)
```

### Estrutura de Containers Dinâmicos

```typescript
// app/layout.tsx - Layout raiz
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <DynamicShell>
          {children}
        </DynamicShell>
      </body>
    </html>
  )
}

// components/DynamicShell.tsx - Container dinâmico
export function DynamicShell({ children }) {
  const { lottery, view } = useAppState()
  
  return (
    <div className="app-shell">
      <Header lottery={lottery} />
      <Sidebar />
      <main className="dynamic-content">
        {children}
      </main>
      <BottomNav /> {/* Mobile only */}
    </div>
  )
}

// Componentes modulares por loteria
export function LotteryView({ lottery }: { lottery: LotteryType }) {
  const Component = LOTTERY_COMPONENTS[lottery]
  
  return (
    <Suspense fallback={<LoadingSkeleton />}>
      <Component />
    </Suspense>
  )
}
```

### Responsividade Mobile-First

```css
/* Breakpoints */
mobile: 320px - 768px   (base)
tablet: 768px - 1024px
desktop: 1024px+

/* Abordagem */
1. Design para mobile primeiro
2. Progressive enhancement para tablet/desktop
3. Touch-first (botões grandes, gestos)
4. Offline-first (PWA cache)
```

---

## ⚙️ Backend - API REST

### Stack Tecnológico

```
Backend Stack:
├─ FastAPI (Python 3.11+)
├─ SQLAlchemy (ORM)
├─ Alembic (migrations)
├─ Pydantic (validação)
├─ JWT (autenticação)
├─ Celery (tasks assíncronas)
├─ Redis (cache + queue)
└─ PostgreSQL (database)
```

### Estrutura de Diretórios

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configurações
│   │
│   ├── core/                   # Lógica de negócio compartilhada
│   │   ├── spatial.py          # Análise espacial genérica
│   │   ├── monte_carlo.py      # Simulação MC
│   │   ├── validation.py       # Validação estatística
│   │   └── features.py         # Extração de features
│   │
│   ├── lotteries/              # Implementações específicas
│   │   ├── __init__.py
│   │   ├── base.py             # Classe abstrata
│   │   ├── megasena.py         # ✅ Implementado
│   │   ├── lotofacil.py        # ✅ Implementado
│   │   ├── quina.py
│   │   ├── duplasena.py
│   │   ├── lotomania.py
│   │   ├── timemania.py
│   │   ├── diadesorte.py
│   │   └── supersete.py
│   │
│   ├── api/                    # Endpoints REST
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (auth, db)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py         # /auth/* (login, register)
│   │       ├── users.py        # /users/* (profile, settings)
│   │       ├── lotteries.py    # /lotteries/* (list, details)
│   │       ├── analysis.py     # /analysis/* (features, MC)
│   │       ├── games.py        # /games/* (generator)
│   │       └── payments.py     # /payments/* (subscriptions)
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── lottery.py
│   │   ├── draw.py
│   │   ├── subscription.py
│   │   └── analysis.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── lottery.py
│   │   ├── analysis.py
│   │   └── payment.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── lottery_service.py
│   │   ├── analysis_service.py
│   │   └── payment_service.py
│   │
│   ├── workers/                # Celery tasks
│   │   ├── __init__.py
│   │   ├── scraper.py          # Atualiza dados Caixa
│   │   ├── monte_carlo.py      # Simulações pesadas
│   │   └── notifications.py    # Emails, push
│   │
│   └── utils/
│       ├── __init__.py
│       ├── security.py         # Hash, JWT
│       └── scraper.py          # Web scraping Caixa
│
├── alembic/                    # Database migrations
├── tests/
├── .env.example
├── requirements.txt
└── Dockerfile
```

### API Design - RESTful

#### Autenticação
```
POST   /api/v1/auth/register       # Criar conta
POST   /api/v1/auth/login          # Login (retorna JWT)
POST   /api/v1/auth/refresh        # Refresh token
POST   /api/v1/auth/logout         # Invalidar token
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
```

#### Usuários
```
GET    /api/v1/users/me            # Perfil do usuário logado
PUT    /api/v1/users/me            # Atualizar perfil
GET    /api/v1/users/me/subscription # Status da assinatura
GET    /api/v1/users/me/history    # Histórico de apostas
```

#### Loterias
```
GET    /api/v1/lotteries           # Lista todas as loterias
GET    /api/v1/lotteries/{slug}    # Detalhes de uma loteria
GET    /api/v1/lotteries/{slug}/draws # Concursos históricos
GET    /api/v1/lotteries/{slug}/draws/{id} # Concurso específico
GET    /api/v1/lotteries/{slug}/stats # Estatísticas gerais
```

#### Análise
```
POST   /api/v1/analysis/{lottery}/features  # Calcular features
POST   /api/v1/analysis/{lottery}/monte-carlo # Simular MC
GET    /api/v1/analysis/{lottery}/validation # Resultados validação
GET    /api/v1/analysis/{lottery}/heatmap   # Dados do heatmap
```

#### Gerador de Jogos
```
POST   /api/v1/games/{lottery}/generate # Gerar jogos inteligentes
POST   /api/v1/games/{lottery}/validate # Validar jogo do usuário
POST   /api/v1/games/{lottery}/optimize # Otimizar bolão
```

#### Pagamentos
```
POST   /api/v1/payments/checkout       # Iniciar checkout
POST   /api/v1/payments/webhook        # Stripe/MP webhook
GET    /api/v1/payments/invoices       # Histórico de pagamentos
POST   /api/v1/payments/cancel         # Cancelar assinatura
```

### Autenticação - JWT

```python
# app/core/security.py
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# app/api/deps.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(
    token: str = Depends(security)
) -> User:
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY)
        user_id = payload["sub"]
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(401, "Invalid token")
        return user
    except:
        raise HTTPException(401, "Invalid token")
```

---

## 💾 Banco de Dados

### Schema PostgreSQL

```sql
-- Users & Authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE
);

-- Subscriptions
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    plan_type VARCHAR(50) NOT NULL, -- free, individual, multi, complete, pro
    status VARCHAR(50) NOT NULL, -- active, cancelled, expired
    started_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP,
    stripe_subscription_id VARCHAR(255),
    auto_renew BOOLEAN DEFAULT TRUE
);

-- Lotteries (metadata)
CREATE TABLE lotteries (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(50) UNIQUE NOT NULL, -- megasena, lotofacil, etc
    name VARCHAR(100) NOT NULL,
    grid_rows INTEGER NOT NULL,
    grid_cols INTEGER NOT NULL,
    draw_size INTEGER NOT NULL, -- quantos números sorteados
    is_active BOOLEAN DEFAULT TRUE
);

-- Draws (concursos históricos)
CREATE TABLE draws (
    id SERIAL PRIMARY KEY,
    lottery_id INTEGER REFERENCES lotteries(id),
    draw_number INTEGER NOT NULL,
    draw_date DATE NOT NULL,
    numbers INTEGER[] NOT NULL, -- {1,5,12,23,45,59}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(lottery_id, draw_number)
);

-- Features (pré-calculadas)
CREATE TABLE draw_features (
    id SERIAL PRIMARY KEY,
    draw_id INTEGER REFERENCES draws(id),
    centroid_row FLOAT,
    centroid_col FLOAT,
    dispersion FLOAT,
    q1 INTEGER,
    q2 INTEGER,
    q3 INTEGER,
    q4 INTEGER,
    border_count INTEGER,
    -- ... todas as 27 features
    features_json JSONB, -- backup completo
    created_at TIMESTAMP DEFAULT NOW()
);

-- Monte Carlo Results (cache)
CREATE TABLE monte_carlo_cache (
    id SERIAL PRIMARY KEY,
    lottery_id INTEGER REFERENCES lotteries(id),
    n_simulations INTEGER NOT NULL,
    baseline_stats JSONB NOT NULL, -- estatísticas por feature
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- User Games (apostas salvas)
CREATE TABLE user_games (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lottery_id INTEGER REFERENCES lotteries(id),
    numbers INTEGER[] NOT NULL,
    generated_by VARCHAR(50), -- manual, ai, random
    created_at TIMESTAMP DEFAULT NOW()
);

-- Analytics (tracking)
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes para performance
CREATE INDEX idx_draws_lottery_date ON draws(lottery_id, draw_date DESC);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_features_draw ON draw_features(draw_id);
```

### Cache Redis

```
Estrutura de chaves:

# Sessions
session:{user_id} → { token, expires_at }

# Rate limiting
ratelimit:{user_id}:{endpoint} → count (TTL: 1 minute)

# Cache de análises
analysis:{lottery}:{draw_id}:features → JSON
montecarlo:{lottery}:{n_sims}:stats → JSON

# Real-time
lottery:{lottery}:latest_draw → draw_number
```

---

## 📱 Estratégia Mobile

### Capacitor - Build & Deploy

```bash
# Desenvolvimento
npm run dev          # Next.js dev server

# Build para Web
npm run build        # Next.js production build

# Build para Mobile
npm run build
npx cap add ios      # Adiciona plataforma iOS
npx cap add android  # Adiciona plataforma Android
npx cap sync         # Sincroniza web assets

# Abrir IDEs nativas
npx cap open ios     # Xcode
npx cap open android # Android Studio

# Build final
# iOS: Xcode → Archive → Upload to App Store
# Android: Android Studio → Build → Generate Signed APK
```

### PWA (Progressive Web App)

```javascript
// next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development'
})

module.exports = withPWA({
  // Next.js config
})

// public/manifest.json
{
  "name": "LoteriaTech",
  "short_name": "LoteriaTech",
  "description": "Análise Espacial de Loterias",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#6366f1",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Plugins Nativos (Capacitor)

```typescript
// Notificações Push
import { PushNotifications } from '@capacitor/push-notifications';

await PushNotifications.requestPermissions();
await PushNotifications.register();

// Compartilhamento
import { Share } from '@capacitor/share';

await Share.share({
  title: 'Meu jogo da Mega-Sena',
  text: 'Confira meus números: 5, 12, 23, 35, 42, 58',
  url: 'https://loteriatech.com.br/share/xyz'
});

// Camera (para ler volantes físicos - futuro)
import { Camera } from '@capacitor/camera';

const photo = await Camera.getPhoto({
  quality: 90,
  allowEditing: false,
  resultType: CameraResultType.Uri
});
```

---

## 🚀 Deploy & Infrastructure

### Ambientes

```
Development:
├─ Frontend: localhost:3000
├─ Backend: localhost:8000
└─ Database: localhost:5432

Staging:
├─ Frontend: staging.loteriatech.com.br
├─ Backend: api-staging.loteriatech.com.br
└─ Database: AWS RDS (staging)

Production:
├─ Frontend: app.loteriatech.com.br
├─ Backend: api.loteriatech.com.br
└─ Database: AWS RDS (production)
```

### Stack de Deploy

```
Frontend:
├─ Vercel (Next.js) - $20/mês
│   ├─ Auto-deploy from main branch
│   ├─ CDN global
│   └─ Edge functions

Backend:
├─ Railway ou Render - $15-30/mês
│   ├─ Auto-deploy from main
│   ├─ Docker containers
│   └─ Auto-scaling

Database:
├─ Supabase (PostgreSQL) - $25/mês
│   ├─ Managed Postgres
│   ├─ Daily backups
│   └─ Connection pooling

Cache/Queue:
├─ Upstash (Redis) - $10/mês
│   ├─ Serverless Redis
│   └─ Global replication

Storage:
├─ Cloudflare R2 - $5/mês
│   └─ S3-compatible

CDN/DNS:
├─ Cloudflare - Free
│   ├─ DNS
│   ├─ CDN
│   └─ DDoS protection

Total estimado: ~$80/mês
```

### CI/CD - GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest
  
  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Railway
        run: railway up
  
  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Vercel
        run: vercel --prod
```

---

## 🔒 Segurança

### Checklist

- [ ] HTTPS obrigatório (TLS 1.3)
- [ ] JWT com refresh tokens
- [ ] Rate limiting (100 req/min por usuário)
- [ ] CORS configurado corretamente
- [ ] SQL injection prevention (SQLAlchemy)
- [ ] XSS prevention (React auto-escape)
- [ ] CSRF tokens
- [ ] Password hashing (bcrypt)
- [ ] 2FA (opcional, plano Pro)
- [ ] Logs de auditoria
- [ ] Backup diário do banco
- [ ] Monitoramento (Sentry)

---

## 📊 Monitoramento

```
Logs:
├─ Backend: Papertrail ou Logflare
├─ Frontend: Vercel Analytics
└─ Errors: Sentry

Metrics:
├─ Uptime: UptimeRobot (gratuito)
├─ Performance: Lighthouse CI
└─ Analytics: Plausible (GDPR-friendly)

Alertas:
├─ Email: SendGrid
├─ Slack: Webhooks
└─ On-call: PagerDuty (futuro)
```

---

## 📝 Próximos Passos

Ver documento: [ROADMAP.md](ROADMAP.md)

---

**Última atualização**: Janeiro 2026  
**Responsável**: Equipe de Arquitetura
