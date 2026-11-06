#!/usr/bin/env bash
# Start backend + frontend for local development (requires backend/.env configured).
set -e
cd "$(dirname "$0")/.."

(cd backend && source .venv/bin/activate && uvicorn app.main:app --reload) &
BACKEND_PID=$!
trap "kill $BACKEND_PID" EXIT

(cd frontend && npm run dev)
