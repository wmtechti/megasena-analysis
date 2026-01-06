# LoteriaTech Frontend

Frontend Next.js 14 para plataforma de análise espacial de loterias brasileiras.

## 🚀 Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **HTTP Client**: Axios

## 📁 Estrutura

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   └── providers/          # Context providers
│   ├── lib/
│   │   ├── api.ts             # API service functions
│   │   ├── api-client.ts      # Axios configuration
│   │   ├── stores/            # Zustand stores
│   │   └── utils.ts           # Utilities
│   └── types/
│       └── index.ts           # TypeScript definitions
├── public/                     # Static assets
├── .env.local                 # Environment variables (local)
├── .env.example               # Environment template
├── components.json            # shadcn/ui config
├── tailwind.config.ts         # Tailwind configuration
└── tsconfig.json              # TypeScript config
```

## 🛠️ Setup

### Instalação

```bash
cd frontend
npm install
```

### Environment Variables

```bash
cp .env.example .env.local
```

Edite `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=LoteriaTech
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Rodar Desenvolvimento

```bash
npm run dev
```

Acesse: http://localhost:3000

### Build para Produção

```bash
npm run build
npm start
```

## 📦 Componentes shadcn/ui Instalados

- `button` - Botões estilizados
- `card` - Cards de conteúdo
- `input` - Campos de texto
- `label` - Labels para formulários
- `select` - Dropdowns
- `separator` - Separadores visuais
- `tabs` - Navegação por abas
- `table` - Tabelas de dados
- `badge` - Tags e badges
- `skeleton` - Loading states

### Adicionar Mais Componentes

```bash
npx shadcn@latest add [component-name]
```

## 🔗 API Integration

O frontend se conecta ao backend FastAPI através do `api-client.ts`.

### Exemplo de Uso

```typescript
import { lotteriesApi } from "@/lib/api";

// Listar loterias
const lotteries = await lotteriesApi.list();

// Buscar sorteios da Mega-Sena
const draws = await lotteriesApi.getDraws("megasena", 1, 50);

// Análise completa
const analysis = await lotteriesApi.getAnalysis("megasena");
```

### Com React Query

```typescript
import { useQuery } from "@tanstack/react-query";
import { lotteriesApi } from "@/lib/api";

function LotteryList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["lotteries"],
    queryFn: lotteriesApi.list,
  });

  if (isLoading) return <div>Carregando...</div>;
  if (error) return <div>Erro ao carregar loterias</div>;

  return (
    <div>
      {data?.map((lottery) => (
        <div key={lottery.id}>{lottery.name}</div>
      ))}
    </div>
  );
}
```

## 🔐 Autenticação

O frontend usa Zustand para gerenciar estado de autenticação:

```typescript
import { useAuthStore } from "@/lib/stores/auth-store";

function Profile() {
  const { user, isAuthenticated, isPremium } = useAuthStore();

  if (!isAuthenticated()) {
    return <div>Faça login</div>;
  }

  return (
    <div>
      <h1>Olá, {user?.name}</h1>
      {isPremium() && <p>Usuário Premium ✨</p>}
    </div>
  );
}
```

## 📱 Responsividade

O design é mobile-first com breakpoints do Tailwind:

- `sm`: 640px (mobile landscape)
- `md`: 768px (tablet)
- `lg`: 1024px (desktop)
- `xl`: 1280px (large desktop)

## 🎨 Customização

### Cores (Tailwind)

Edite `tailwind.config.ts` para customizar paleta de cores.

### Componentes shadcn/ui

Componentes estão em `src/components/ui/` e podem ser editados diretamente.

## 📊 Features Implementadas

### ✅ Página Inicial
- Hero section com branding
- Cards de status (API health check)
- Links para loterias e login
- Footer

### 🔄 Próximas Features
- [ ] Página de listagem de loterias
- [ ] Página de detalhes de loteria
- [ ] Visualização de sorteios
- [ ] Gráficos de frequência
- [ ] Sistema de autenticação (login/registro)
- [ ] Dashboard do usuário
- [ ] Planos e assinaturas
- [ ] Análise avançada com features espaciais

## 🚢 Deploy

### Vercel (Recomendado)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Outras Plataformas
- **Netlify**: Conectar repositório GitHub
- **Railway**: Suporta Next.js automaticamente
- **AWS Amplify**: CI/CD integrado

## 📝 Scripts

```bash
npm run dev          # Desenvolvimento (Turbopack)
npm run build        # Build produção
npm run start        # Rodar build de produção
npm run lint         # ESLint
```

## 🔍 TypeScript

Strict mode habilitado para máxima segurança de tipos.

Tipos principais em `src/types/index.ts`:
- `User`, `UserRole`, `AuthToken`
- `Lottery`, `Draw`, `DrawFeature`
- `NumberFrequency`, `LotteryAnalysis`

## 🤝 Integração com Backend

### Backend deve estar rodando em:
- Desenvolvimento: `http://localhost:8000`
- Produção: Configurar via `NEXT_PUBLIC_API_URL`

### Endpoints Esperados:
- `GET /health` - Health check
- `GET /api/v1/lotteries` - Listar loterias
- `GET /api/v1/lotteries/{slug}` - Detalhes
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registro

## 📚 Documentação

- [Next.js Docs](https://nextjs.org/docs)
- [shadcn/ui](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TanStack Query](https://tanstack.com/query)
- [Zustand](https://zustand-demo.pmnd.rs)

## 🐛 Troubleshooting

### Erro de CORS
Certifique-se que o backend está configurado com CORS para `http://localhost:3000`.

### API não conecta
Verifique se `NEXT_PUBLIC_API_URL` está correto no `.env.local`.

### Componentes shadcn não funcionam
Execute `npx shadcn@latest init` novamente.

---

**Desenvolvido com ❤️ para análise de loterias brasileiras**
