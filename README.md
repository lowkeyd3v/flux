# FLUX

**Adaptive intelligence for everyday commerce.**

FLUX is an AI-powered business intelligence assistant for Indian street vendors and micro-entrepreneurs. It combines data-driven demand forecasting, real-time weather and contextual awareness, explainable stock preparation recommendations, and a grounded government-scheme RAG (Retrieval-Augmented Generation) assistant to help vendors make confident, profitable daily business decisions.

Built for **OOSC 4.0 Hackathon — Problem Statement PS5: AI for Public Good**.

> **Status: Milestones 1–8 (Foundation through Production Deployment) Complete.** All core features—vendor profile management, sales ledger, ML demand forecasting with uncertainty bounds, rule-based recommendation engine with OpenWeatherMap integration, grounded government scheme Q&A with personalized recommendations, trilingual UI (English, Hindi, Hinglish), browser-native Speech-to-Text / Text-to-Speech, voice intent parsing, multi-stage Docker containerization, Prometheus metrics & telemetry, and Kubernetes/Cloud deployment manifests—are fully implemented, integrated, and verified with 48 automated tests.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Target Users](#target-users)
- [Core Features](#core-features)
- [Project Status & Roadmap](#project-status--roadmap)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Local Setup](#local-setup)
- [Production Deployment](#production-deployment)
- [Environment Variables](#environment-variables)
- [ML Methodology & Dataset](#ml-methodology--dataset)
- [Government Scheme RAG System](#government-scheme-rag-system)
- [Multilingual & Voice Assistant System](#multilingual--voice-assistant-system)
- [Monitoring & Observability](#monitoring--observability)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Limitations](#limitations)
- [Future Scope](#future-scope)
- [License](#license)

---

## Problem Statement

Over 10 million street vendors and micro-entrepreneurs across India make daily business decisions—how much stock to prepare, what to price, when demand will spike or dip—largely by intuition. They face systemic hurdles:

- **Demand Uncertainty & Perishability:** Over-preparation leads to wasted raw materials and inventory spoilage; under-preparation leads to lost revenue and dissatisfied customers.
- **Weather & Local Context Vulnerability:** Extreme heat, sudden rains, and festivals significantly alter daily footfall and purchasing patterns, but vendors lack localized forecasting tools.
- **Information Asymmetry in Government Support:** Valuable welfare and financial schemes (such as PM SVANidhi, PM MUDRA Yojana, and PM Vishwakarma) offer low-cost working capital, toolkits, and interest subsidies, yet vendors struggle to discover eligibility rules, required documentation, and application procedures due to complex bureaucratic portals.
- **Language & Literacy Barriers:** Many vendors are non-native English speakers who operate in Hindi, regional dialects, or colloquial Hinglish, requiring voice-driven interaction rather than dense text interfaces.

---

## Solution

FLUX provides a lightweight, mobile-friendly dashboard tailored to the operational realities of street vendors:

1. **Vendor Business Profile & Sales Ledger:** Create store profiles (product type, location, unit price, current inventory, daily working budget) and log daily sales history.
2. **ML-Driven Demand Forecasting:** Predict unit demand for upcoming days using a Random Forest model trained on seasonal patterns, calendar events, and weather conditions, complete with confidence intervals.
3. **Smart Recommendations with Weather Context:** Receive plain-language, actionable stock preparation quantities and expected revenue adjusted for live weather forecasts, current inventory, and budget constraints.
4. **Government Scheme RAG Assistant:** Ask natural-language questions regarding government welfare, loans, and subsidies, receiving hallucination-free answers grounded in official scheme documents with source citations and direct application links.
5. **Personalized Scheme Matching:** Automatically matches vendors to relevant government initiatives based on their business product, budget size, and geographic location.
6. **Voice & Multilingual Accessibility:** Switch seamlessly between **English**, **हिंदी (Hindi)**, and **Hinglish**, with browser-native speech recognition (STT) for questions and audio narration (TTS) for recommendations.
7. **Production Containerization & Observability:** Production-ready multi-stage Docker containers, Nginx reverse proxy, Prometheus metrics (`/api/metrics`), and Kubernetes/Cloud Run manifests.

---

## Target Users

Indian street vendors, roadside food stalls, artisans, and micro-retailers (e.g., chaat carts, tea stalls, fruit vendors, handicraft makers) needing accessible, low-friction, high-utility business tools in their own language.

---

## Core Features

### 1. Vendor Profile & Sales Management (Milestone 2)
- Fast vendor profile creation with business attributes: product category, city/location, default selling price, current inventory, and daily budget.
- Interactive sales ledger supporting single-day logging and bulk historical data entry.
- PostgreSQL database backed by SQLAlchemy ORM and Alembic migrations.

### 2. Machine Learning Demand Forecasting (Milestone 3)
- Point forecast of expected units sold for any selected future date.
- Prediction uncertainty bounds (`predicted_demand_low`, `predicted_demand_high`) generated from ensemble tree variance.
- Incorporates calendar features (day of week, seasonality), holiday/event flags, and weather conditions.

### 3. Recommendation Engine & Weather Intelligence (Milestone 4)
- **Constraint-Aware Arithmetic:** Calculates exact preparation units needed beyond existing stock, capped by the vendor's actual available budget.
- **Weather Integration:** Connects with OpenWeatherMap API for live temperature and rain forecasts (with automatic fallback to manual entry or neutral historical baselines when offline/unconfigured).
- **Risk Assessment & Explainability:** Evaluates forecast confidence and low/high spread to assign a risk rating (`low`, `medium`, `high`) accompanied by clear, non-technical reasoning.

### 4. Government Scheme RAG & Personalized Advisor (Milestone 5)
- **Comprehensive Knowledge Base:** Curated database of major Indian micro-enterprise schemes including **PM SVANidhi**, **PM MUDRA Yojana (Shishu, Kishore, Tarun)**, **PM Vishwakarma**, **e-Shram Portal**, and **PMSYM**.
- **Source-Grounded Retrieval:** Vector TF-IDF indexing and cosine similarity retrieval with intent and domain-specific lexical boosting.
- **Dual-Engine Synthesis:** Deterministic, hallucination-free extractive synthesis engine with seamless LLM API integration for enriched responses.
- **Interactive Assistant UI:** Question suggestions, source chunk transparency drawers, step-by-step application modals, and recommended follow-up questions.
- **Personalized Recommendations:** Automated matching engine analyzing vendor constraints to suggest optimal credit lines and grants.

### 5. Unified Dashboard (Milestone 6)
- Cohesive React interface linking vendor profile state directly to predictions, recommendations, sales history, and personalized schemes.

### 6. Hindi/Hinglish Localization & Voice Assistant (Milestone 7)
- **Trilingual Localization:** Instant language switching across **English**, **हिंदी (Hindi)**, and **Hinglish (Colloquial Hindi)**.
- **Voice Speech-to-Text (STT):** Integrated Web Speech recognition button on Scheme Assistant for speaking questions in Hindi/Hinglish.
- **Voice Text-to-Speech (TTS):** Audio narration button (`SpeakerButton`) on recommendations and scheme answers for hands-free audio playback.
- **Voice Intent Processing:** Backend endpoint recognizing spoken user commands (scheme searches, demand predictions, preparation advice, sales logging).

### 7. Production Deployment & Monitoring (Milestone 8)
- **Multi-Stage Containerization:** Production Dockerfiles for FastAPI + Gunicorn ASGI workers and Vite + Nginx edge server.
- **Full-Stack Orchestration:** Production `docker-compose.prod.yml` with PostgreSQL 16, backend, frontend, Prometheus, and Grafana.
- **Prometheus Metrics & Health Probes:** Real-time metrics on `/api/metrics`, plus `/api/health/live`, `/api/health/ready`, and `/api/health/detailed`.
- **Structured Observability:** JSON access logging and `X-Request-ID` distributed tracing middleware.
- **Cloud & CDN Manifests:** Ready-to-deploy Kubernetes (`deploy/k8s/`), Google Cloud Run (`deploy/cloudrun/`), and Render blueprints (`deploy/render.yaml`).

---

## Project Status & Roadmap

| Feature / Milestone | Status | Description |
|---|---|---|
| **Milestone 1: Project Foundation** | **Complete** | React + Vite + Tailwind frontend, FastAPI backend, Docker PostgreSQL, DB migrations, health checks. |
| **Milestone 2: Vendor Profiles & Sales** | **Complete** | Full CRUD for vendor profiles and sales records, validation schemas, database models. |
| **Milestone 3: Demand Forecasting (ML)** | **Complete** | Time-series split, Random Forest model, feature engineering, uncertainty intervals, inference API. |
| **Milestone 4: Recommendation Engine** | **Complete** | Rule-based preparation logic, OpenWeatherMap integration, risk scoring, explainable text. |
| **Milestone 5: Scheme RAG Assistant** | **Complete** | Vector search over scheme documents, grounded synthesis, personalized vendor scheme matching. |
| **Milestone 6: Dashboard Integration** | **Complete** | End-to-end frontend integration connecting vendor selection with all AI/ML & RAG services. |
| **Milestone 7: Hindi/Hinglish & Voice** | **Complete** | Trilingual UI (English, Hindi, Hinglish), browser-native Speech-to-Text & Text-to-Speech, voice intent API. |
| **Milestone 8: Production Deployment** | **Complete** | Multi-stage Docker containerization, Docker Compose prod stack, Kubernetes & Cloud Run manifests, Prometheus metrics, structured logging, CDN edge optimization. |

---

## System Architecture

```
                                  +---------------------------------------------+
                                  |              End User / Vendor              |
                                  +---------------------------------------------+
                                                         |
                                                         v
                                  +---------------------------------------------+
                                  |     Cloudflare / CloudFront CDN & SSL       |
                                  |      - Hashed Static Chunks Cached 1yr      |
                                  |      - Dynamic API Requests Pass-Through    |
                                  +---------------------------------------------+
                                          /                             \
                       (Static Assets / Web)                    (API Gateway / Reverse Proxy)
                                        /                                 \
                                       v                                   v
+---------------------------------------------+   +-----------------------------------------------------------------+
|          Nginx Alpine Container             |   |                  FastAPI Production Container                   |
|  - SPA Client-Side Fallback Routing         |   |                (Gunicorn + Uvicorn ASGI Workers)                |
|  - Immutable Vite Asset Headers             |   |                                                                 |
|  - Security Headers & Compression           |   |  +-------------------+  +------------------+  +--------------+  |
+---------------------------------------------+   |  | Vendors & Sales   |  | Demand Forecast  |  | Stock Recs   |  |
                                                  |  +-------------------+  +------------------+  +--------------+  |
                                                  |  | Schemes RAG Engine|  | Voice Intent API |  | Health Probes|  |
                                                  |  +-------------------+  +------------------+  +--------------+  |
                                                  |                                 |                               |
                                                  |  [ X-Request-ID Tracing ] [ JSON Structured Logs ] [ Prometheus ]|
                                                  +-----------------------------------------------------------------+
                                                              /                      |                      \
                                                             /                       |                       \
                                                            v                        v                        v
                                            +---------------------+  +----------------------+  +---------------------+
                                            | PostgreSQL Database |  |  External Providers  |  |  Prometheus Scraper |
                                            | (Persistent Volume) |  |  (OpenWeather, LLM)  |  |  & Grafana Dashboard|
                                            +---------------------+  +----------------------+  +---------------------+
```

---

## Tech Stack

- **Frontend:** React 19, Vite, Tailwind CSS, Lucide Icons, React Router v7, Axios
- **Backend:** Python 3.11/3.13, FastAPI, Gunicorn, Uvicorn, Pydantic v2, SQLAlchemy 2.0, Alembic
- **Database:** PostgreSQL 16 (Local & Production Containerized)
- **Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib (Random Forest Regressor)
- **Generative AI & RAG:** Custom TF-IDF vector retrieval engine with lexical/intent boosting, Grounded Extractive Synthesizer, LLM chat client
- **Observability & Metrics:** Prometheus exposition (`/api/metrics`), Grafana dashboards, structured JSON logging, distributed tracing (`X-Request-ID`)
- **Containerization & Cloud:** Docker Multi-Stage, Docker Compose, Kubernetes (K8s), Google Cloud Run, Nginx Alpine, GitHub Actions CI/CD
- **External Services:** OpenWeatherMap API (5-day forecasts & current weather)
- **Testing:** Pytest, FastAPI TestClient, Starlette, AnyIO (48 automated tests)

---

## Repository Structure

```
flux/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Automated tests, linting & Docker builds
│       └── deploy.yml                # Automated release & container publishing (GHCR)
│
├── frontend/                         # React Single-Page Application
│   ├── src/
│   │   ├── components/               # UI Components & ErrorBoundary
│   │   ├── pages/                    # Route pages (HomePage, VendorPage)
│   │   ├── services/                 # Axios client with tracing & latency tracking
│   │   ├── utils/performance.js      # Web Vitals & performance telemetry
│   │   ├── translations/             # English, Hindi, Hinglish dictionaries
│   │   └── hooks/                    # Custom React state hooks
│   ├── public/
│   │   ├── _headers                  # Cloudflare Pages / CDN cache headers
│   │   ├── robots.txt                # Search engine crawler configuration
│   │   └── sitemap.xml               # Site URL manifest
│   ├── Dockerfile                    # Multi-stage production container
│   ├── nginx.conf                    # Nginx reverse proxy & cache configuration
│   └── package.json
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py                   # App factory with tracing & metrics middlewares
│   │   ├── core/
│   │   │   ├── config.py             # Pydantic Settings & environment config
│   │   │   ├── metrics.py            # Prometheus metrics collector & registry
│   │   │   └── middleware.py         # Request ID tracing & structured JSON logging
│   │   ├── api/                      # REST route controllers
│   │   │   ├── health.py             # Liveness, readiness, detailed & Prometheus endpoints
│   │   │   ├── vendors.py            # Vendor profile CRUD
│   │   │   ├── sales_records.py      # Sales history logging & bulk upload
│   │   │   ├── predictions.py        # Demand forecasting endpoint
│   │   │   ├── recommendations.py    # Stock prep & weather recommendation
│   │   │   ├── schemes.py            # Government scheme RAG & recommendations
│   │   │   └── voice.py              # Voice intent parsing & language catalog
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── services/                 # Core business & AI logic
│   │   └── data/schemes_data.json    # Curated scheme knowledge base
│   ├── alembic/                      # Database migration versions
│   ├── tests/                        # 48 Pytest unit, integration & monitoring tests
│   ├── Dockerfile                    # Multi-stage production container
│   ├── docker-entrypoint.sh          # DB migration runner & server starter
│   ├── gunicorn_conf.py              # Production Gunicorn ASGI worker config
│   └── requirements.txt
│
├── deploy/                           # Cloud & Production Deployment Manifests
│   ├── k8s/                          # Kubernetes Manifests (Deployments, Services, HPA, Ingress)
│   ├── cloudrun/                     # Google Cloud Run service definition & deploy script
│   ├── monitoring/                   # Prometheus scrape config & Grafana dashboard JSON
│   ├── render.yaml                   # Render.com infrastructure blueprint
│   └── docker.env.example            # Docker Compose production environment template
│
├── docs/                             # Comprehensive System Documentation
│   ├── PRODUCTION_DEPLOYMENT.md      # Step-by-step production deployment & runbooks
│   ├── CDN_AND_EDGE_GUIDE.md         # CDN edge caching, SSL & performance guide
│   └── MONITORING_AND_OBSERVABILITY.md# Metrics, structured logs, and alert rules
│
├── ml/                               # Machine Learning Pipeline
│   ├── data/                         # Synthetic data generation
│   ├── preprocessing/                # Feature engineering
│   ├── training/                     # Training & evaluation
│   ├── inference/predict.py          # Model loading & inference wrapper
│   └── models/demand_model.joblib    # Serialized Random Forest model
│
├── docker-compose.yml                # Local development database
├── docker-compose.prod.yml           # Full production compose stack
├── LICENSE                           # MIT License
└── README.md
```

---

## Local Setup

### Prerequisites

- **Node.js:** v18.0 or higher
- **Python:** v3.11 or higher
- **Docker & Docker Compose** (or a local PostgreSQL instance)

---

### Step 1: Clone and Enter the Repository

```bash
git clone https://github.com/your-username/flux.git
cd flux
```

---

### Step 2: Start PostgreSQL with Docker

```bash
docker-compose up -d
```

*Starts PostgreSQL on `localhost:5432` with database `flux_db`, user `flux_user`, and password `flux_password`.*

---

### Step 3: Backend Setup & Database Migrations

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Windows (CMD):
.\venv\Scripts\activate.bat

pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
```

---

### Step 4: Generate Synthetic Data & Train ML Model (One-Time)

From the repo root (with backend virtual environment activated):

```bash
# Generate the synthetic sales dataset (~2,800 records)
python -m ml.data.generate_synthetic_data

# Train and serialize the Random Forest demand forecasting model
python -m ml.training.train_demand_model
```

---

### Step 5: Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

- Backend API: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

---

### Step 6: Frontend Setup & Run

In a separate terminal window:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend application will be accessible at `http://localhost:5173`.

---

## Environment Variables

### Backend Configuration (`backend/.env`)

| Variable | Description | Default / Example |
|---|---|---|
| `APP_ENV` | Application environment mode | `development` |
| `DATABASE_URL` | SQLAlchemy PostgreSQL connection string | `postgresql://flux_user:flux_password@localhost:5432/flux_db` |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `WEATHER_API_KEY` | *(Optional)* [OpenWeatherMap](https://openweathermap.org/api) API key for automated live weather in recommendations. If empty, manual weather entry is used with graceful neutral fallback. | `""` |
| `LLM_API_KEY` | *(Optional)* OpenAI / LLM API key for generative chat answers. If empty, the system uses the deterministic Grounded Extractive engine. | `""` |
| `API_V1_PREFIX` | Base prefix for all API routes | `/api` |

### Frontend Configuration (`frontend/.env`)

| Variable | Description | Default |
|---|---|---|
| `VITE_API_BASE_URL` | Backend URL endpoint consumed by Axios | `http://localhost:8000` |

---

## ML Methodology & Dataset

### 1. Synthetic Dataset
Because real street-vendor point-of-sale datasets are scarce and proprietary, `ml/data/generate_synthetic_data.py` generates ~2,800 rows of daily sales records across 8 vendor archetypes (covering 5 product categories across 4 North Indian cities) spanning a full year. The generator incorporates:
- **Weekly Seasonality:** Weekend demand surges (e.g. chaat/tea on Saturday/Sunday).
- **Festival & Holiday Spikes:** Explicit multipliers for Diwali, Holi, Eid, and local fairs.
- **Weather Sensitivity:** Negative elasticity for heavy rain and extreme heat (>40°C).
- **Realistic Noise:** Gaussian variance mimicking real retail fluctuation.

### 2. Feature Engineering & Preprocessing
`ml/preprocessing/features.py` derives:
- Calendar features: `day_of_week`, `is_weekend`, `month`.
- Binary indicators: `is_holiday_or_event`.
- Contextual features: `temperature_celsius`, `weather_condition` (one-hot encoded: `clear`, `cloudy`, `rain`, `extreme_heat`).
- Vendor attributes: `product`, `location`, `price`.

The exact same transformation pipeline is executed during both training and real-time inference to prevent train/serve skew.

### 3. Date-Based Train/Validation Split
To prevent temporal data leakage (where future sales leak into past predictions), the dataset is split strictly **chronologically**:
- **Training Set:** First 80% of historical dates.
- **Validation Set:** Most recent 20% held-out date range.

### 4. Model Selection & Metrics
A baseline Linear Regression model was evaluated against a **Random Forest Regressor** (100 estimators):
- **Validation MAE:** ≈ 8.7 units
- **Validation MAPE:** ≈ 10.7%
- **Validation R² Score:** ≈ 0.84

*Detailed metrics and hyperparameters are serialized in `ml/models/demand_model_metadata.json`.*

### 5. Prediction Uncertainty Intervals
Rather than outputting an artificially exact point estimate, the inference service computes the spread across the individual decision trees in the Random Forest ensemble:
- `predicted_demand_low`: 10th percentile of tree predictions.
- `predicted_demand_point`: Mean ensemble prediction.
- `predicted_demand_high`: 90th percentile of tree predictions.

---

## Government Scheme RAG System

The FLUX Scheme Assistant delivers accurate, actionable, and non-hallucinated guidance on Indian government initiatives for micro-enterprises.

```
                      +------------------------------------------+
                      |         Vendor Query + Profile           |
                      +------------------------------------------+
                                           |
                                           v
                      +------------------------------------------+
                      |  TF-IDF Vector Index & Lexical Boosting  |
                      +------------------------------------------+
                                           |
                    +----------------------+---------------------+
                    | Top-K Relevant Scheme Document Chunks      |
                    +--------------------------------------------+
                                           |
                                           v
                      +------------------------------------------+
                      |    Dual-Engine Synthesis Architecture    |
                      |  - Grounded Extractive Synthesizer       |
                      |  - External LLM Client (OpenAI/Gemini)   |
                      +------------------------------------------+
                                           |
                                           v
                      +------------------------------------------+
                      | Grounded Answer with Citations & Portals |
                      | Suggested Follow-Ups & Match Reasons     |
                      +------------------------------------------+
```

### Knowledge Base Content
Structured in `backend/app/data/schemes_data.json`, containing curated documents for:
- **PM SVANidhi:** Collateral-free working capital micro-credit (₹10k → ₹20k → ₹50k tranches) with 7% interest subvention and digital transaction cashback.
- **PM MUDRA Yojana:** Non-farm enterprise loans up to ₹10 Lakhs categorized into *Shishu* (up to ₹50k), *Kishore* (₹50k to ₹5 Lakhs), and *Tarun* (₹5 to ₹10 Lakhs).
- **PM Vishwakarma:** 18 traditional artisan trades with ₹15,000 toolkits, skill training stipends, and 5% concessional enterprise loans.
- **e-Shram Portal:** Unorganized worker national database providing 12-digit UAN and ₹2 Lakh accidental insurance coverage.
- **PMSYM (Pradhan Mantri Shram Yogi Maan-dhan):** Old-age social security pension scheme providing ₹3,000/month after age 60.

### Document Chunking & Retrieval
- Documents are segmented into targeted chunks: *Overview & Target Group*, *Eligibility Criteria*, *Financial Assistance & Subsidies*, *Required Documents*, and *Application Process*.
- Retrieval uses TF-IDF vectorization with cosine similarity, boosted by exact domain keyword matches and intent keywords (`eligible`, `documents`, `subsidy`, `apply`).

### Grounded Answer Synthesis
- **Deterministic Extractive Engine:** Operates entirely locally without external API dependencies or API keys. Extracts exact criteria, required documents, and application steps directly from retrieved context chunks.
- **LLM Synthesis:** When `LLM_API_KEY` is provided, queries are synthesized into fluid conversational answers while strictly bounded by the retrieved official context.

---

## Multilingual & Voice Assistant System

FLUX is built specifically for Indian street vendors who speak diverse languages and have varying levels of literacy:

- **Trilingual Localization (`en`, `hi`, `hinglish`):** Switch effortlessly between English, Hindi (हिंदी in Devanagari), and conversational Hinglish (Roman script, e.g. *"Aaj kitna banana chahiye?"*).
- **Speech-to-Text (STT):** Powered by browser-native Web Speech Recognition (`webkitSpeechRecognition`) with zero server latency and automatic language adaptation (`hi-IN` / `en-IN`).
- **Text-to-Speech (TTS):** Integrated audio narration using `speechSynthesis` with Indian accent voice matching to read aloud recommendations and scheme guidance.
- **Voice Intent Processor:** Backend REST endpoint mapping spoken phrases to actionable platform intents (scheme inquiries, demand forecasts, stock prep calculations, and sales logging).

---

## API Documentation

All endpoints are prefixed with `/api` (configurable via `API_V1_PREFIX`). Interactive Swagger documentation is available at `http://localhost:8000/docs`.

### Health & Observability Probes
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health and PostgreSQL database connectivity check |
| `GET` | `/api/health/live` | Kubernetes liveness probe (checks process responsiveness) |
| `GET` | `/api/health/ready` | Kubernetes readiness probe (verifies DB, ML model, and RAG data) |
| `GET` | `/api/health/detailed` | Comprehensive system telemetry, memory stats, CPU, and components |
| `GET` | `/api/metrics` | Prometheus metrics exposition format (version 0.0.4) |

### Vendor Profile Management
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/vendors` | Create a new vendor profile |
| `GET` | `/api/vendors` | List all registered vendor profiles |
| `GET` | `/api/vendors/{vendor_id}` | Retrieve specific vendor profile by UUID |
| `PATCH` | `/api/vendors/{vendor_id}` | Partially update vendor attributes (budget, inventory, price) |
| `DELETE` | `/api/vendors/{vendor_id}` | Delete vendor profile (cascades to associated sales records) |

### Sales History Ledger
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/vendors/{vendor_id}/sales` | Log a daily sales record |
| `POST` | `/api/vendors/{vendor_id}/sales/bulk` | Batch upload historical sales records |
| `GET` | `/api/vendors/{vendor_id}/sales` | Retrieve historical sales logs for a vendor |
| `DELETE` | `/api/vendors/{vendor_id}/sales/{record_id}` | Delete a specific sales record |

### Demand Forecasting & Smart Recommendations
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/vendors/{vendor_id}/predict` | ML demand forecast for a target date with weather context |
| `POST` | `/api/vendors/{vendor_id}/recommend` | Preparation quantity, revenue forecast, risk score & weather summary |

### Government Schemes & RAG Assistant
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/schemes` | List all government schemes (with optional `?category=` filter) |
| `GET` | `/api/schemes/{scheme_id}` | Get full scheme details, eligibility, required docs, and steps |
| `POST` | `/api/schemes/query` | Natural-language RAG query with source-attributed answers |
| `GET` | `/api/vendors/{vendor_id}/schemes/recommended` | Personalized scheme recommendations matching vendor profile |

### Voice & Multilingual Assistant
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/voice/parse-intent` | Parse spoken vendor query into structured action (schemes, predictions, sales) |
| `GET` | `/api/voice/supported-languages` | List supported languages (`en`, `hi`, `hinglish`) and speech synthesizer models |

---

## Running Tests

The test suite covers database persistence, ML model inference, rule-based recommendation logic, weather fallback mechanisms, RAG retrieval/synthesis, multilingual voice intent parsing, and production observability:

```bash
cd backend
# With virtual environment activated
pytest -v
```

**Test Coverage Summary (48 Tests):**
- `tests/test_health.py`: Health endpoint and DB connectivity checks.
- `tests/test_monitoring.py`: Liveness probe, readiness probe, system telemetry, Prometheus metrics, and distributed tracing (`X-Request-ID`).
- `tests/test_vendors.py`: Vendor CRUD and validation.
- `tests/test_sales_records.py`: Single and bulk sales logging with constraints.
- `tests/test_predictions.py`: ML prediction inference and range bounds.
- `tests/test_recommendations.py`: Stock prep constraints, budget limits, risk assessment, and weather fallbacks.
- `tests/test_schemes.py`: Scheme listing, detail lookup, vector retrieval, vendor-context queries, and personalized matching.
- `tests/test_voice.py`: Multilingual intent parsing across English, Hindi, and Hinglish, and supported languages catalog.

---

## Production Deployment

FLUX provides production configurations and manifests across multiple cloud providers:

### Option 1: Full-Stack Docker Compose (Single Host / VPS)
```bash
# 1. Configure production environment
cp deploy/docker.env.example .env

# 2. Launch production stack with PostgreSQL, Backend, Frontend, Prometheus & Grafana
docker compose -f docker-compose.prod.yml up -d --build
```

### Option 2: Kubernetes Cluster (EKS / GKE / AKS)
```bash
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/configmap.yaml
kubectl apply -f deploy/k8s/secret.yaml
kubectl apply -f deploy/k8s/postgres.yaml
kubectl apply -f deploy/k8s/backend.yaml
kubectl apply -f deploy/k8s/frontend.yaml
kubectl apply -f deploy/k8s/ingress.yaml
kubectl apply -f deploy/k8s/hpa.yaml
```

### Option 3: Google Cloud Run (Serverless)
```bash
chmod +x deploy/cloudrun/deploy.sh
./deploy/cloudrun/deploy.sh
```

### Option 4: Render / PaaS 1-Click Deployment
Use `deploy/render.yaml` to deploy the unified backend, frontend, and PostgreSQL services directly via Render Blueprints.

*For detailed production runbooks, SSL configuration, database backup scripts, and rollback strategies, see [docs/PRODUCTION_DEPLOYMENT.md](docs/PRODUCTION_DEPLOYMENT.md), [docs/CDN_AND_EDGE_GUIDE.md](docs/CDN_AND_EDGE_GUIDE.md), and [docs/MONITORING_AND_OBSERVABILITY.md](docs/MONITORING_AND_OBSERVABILITY.md).*

---

## Limitations

- **Synthetic Sales Data:** The current ML demand forecasting model is trained on synthetic data representing typical North Indian street food and retail dynamics. Retraining on actual vendor point-of-sale logs is recommended for production accuracy.
- **Simplified Authentication:** In this hackathon build, vendor profiles are accessible without individual authentication tokens. Multi-tenant authentication (e.g. phone OTP / JWT) will be integrated in subsequent milestones.
- **Weather Forecast Horizon:** Free-tier OpenWeatherMap forecasts are limited to a 5-day horizon; queries beyond 5 days rely on vendor manual input or historical weather averages.

---

## Future Scope

- **Supplier & Raw Material Price Tracking:** Integrating local mandi (wholesale market) commodity pricing to advise vendors on optimal raw ingredient purchasing times.
- **Peer Benchmark Insights:** Anonymized neighborhood demand trends comparing vendor sales against local averages.
- **Federated On-Device Training:** Fine-tuning demand forecasting models directly on vendor mobile devices while preserving privacy.

---

## License

This project is licensed under the [MIT License](LICENSE).

