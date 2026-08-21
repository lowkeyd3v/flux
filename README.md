# FLUX

**Adaptive intelligence for everyday commerce.**

FLUX is an AI-powered business intelligence assistant for Indian street vendors and micro-entrepreneurs. It combines demand forecasting, weather/contextual awareness, explainable recommendations, and a government-scheme RAG assistant to help vendors make better daily business decisions.

Built for **OOSC 4.0 Hackathon — Problem Statement PS5: AI for Public Good**.

> **Status: Milestone 1 (Foundation) complete.** This README reflects only what is currently implemented. Sections describing future milestones (ML forecasting, recommendations, RAG, voice) are marked as planned and will be filled in as those features are built — see [Project Status](#project-status).

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Target Users](#target-users)
- [Project Status](#project-status)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [ML Methodology & Dataset](#ml-methodology--dataset)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Team](#team)
- [Future Scope](#future-scope)
- [Limitations](#limitations)

---

## Problem Statement

Street vendors and micro-entrepreneurs across India make daily business decisions — how much stock to prepare, what to price, when demand will spike or dip — largely by intuition. They often lack access to:

- Data-driven demand forecasting
- Localized, contextual information (e.g. weather impact on footfall/sales)
- Awareness of government schemes they may be eligible for, and how to access them

This creates avoidable financial risk (over-preparation → waste, under-preparation → lost sales) and leaves real economic support (schemes, subsidies, credit access) underutilized simply because it's hard to discover and understand.

## Solution

FLUX gives a vendor a simple, mobile-friendly dashboard where they can:

1. Create a business profile and log sales history
2. Get an ML-driven demand prediction for an upcoming day, adjusted for weather/context
3. Receive an explainable recommendation (how much to prepare, expected revenue, risk level)
4. Ask a FLUX assistant natural-language questions about government schemes, with answers grounded in real scheme documents via RAG — not invented by the model

## Target Users

Indian street vendors and micro-entrepreneurs (e.g. food carts, small retail stalls) who need lightweight, low-friction tools that work in simple language, and eventually in Hindi/Hinglish.

## Project Status

| Feature | Status |
|---|---|
| Project foundation (frontend, backend, DB, health check) | Done (Milestone 1) |
| Vendor profile + sales data | Done (Milestone 2) |
| Demand forecasting (ML) | Done (Milestone 3) |
| Recommendation engine + weather | Planned (Milestone 4) |
| Government scheme RAG | Planned (Milestone 5) |
| Dashboard integration | Planned (Milestone 6) |
| Hindi/Hinglish + voice | Planned (Milestone 7, if time permits) |
| Testing + deployment | Planned (Milestone 8) |

Nothing below this point describes a shipped feature unless explicitly stated. Service interfaces for the AI/ML components exist as clean, typed abstractions (see `backend/app/services/`) but currently raise `NotImplementedError` — this is intentional, so the codebase never pretends to have AI/ML functionality it doesn't yet have.

## Architecture

```
React Frontend
      |
      v
FastAPI Backend
      |
 -----------------------------------------
 |          |              |             |
 ML     Recommendation   RAG/AI       Weather
 Service   Service       Service      Service
 |          |              |             |
 -----------------------------------------
                |
           PostgreSQL
```

Each AI/ML/RAG/Weather component is defined as an independently replaceable service interface, so implementations can be swapped without touching API routes.

Currently implemented: Frontend to Backend to PostgreSQL, with a working `/api/health` endpoint that checks DB connectivity. Service interfaces exist as abstractions only.

## Tech Stack

**Frontend:** React, Vite, Tailwind CSS, React Router, Recharts, Axios
**Backend:** Python, FastAPI, Pydantic, SQLAlchemy, PostgreSQL
**ML (planned):** Pandas, NumPy, Scikit-learn, Joblib
**Generative AI (planned):** LLM API (provider-abstracted), FAISS/ChromaDB, Sentence Transformers
**Voice (planned, P2):** Whisper or equivalent
**Deployment:** Simple, single-service hosting (no Kubernetes/microservices)

## Repository Structure

```
flux/
├── frontend/            # React + Vite + Tailwind app
│   └── src/
│       ├── components/  # Reusable UI components
│       ├── pages/       # Route-level pages
│       ├── layouts/     # Page layout wrappers
│       ├── services/    # API client + service calls
│       ├── hooks/       # Custom React hooks
│       ├── utils/       # Helpers
│       └── assets/
│
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── main.py       # Thin entrypoint: settings + middleware + routers
│   │   ├── core/         # Config/settings
│   │   ├── api/          # API route handlers
│   │   ├── models/       # SQLAlchemy ORM models (Vendor, SalesRecord)
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Service interfaces (ML, RAG, AI, Weather, Voice, Recommendation)
│   │   ├── db/           # DB session/engine setup
│   │   └── utils/
│   ├── alembic/           # Database migrations
│   ├── tests/             # Pytest suite
│   ├── requirements.txt
│   └── .env.example
│
├── ml/                    # ML training/inference — synthetic data, preprocessing, training, inference (Milestone 3)
├── data/                  # Datasets (synthetic data will be clearly labeled)
├── docs/                  # Architecture diagrams, design notes
├── tests/                 # (reserved for cross-cutting/integration tests)
├── docker-compose.yml     # PostgreSQL for local development
├── .gitignore
├── LICENSE
└── README.md
```

## Local Setup

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker + Docker Compose (for PostgreSQL) — or a local PostgreSQL instance

### 1. Clone and enter the repo

```bash
git clone <repo-url>
cd flux
```

### 2. Start PostgreSQL

```bash
docker-compose up -d
```

This starts PostgreSQL on `localhost:5432` with database `flux_db`, user `flux_user`, password `flux_password` (see `docker-compose.yml`; change these for anything beyond local dev).

If Docker isn't available, install PostgreSQL locally and create a matching user/database, or point `DATABASE_URL` in `backend/.env` at your own instance.

### 3. Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # adjust values if needed
alembic upgrade head            # creates vendors and sales_records tables
uvicorn app.main:app --reload --port 8000
```

### 3b. Generate the demand forecasting model (one-time)

In a separate terminal, from the repo root, with the backend venv active:

```bash
source backend/venv/bin/activate    # Windows: backend\venv\Scripts\activate
python -m ml.data.generate_synthetic_data      # creates ml/data/synthetic_sales_data.csv
python -m ml.training.train_demand_model       # trains and saves ml/models/demand_model.joblib
```

This only needs to be run once (or whenever you want to regenerate the dataset/retrain). Without this step, the `/predict` endpoint returns a 503 error rather than a fake prediction.

Backend will be available at `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

### 4. Frontend setup

In a separate terminal:

```bash
cd frontend
npm install
cp .env.example .env            # adjust VITE_API_BASE_URL if needed
npm run dev
```

Frontend will be available at `http://localhost:5173`. It calls the backend's `/api/health` endpoint on load and displays connection status on the home page.

### 5. Verify

- Visit `http://localhost:5173` — you should see the FLUX home page with a "Connected" backend status badge.
- Visit `http://localhost:8000/api/health` directly — should return `{"status": "ok", "service": "flux-backend", "database": "ok"}`.
- Visit `http://localhost:5173/vendor` — create a vendor profile, select it, and log a sales record. Refresh to confirm the data persisted.
- On the same page, use the **Demand Prediction** card to get a forecast for a chosen date/weather — should return a real number, not a placeholder.
- Just below it, use the **Recommendation** card to get how much to prepare, expected revenue, and risk level. If you set `WEATHER_API_KEY` in `backend/.env`, leaving "Enter weather manually" unchecked will auto-fetch weather for the vendor's location; otherwise it falls back gracefully (`weather.source: "unavailable"`) rather than failing.

## Environment Variables

**Backend** (`backend/.env`, see `backend/.env.example`):

| Variable | Description | Default |
|---|---|---|
| `APP_ENV` | Environment name | `development` |
| `DATABASE_URL` | SQLAlchemy Postgres connection string | see `.env.example` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `LLM_API_KEY` | Reserved for AI assistant service (Milestone 5) | empty |
| `WEATHER_API_KEY` | [OpenWeatherMap](https://openweathermap.org/api) API key. Optional: if empty, `/recommend` still works but skips auto-fetched weather (falls back to the demand model's neutral defaults, or your own `temperature_celsius`/`weather_condition` values) | empty |

**Frontend** (`frontend/.env`, see `frontend/.env.example`):

| Variable | Description | Default |
|---|---|---|
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |

## ML Methodology & Dataset

**Dataset**: `ml/data/synthetic_sales_data.csv` — **SYNTHETIC / DEMO DATA, not real vendor sales.** No real street-vendor sales dataset was available at hackathon time, so `ml/data/generate_synthetic_data.py` generates ~2,800 rows of daily sales for 8 vendor archetypes (5 products × 4 North Indian cities) over roughly one year, with realistic weekly seasonality, holiday/event spikes, weather sensitivity, and random noise. The schema matches the `SalesRecord` model, so real vendor data can replace this file without changing the pipeline.

**Preprocessing** (`ml/preprocessing/features.py`): derives calendar features (day of week, month) from the date, one-hot encodes product/location/weather condition, and assembles a numeric feature matrix. The same function is used for both training and inference, so there's no train/serve skew.

**Train/validation split** (`ml/training/train_demand_model.py`): split **by date**, not randomly — the most recent 20% of the date range is held out for validation, and the model only ever trains on earlier dates. A random shuffle split would leak future information into training for time-series data, so this was deliberately avoided.

**Models compared**: a Linear Regression baseline and a Random Forest Regressor. The Random Forest was selected (lower validation MAE): **MAE ≈ 8.7 units, MAPE ≈ 10.7%, R² ≈ 0.84** on held-out validation data (exact numbers in `ml/models/demand_model_metadata.json`, regenerated each time the model is retrained).

**Serving**: the trained model is serialized with `joblib` to `ml/models/demand_model.joblib`. `ml/inference/predict.py` loads it once and exposes `predict_demand(...)`, which the backend's `MLDemandPredictionService` calls. The prediction's low/high range comes from the spread across the Random Forest's individual trees, giving an honest uncertainty band rather than a single falsely-precise number.

**Retraining**: to regenerate the dataset and retrain the model:

```bash
cd /path/to/flux   # repo root
source backend/venv/bin/activate
python -m ml.data.generate_synthetic_data
python -m ml.training.train_demand_model
```

## API Documentation

Currently implemented endpoints:

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Basic API liveness message |
| `GET` | `/api/health` | Health check; also verifies DB connectivity |
| `POST` | `/api/vendors` | Create a vendor business profile |
| `GET` | `/api/vendors` | List all vendor profiles |
| `GET` | `/api/vendors/{vendor_id}` | Get a single vendor profile |
| `PATCH` | `/api/vendors/{vendor_id}` | Partially update a vendor profile |
| `DELETE` | `/api/vendors/{vendor_id}` | Delete a vendor profile (cascades to its sales records) |
| `POST` | `/api/vendors/{vendor_id}/sales` | Log a single day's sales record |
| `POST` | `/api/vendors/{vendor_id}/sales/bulk` | Upload multiple historical sales records at once |
| `GET` | `/api/vendors/{vendor_id}/sales` | List a vendor's sales history |
| `DELETE` | `/api/vendors/{vendor_id}/sales/{record_id}` | Delete a single sales record |
| `POST` | `/api/vendors/{vendor_id}/predict` | Predict expected demand for a given date, with optional weather/holiday context |

Full interactive documentation (Swagger UI) is auto-generated by FastAPI at `/docs` once the backend is running. This table will grow as milestones add real endpoints (predictions, recommendations, scheme Q&A).

## Running Tests

```bash
cd backend
source venv/bin/activate
pytest
```

Current test coverage: 35 unit and integration tests covering health check, vendor profiles, sales records, ML demand forecasting, recommendation engine, and government scheme RAG (`backend/tests/`).

## Deployment

Not yet deployed. Deployment instructions and the live prototype link will be added in Milestone 8, per the project's simple-deployment principle (no Kubernetes or microservices).

## Team

- _Add team member names and roles here_

## Future Scope

See [Project Status](#project-status) for the milestone roadmap: dashboard integration, and — time permitting — Hindi/Hinglish voice support.

## Limitations

- This is a hackathon prototype, not a production system. Authentication, payments, and enterprise-grade infrastructure are intentionally out of scope.
- As of Milestone 3, vendor profiles, sales history, and demand predictions work end-to-end, but the recommendation engine, government scheme RAG, and voice features are not implemented yet — only their interfaces.
- The demand forecasting model is trained on **synthetic data**, not real vendor sales (see [ML Methodology & Dataset](#ml-methodology--dataset)). Predictions are directionally reasonable (respond correctly to weather, holidays, weekends) but should not be treated as real-world accurate until retrained on real data.
- There is no authentication, so any client can view or modify any vendor's data. Acceptable for a hackathon demo; would need to be addressed for a real deployment.
- Local development currently assumes PostgreSQL is reachable at the configured `DATABASE_URL`; no managed cloud DB is configured yet.

