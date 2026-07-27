# InsuRateForge — RateForge Platform

> A production-ready, enterprise-grade insurance pricing platform built with Domain-Driven Design and Clean Architecture.

[![CI](https://github.com/youngbad/InsuRateForge/actions/workflows/ci.yml/badge.svg)](https://github.com/youngbad/InsuRateForge/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Vue 3](https://img.shields.io/badge/vue-3-green.svg)](https://vuejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**RateForge** is a modular, plugin-based insurance pricing monorepo. It provides a full-stack
platform for managing insurance products, calculating quotes, running portfolio batches, handling
renewals and endorsements, and monitoring the system in real time.

### Key Features

| Feature | Details |
|---|---|
| **Pricing Engine** | Pluggable pipeline: validate → normalize → rate → discount → tax → fee → output |
| **Product Plugins** | Each plugin implements `validate()`, `calculate()`, `renew()`, `endorsement()`, `summary()` |
| **Versioned Products** | Historical quotes always use their original rating model |
| **Auth** | JWT access + refresh tokens with full RBAC |
| **Observability** | OpenTelemetry traces, Prometheus metrics, structured JSON logs |
| **Background Jobs** | Dramatiq workers backed by RabbitMQ |
| **Caching** | Redis for quote results and session data |
| **Enterprise UI** | Vue 3 SPA with sidebar, dashboards, charts, dark/light mode |

---

## Architecture

```
InsuRateForge/
├── backend/                    # Python / FastAPI service
│   ├── src/rateforge/
│   │   ├── domain/             # Entities, value objects, repository interfaces
│   │   ├── application/        # Use cases, DTOs, commands & queries
│   │   ├── infrastructure/     # SQLAlchemy, Redis, RabbitMQ, observability
│   │   └── presentation/       # FastAPI routers, middleware, schemas
│   ├── plugins/
│   │   └── motor/              # Sample Motor Insurance product plugin
│   ├── alembic/                # Database migrations
│   └── tests/
├── frontend/                   # Vue 3 / TypeScript SPA
│   └── src/
│       ├── api/                # Axios API clients
│       ├── stores/             # Pinia state (auth, theme, notifications)
│       ├── composables/        # TanStack Query composables
│       ├── layouts/            # DefaultLayout (sidebar) + AuthLayout
│       ├── components/         # Shared UI components & charts
│       └── views/              # Page views (Dashboard, Quotes, Portfolio…)
├── infrastructure/
│   ├── nginx/                  # Nginx reverse-proxy configs
│   └── prometheus/             # Prometheus scrape config
├── docker-compose.yml          # Full stack orchestration
├── docker-compose.override.yml # Dev overrides (hot-reload volumes)
├── .github/workflows/          # CI (lint+test) and CD (deploy on tag)
└── .pre-commit-config.yaml     # Code quality hooks
```

### DDD Layers (Backend)

```
domain/          ← Pure business logic — no framework dependencies
application/     ← Orchestrates domain objects; defines use-case boundaries
infrastructure/  ← Adapters: database, cache, messaging, observability
presentation/    ← FastAPI routers, request/response schemas, middleware
```

---

## Tech Stack

### Backend
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 | Language |
| FastAPI | ≥0.115 | HTTP framework |
| Pydantic v2 | ≥2.8 | Validation & settings |
| SQLAlchemy | ≥2.0 | Async ORM |
| asyncpg | ≥0.29 | PostgreSQL async driver |
| Alembic | ≥1.13 | Database migrations |
| Redis | ≥5.0 | Cache |
| RabbitMQ + Dramatiq | ≥1.17 | Background tasks |
| python-jose | ≥3.3 | JWT auth |
| passlib[bcrypt] | ≥1.7 | Password hashing |
| OpenTelemetry | ≥1.26 | Distributed tracing |
| prometheus-client | ≥0.20 | Metrics |
| structlog | ≥24.4 | Structured logging |
| uv | latest | Package manager |
| Ruff | ≥0.5 | Linting & formatting |
| MyPy | ≥1.11 | Type checking |
| Pytest | ≥8.3 | Testing |

### Frontend
| Tool | Version | Purpose |
|---|---|---|
| Vue 3 | ≥3.5 | UI framework |
| TypeScript | ≥5.5 | Type safety |
| Vite | ≥5.4 | Build tool |
| Pinia | ≥2.2 | State management |
| Vue Router | ≥4.4 | Client-side routing |
| TanStack Query | ≥5.59 | Server state |
| PrimeVue | ≥4.1 | UI component library |
| ApexCharts | ≥3.54 | Charts |
| Axios | ≥1.7 | HTTP client |

### Infrastructure
| Tool | Purpose |
|---|---|
| Docker + Compose | Container orchestration |
| PostgreSQL 16 | Primary database |
| Redis 7 | Cache & session store |
| RabbitMQ 3 | Message broker |
| Nginx | Reverse proxy |
| Prometheus + Grafana | Metrics & dashboards |
| GitHub Actions | CI/CD |
| pre-commit | Git hooks |

---

## Quick Start

### Prerequisites

- Docker ≥ 26 and Docker Compose ≥ 2
- Node.js ≥ 20 (for local frontend development)
- Python ≥ 3.13 and `uv` (for local backend development)

### 1. Clone & configure

```bash
git clone https://github.com/youngbad/InsuRateForge.git
cd InsuRateForge
cp .env.example .env          # edit values as needed
```

### 2. Start with Docker Compose

```bash
# Start all services (postgres, redis, rabbitmq, backend, worker, frontend, nginx, prometheus, grafana)
docker compose up -d

# Follow logs
docker compose logs -f backend worker
```

Services:
| Service | URL |
|---|---|
| Frontend (SPA) | http://localhost |
| Backend API | http://localhost/api/v1 |
| API Docs (Swagger) | http://localhost/api/v1/docs |
| Prometheus metrics | http://localhost:9090 |
| Grafana | http://localhost:3000 (admin / changeme) |
| RabbitMQ management | http://localhost:15672 (guest / guest) |

### 3. Run database migrations

```bash
docker compose exec backend alembic upgrade head
```

---

## Local Development

### Backend

```bash
cd backend

# Install dependencies with uv
uv sync --all-extras

# Copy environment config
cp .env.example .env

# Run migrations (requires Postgres to be running)
uv run alembic upgrade head

# Start the dev server
uv run uvicorn rateforge.main:app --reload --port 8000

# Lint & format
uv run ruff check src tests plugins --fix
uv run ruff format src tests plugins

# Type check
uv run mypy src

# Run tests
uv run pytest tests/ -v
```

### Frontend

```bash
cd frontend

npm install

# Start dev server (proxies /api → http://localhost:8000)
npm run dev

# Type check
npm run type-check

# Lint
npm run lint

# Build
npm run build
```

---

## Modules

### Pricing Engine

The core of RateForge is a fully pluggable pipeline:

```
PricingPipeline
  ├── ValidationStage     — delegates to plugin.validate()
  ├── NormalizeStage      — sanitises & coerces input
  ├── RateStage           — delegates to plugin.calculate()
  ├── DiscountStage       — applies recommended discounts
  ├── TaxStage            — applies insurance taxes
  ├── FeeStage            — adds policy fees
  └── OutputStage         — assembles final PricingResult
```

### Product Plugins

Each plugin lives in `backend/plugins/<slug>/` and implements the `ProductPlugin` interface:

```python
class ProductPlugin(ABC):
    @abstractmethod
    def validate(self, payload: dict) -> dict: ...       # validate & coerce input
    @abstractmethod
    def calculate(self, payload: dict) -> dict: ...      # compute base premium + factors
    @abstractmethod
    def renew(self, existing_quote: dict) -> dict: ...   # generate renewal payload
    @abstractmethod
    def endorsement(self, existing_quote: dict, changes: dict) -> dict: ...
    @abstractmethod
    def summary(self, payload: dict) -> dict: ...        # human-readable summary
```

The included **Motor Insurance** plugin (`plugins/motor/`) demonstrates a full implementation.

### API Endpoints

All endpoints are versioned under `/api/v1/`:

| Group | Endpoints |
|---|---|
| Auth | `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout` |
| Users | `GET/POST /users`, `GET/PATCH/DELETE /users/{id}` |
| Products | `GET/POST /products`, `GET /products/{slug}/{version}` |
| Quotes | `GET/POST /quotes`, `GET/PATCH /quotes/{id}` |
| Pricing | `POST /pricing/calculate`, `POST /pricing/renew`, `POST /pricing/endorse` |
| Portfolio | `GET/POST /portfolio/runs`, `GET /portfolio/runs/{id}` |
| Renewals | `GET/POST /renewals` |
| Endorsements | `GET/POST /endorsements` |
| Audit | `GET /audit/logs` |
| Metrics | `GET /metrics/summary` |

---

## Frontend Views

| Route | View | Description |
|---|---|---|
| `/login` | LoginView | JWT authentication |
| `/` | DashboardView | KPI cards, revenue chart, product mix |
| `/quotes` | QuotesListView | Filterable/sortable quote table |
| `/quotes/:id` | QuoteDetailView | Quote form + pricing breakdown |
| `/products` | ProductsListView | Product catalogue |
| `/products/:id` | ProductDetailView | Product details + version history |
| `/portfolio` | PortfolioView | Portfolio run management |
| `/admin` | AdminView | User & role management |
| `/analytics` | AnalyticsView | Reporting & analytics charts |
| `/monitoring` | MonitoringView | System health & metrics |

---

## Environment Variables

See `.env.example` for the full list. Key variables:

```bash
DATABASE_URL=******localhost:5432/rateforge
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=******localhost:5672/
SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

## Testing

```bash
# Backend unit + integration tests
cd backend && uv run pytest tests/ -v --cov=src/rateforge

# Frontend type check
cd frontend && npm run type-check
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Install pre-commit hooks: `pre-commit install`
4. Make changes, ensure tests pass
5. Open a pull request against `develop`

---

## License

MIT — see [LICENSE](LICENSE).