# FLUX: Adaptive Intelligence for Everyday Commerce

<div align="center">

[![OOSC Hackathon](https://img.shields.io/badge/OOSC%204.0-Problem%20Statement%205%3A%20AI%20for%20Public%20Good-emerald?style=for-the-badge)](https://github.com/lowkeyd3v/flux)
[![CI Status](https://img.shields.io/badge/CI%20Build-Passing-brightgreen?style=for-the-badge&logo=githubactions)](https://github.com/lowkeyd3v/flux/actions)
[![Tests Passing](https://img.shields.io/badge/Pytest-48%2F48%20Passed-success?style=for-the-badge&logo=pytest)](https://github.com/lowkeyd3v/flux)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**An AI-powered business intelligence & welfare enablement assistant for India's 10+ million street vendors and micro-entrepreneurs.**

[⚡ Quickstart & Local Run](#-quickstart--local-run-instructions) • [🎥 Demo Video](#-demo-video) • [🏛️ System Architecture](#-system-architecture) • [📊 Core Capabilities](#-core-capabilities) • [📜 API Reference](#-api-documentation) • [🧪 Testing](#-running-automated-tests)

</div>

---

## 📌 Submission Overview

| Item | Details |
|---|---|
| **Hackathon** | **OOSC 4.0 Hackathon** |
| **Problem Statement** | **Problem Statement 5: AI for Public Good** |
| **Theme** | Inclusive AI, Social Impact and Empowerment of Underserved Communities |
| **Sub-Track** | *AI for Micro-Entrepreneurs and Street Vendors* & *AI for Accessible Public Services* |
| **Repository** | [github.com/lowkeyd3v/flux](https://github.com/lowkeyd3v/flux) |
| **Prototype Access** | **[One-Command Local Run (Docker Compose)](#-quickstart--local-run-instructions)** (`http://localhost`) |
| **Demo Video** | **[Watch 10-Minute Video Demo](#-demo-video)** *(Mandatory submission video)* |
| **Test Suite** | **48/48 Automated Tests Passing** (Pytest + React Build) |

---

## 🚀 How to Run the Prototype

Per hackathon submission guidelines, the prototype can be run locally with a single command using Docker Compose:

```bash
# 1. Clone the repository
git clone https://github.com/lowkeyd3v/flux.git
cd flux

# 2. Start the full application stack (PostgreSQL, Backend API, Web Frontend, Prometheus)
docker compose -f docker-compose.prod.yml up -d --build
```

- 🌐 **Web Dashboard:** `http://localhost`
- 📑 **Interactive OpenAPI (Swagger) Docs:** `http://localhost:8000/docs`
- 📊 **Prometheus Real-Time Metrics:** `http://localhost:8000/api/metrics`
- 🩺 **Health & Readiness Check:** `http://localhost:8000/api/health/ready`

*(For step-by-step developer setup without Docker, see [Local Developer Setup](#option-b-local-developer-setup))*

---

## 🎥 Demo Video

> 🔗 **Video Submission Link:** [Watch FLUX 10-Minute Demo Video](https://youtu.be/placeholder-demo-video) *(Update with your video link)*

### Video Walkthrough Highlights:
1. **Vendor Business Profile & Ledger:** Vendor registration and daily sales logging.
2. **ML Demand Forecasting with Uncertainty:** Real-time demand inference with confidence bounds.
3. **Smart Weather-Aware Recommendations:** Actionable stock preparation quantities adjusted for rain/heat and budget constraints.
4. **Grounded Government Scheme RAG:** Hallucination-free Q&A on PM SVANidhi, PM MUDRA, PM Vishwakarma, e-Shram, and PMSYM with citations and application steps.
5. **Personalized Scheme Matching:** Automated recommendations tailored to vendor trades and budgets.
6. **Voice & Trilingual Accessibility:** Hands-free speech recognition (STT) and voice narration (TTS) in English, Hindi (हिंदी), and Hinglish.
7. **Production Observability:** Live Prometheus metrics and structured distributed tracing.

---

## 🌟 Problem Statement & Social Impact

### The Reality of Indian Street Vendors
India is home to over **10 million street vendors and micro-entrepreneurs** who drive daily urban commerce—chaiwalas, fruit sellers, chaat carts, street tailors, and artisans. Despite their vital contribution, they operate with extreme vulnerability:

1. **Demand Uncertainty & Perishable Spoilage:** Vendors rely on guesswork to prep stock. Over-preparation leads to spoiled ingredients and direct financial loss; under-preparation leads to lost daily income.
2. **Weather Sensitivity:** Extreme summer heat (>40°C) or sudden monsoon rains decimate footfall, but vendors lack localized forecasting tools tailored to their specific products.
3. **Information Asymmetry in Government Welfare:** Schemes like **PM SVANidhi** (collateral-free credit + 7% interest subsidy), **PM MUDRA Yojana**, and **PM Vishwakarma** (₹15,000 toolkits + 5% loans) exist, but complex portals and bureaucratic jargon prevent informal workers from discovering eligibility and applying.
4. **Digital & Language Literacy Barriers:** Most vendors prefer speaking in **Hindi** or colloquial **Hinglish** over navigating dense English web portals.

---

## 💡 The FLUX Solution

FLUX is a lightweight, mobile-first, voice-enabled business intelligence copilot designed specifically for Indian micro-enterprises:

```
+---------------------------------------------------------------------------------------------------+
|                                       FLUX CORE CAPABILITIES                                      |
|                                                                                                   |
|  [📈 ML Demand Forecast]  --> Predicts unit demand with uncertainty bounds (Random Forest)        |
|  [🌤️ Stock Decision Engine] --> Computes prep quantities capped by budget & adjusted for weather |
|  [🏛️ Scheme RAG Advisor]    --> Answers scheme questions grounded in official government docs     |
|  [🎯 Personalized Matching] --> Matches vendor trades with optimal credit lines & toolkit grants  |
|  [🗣️ Trilingual Voice Assistant] --> Speech-to-Text & Text-to-Speech in English, Hindi & Hinglish|
|  [📊 Production Telemetry]  --> Prometheus metrics, structured JSON logs & distributed tracing    |
+---------------------------------------------------------------------------------------------------+
```

---

## 🏛️ System Architecture

```
                                  +---------------------------------------------+
                                  |              End User / Vendor              |
                                  |            (Mobile / Desktop PWA)           |
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

## 🚀 Core Capabilities

### 1. 📈 Machine Learning Demand Forecasting
- **Time-Series Random Forest Regressor** trained on weekly seasonality, holiday/festival calendar multipliers, price elasticity, and weather sensitivities.
- **Uncertainty Bounds:** Computes 10th percentile (`predicted_demand_low`), mean point estimate (`predicted_demand_point`), and 90th percentile (`predicted_demand_high`) across the decision tree ensemble.
- **Strict Chronological Validation:** Train/validation splits are strictly date-based (80/20 chronological) to prevent future data leakage (Validation MAE ≈ 8.7 units, R² ≈ 0.84).

### 2. 🌤️ Context-Aware Stock Recommendation Engine
- **Constraint-Aware Arithmetic:** Calculates exact units to prepare based on existing stock (`prep_units = forecast - inventory`), strictly capped by the vendor's daily working budget (`budget / selling_price`).
- **Live Weather Integration:** Connects with OpenWeatherMap API for live temperature and rain forecasts (with automatic fallback to neutral baselines when offline).
- **Explainable Decision Logic:** Generates plain-language reasoning and risk scores (`low`, `medium`, `high`) explaining forecast confidence and weather impacts.

### 3. 🏛️ Government Scheme RAG Assistant (Non-Hallucinating)
- **Comprehensive Knowledge Base:** Curated database of major Indian micro-enterprise schemes:
  - **PM SVANidhi:** Collateral-free working capital loan (₹10,000 → ₹20,000 → ₹50,000) with 7% interest subvention and digital cashback.
  - **PM MUDRA Yojana:** Non-farm micro-loans up to ₹10 Lakhs across *Shishu* (up to ₹50k), *Kishore* (₹50k–₹5L), and *Tarun* (₹5L–₹10L).
  - **PM Vishwakarma:** 18 traditional artisan trades with ₹15,000 toolkit grants and 5% concessional enterprise loans.
  - **e-Shram Portal:** Unorganized worker national database with ₹2 Lakh accidental insurance.
  - **PMSYM:** Old-age social security pension scheme providing ₹3,000/month after age 60.
- **Vector Retrieval with Lexical Boosting:** TF-IDF vector index combined with cosine similarity and domain intent keyword boosting (`eligible`, `documents`, `subsidy`, `apply`).
- **Dual-Engine Synthesis:** Deterministic, hallucination-free extractive synthesis engine that extracts exact criteria, documents, and portal links, plus optional LLM client integration.

### 4. 🎯 Automated Personalized Scheme Matcher
- Analyzes vendor business attributes (product type, daily budget, location) to automatically surface optimal government initiatives with match reasons and direct application steps.

### 5. 🗣️ Trilingual UI & Voice Interaction
- **Instant Trilingual Switching:** Seamless toggle between **English**, **हिंदी (Hindi)**, and **Hinglish** (conversational Romanized Hindi, e.g., *"Aaj kitna banana chahiye?"*).
- **Speech-to-Text (STT):** Browser-native Web Speech recognition (`webkitSpeechRecognition`) adapting dynamically between `hi-IN` and `en-IN` with zero server latency.
- **Text-to-Speech (TTS):** Integrated audio narration (`SpeakerButton`) reading recommendations and scheme details aloud in an Indian accent.
- **Voice Intent Parser:** Backend NLP endpoint mapping spoken phrases to actionable platform actions.

### 6. 📊 Production Observability & Telemetry
- **Prometheus Metrics (`/api/metrics`):** Exposes request counters, response latency summaries (p50/p90/p99), in-flight requests, database connectivity, and ML/RAG execution timings.
- **Distributed Tracing:** Generates and propagates `X-Request-ID` across every client request, server log, and database interaction.
- **Structured JSON Logging:** Emits machine-parsable access logs with request timestamps, client IPs, endpoints, status codes, and latencies.
- **Kubernetes Probes:** Standard `/api/health/live`, `/api/health/ready`, and `/api/health/detailed` health endpoints.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite, Tailwind CSS, Lucide Icons, React Router v7, Axios |
| **Backend** | Python 3.11/3.13, FastAPI, Gunicorn, Uvicorn, Pydantic v2, SQLAlchemy 2.0, Alembic |
| **Database** | PostgreSQL 16 (Relational DB with ACID transactions and Alembic migrations) |
| **Machine Learning** | Scikit-learn, Pandas, NumPy, Joblib (Random Forest Demand Regressor) |
| **RAG & GenAI** | TF-IDF Vector Retrieval, Cosine Similarity, Grounded Extractive Synthesizer, LLM API Client |
| **Observability** | Prometheus (`/api/metrics`), Grafana Dashboards, Structured JSON Logging, `X-Request-ID` Tracing |
| **Containerization & CI/CD** | Docker Multi-Stage, Docker Compose, Kubernetes (K8s), Google Cloud Run, Nginx Alpine, GitHub Actions |
| **External APIs** | OpenWeatherMap API (5-day forecasts & current weather) |
| **Testing** | Pytest, FastAPI TestClient, Starlette, AnyIO (48 automated tests) |

---

## 📁 Repository Structure

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

## ⚡ Quickstart / Local Run Instructions

### Prerequisites
- **Node.js:** v18.0 or higher
- **Python:** v3.11 or higher
- **Docker & Docker Compose** (for PostgreSQL database)

---

### Option A: One-Command Production Stack (Docker Compose)

```bash
# 1. Clone repository
git clone https://github.com/lowkeyd3v/flux.git
cd flux

# 2. Configure environment
cp deploy/docker.env.example .env

# 3. Start full production stack (PostgreSQL, Backend, Frontend, Prometheus, Grafana)
docker compose -f docker-compose.prod.yml up -d --build
```

- **Frontend Application:** `http://localhost`
- **Backend API:** `http://localhost/api` (or `http://localhost:8000`)
- **Prometheus Metrics:** `http://localhost:9090`
- **Grafana Dashboard:** `http://localhost:3000`

---

### Option B: Local Developer Setup

#### Step 1: Start PostgreSQL
```bash
docker compose up -d
```
*Starts PostgreSQL on `localhost:5432` with user `flux_user`, password `flux_password`, and db `flux_db`.*

#### Step 2: Set Up Backend Virtual Environment
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Install dependencies and apply migrations
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
```

#### Step 3: Train ML Demand Model (One-Time)
From the repository root (with virtual environment active):
```bash
python -m ml.data.generate_synthetic_data
python -m ml.training.train_demand_model
```

#### Step 4: Run Backend Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

#### Step 5: Run Frontend Application
In a separate terminal:
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
- Web Dashboard: `http://localhost:5173`

---

## 🧪 Running Automated Tests

The test suite covers database persistence, ML model inference, stock preparation logic, weather fallbacks, government scheme vector RAG retrieval, multilingual voice intent parsing, and production observability probes:

```bash
cd backend
# With virtual environment activated
pytest -v
```

**Test Suite Summary (48/48 Tests Passing):**
- `tests/test_health.py`: Health endpoint and PostgreSQL connectivity checks.
- `tests/test_monitoring.py`: Kubernetes liveness probe, readiness probe, system telemetry, Prometheus metrics, and distributed tracing (`X-Request-ID`).
- `tests/test_vendors.py`: Vendor CRUD operations and schema validation.
- `tests/test_sales_records.py`: Single and bulk sales logging with constraints.
- `tests/test_predictions.py`: ML prediction inference and uncertainty range bounds.
- `tests/test_recommendations.py`: Stock prep arithmetic, budget caps, risk scoring, and weather fallbacks.
- `tests/test_schemes.py`: Scheme listing, detail lookup, vector retrieval, vendor-context queries, and personalized matching.
- `tests/test_voice.py`: Multilingual intent parsing across English, Hindi, and Hinglish, and supported languages catalog.

---

## 📜 API Documentation

All REST endpoints are prefixed with `/api` (configurable via `API_V1_PREFIX`). Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

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

## 🌐 Production Deployment

Ready-to-deploy cloud configurations and manifests:

- 🐳 **Docker Compose Production:** [docker-compose.prod.yml](docker-compose.prod.yml)
- ☸️ **Kubernetes (EKS/GKE/AKS):** [deploy/k8s/](deploy/k8s/) (`backend.yaml`, `frontend.yaml`, `postgres.yaml`, `ingress.yaml`, `hpa.yaml`)
- ☁️ **Google Cloud Run:** [deploy/cloudrun/](deploy/cloudrun/) (`service.yaml`, `deploy.sh`)
- ⚡ **Render.com Blueprint:** [deploy/render.yaml](deploy/render.yaml)
- 📖 **Comprehensive Runbooks:**
  - [Production Deployment Guide](docs/PRODUCTION_DEPLOYMENT.md)
  - [CDN & Edge Optimization Guide](docs/CDN_AND_EDGE_GUIDE.md)
  - [Monitoring & Observability Guide](docs/MONITORING_AND_OBSERVABILITY.md)

---

## ⚖️ Evaluation Criteria Alignment

| Criteria | How FLUX Excels |
|---|---|
| **Innovation** | Integrates ML demand forecasting with live weather elasticity, constraint-based inventory arithmetic, trilingual voice assistants, and grounded government scheme RAG into a single unified copilot. |
| **Technical Implementation** | Production-ready stack: FastAPI backend, React 19 SPA, PostgreSQL with Alembic migrations, custom TF-IDF RAG engine with lexical boosting, Random Forest with tree variance uncertainty, and Prometheus telemetry. |
| **Feasibility & Social Good** | Designed for low digital literacy: trilingual support (Hindi/Hinglish/English), browser-native speech recognition and audio narration, and grounded welfare scheme eligibility for informal street vendors. |
| **Scalability & Architecture** | Multi-stage Docker containers, Nginx reverse proxy, Kubernetes Horizontal Pod Autoscalers (HPA), Prometheus metrics scraping, and edge CDN caching. |
| **Code Quality & Testing** | Modular architecture, strict separation of concerns, complete typing with Pydantic v2, and **48 automated unit and integration tests** running on GitHub Actions CI. |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
