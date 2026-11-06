# Pink Wheels

**Safe rides. Fair prices.**

Pink Wheels is a women-only bike ride-hailing platform, initially launching in Karachi, Pakistan.
It connects verified women passengers with verified women drivers, offering an affordable
alternative to car bookings (target fare ~PKR 250–270 for short journeys) with safety as the
core design principle.

## Business concept

- Only eligible, verified women can register as passengers or drivers.
- Consent-based, human-reviewed eligibility verification (no AI gender guessing).
- Bike rides at a fraction of car-hailing prices.
- Architecture designed for Karachi first, expandable to other Pakistani cities.

## Technology stack

| Layer      | Technology |
|------------|------------|
| Frontend   | Vue 3, Vite, JavaScript, Tailwind CSS, Vue Router, Pinia, Axios, Leaflet, Lucide icons |
| Backend    | Python, FastAPI, SQLAlchemy, Pydantic, Alembic, JWT, WebSockets, Pytest |
| Database   | PostgreSQL |
| Maps       | OpenStreetMap, Leaflet, OSMnx, custom graph + custom Dijkstra implementation |
| DevOps     | Git, GitHub, Docker, Docker Compose, environment variables, Nginx (production) |

## Project structure

```
pink-wheels/
├── frontend/          # Vue 3 + Vite + Tailwind application
├── backend/           # FastAPI application
│   └── app/
│       ├── api/       # REST route handlers
│       ├── core/      # Config, security, permissions, logging
│       ├── database/  # Engine, session, Base
│       ├── models/    # SQLAlchemy models
│       ├── schemas/   # Pydantic schemas
│       ├── repositories/
│       ├── services/  # Business logic
│       ├── dsa/       # Linked list, priority queue, graph, dijkstra, stack
│       ├── routing/   # OSM service, road network, routing service
│       ├── security/  # Document storage, token service
│       └── websocket/ # Real-time ride updates
├── docs/              # Architecture, API, DSA, security and deployment docs
├── scripts/           # Helper scripts
├── docker-compose.yml
└── Dockerfile
```

## Prerequisites

- Node.js 20+ and npm
- Python 3.12+ (a 3.13 venv is recommended; see `Dockerfile`)
- PostgreSQL 16 (easiest via Docker Compose), or temporarily SQLite for a quick check
- Docker + Docker Compose (optional, for one-command local environment)

## Local setup

### 1. Environment variables

```bash
cp .env.example backend/.env
# Edit backend/.env — set DATABASE_URL and JWT_SECRET at minimum
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head             # run database migrations
uvicorn app.main:app --reload    # serves at http://localhost:8000
```

Interactive API documentation (Swagger UI): http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev                      # serves at http://localhost:5173
```

The frontend expects the backend at `VITE_API_URL` (default `http://localhost:8000`).

### 4. One-command environment with Docker

```bash
docker compose up --build
```

This starts PostgreSQL, runs Alembic migrations, and serves the backend (8000)
and frontend (5173).

## Verification

- Backend health: `curl http://localhost:8000/api/health` → `{"status":"ok","database":"connected"}`
- Frontend landing page shows live backend/database status and a re-check button.

## Testing

```bash
cd backend && pytest
cd frontend && npm run test
```

## Documentation

See the [`docs/`](docs/) folder:

- `architecture.md` — system design and module boundaries
- `database-design.md` — schema, constraints, indexes
- `api-documentation.md` — REST API contracts
- `dsa-explanation.md` / `dijkstra-explanation.md` — the four custom data structures
- `authentication-flow.md` — OTP, JWT, refresh rotation
- `verification-policy.md` — women-only eligibility workflow
- `security.md` — security controls
- `setup-guide.md` / `deployment.md` — local and production deployment

## License

MIT — see [LICENSE](LICENSE).
