# Copilot Instructions - Lottery Analysis Platform

## Project Overview
Full-stack SaaS platform for Brazilian lottery analysis with spatial statistics.

**Stack:**
- Backend: FastAPI + SQLAlchemy (PostgreSQL/Supabase/MSSQL)
- Frontend: Next.js 14 + TypeScript + Tailwind + shadcn/ui
- Mobile: Capacitor 5 (iOS/Android)

## Architecture
- API-First architecture
- Multi-database support (PostgreSQL, Supabase, MS SQL Server)
- Multi-tenant ready
- Freemium model (Free, Individual R$14.90, Multi R$29.90, Complete R$49.90)

## Lotteries Supported
1. ✅ Mega-Sena (10×6 grid, 60 numbers)
2. ✅ Lotofácil (5×5 grid, 25 numbers)
3. Quina
4. Dupla Sena
5. Lotomania
6. Timemania
7. Dia de Sorte
8. Super Sete

## Backend Structure
```
backend/
├── app/
│   ├── models/ (SQLAlchemy)
│   ├── schemas/ (Pydantic)
│   ├── lotteries/ (LotteryBase ABC + implementations)
│   ├── api/v1/ (FastAPI routes)
│   └── services/ (business logic)
```

## Frontend Structure (Next.js 14)
```
frontend/
├── app/ (App Router)
├── components/ (shadcn/ui components)
├── lib/ (API client, Zustand stores)
└── types/ (TypeScript definitions)
```

## Development Guidelines
- Use TypeScript strict mode
- Follow REST API conventions
- Database-agnostic code (no PostgreSQL-specific features)
- Mobile-first responsive design
- Accessibility (WCAG 2.1 AA)
