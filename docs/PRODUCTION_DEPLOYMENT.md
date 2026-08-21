# FLUX Production Deployment Guide

This guide contains complete instructions for deploying FLUX into production environments across Docker Compose, Kubernetes (EKS/GKE/AKS), Google Cloud Run, and managed PaaS platforms.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Prerequisites & System Sizing](#2-prerequisites--system-sizing)
3. [Deployment Option A: Docker Compose (Single VM / VPS)](#3-deployment-option-a-docker-compose-single-vm--vps)
4. [Deployment Option B: Kubernetes (Production Cluster)](#4-deployment-option-b-kubernetes-production-cluster)
5. [Deployment Option C: Google Cloud Run / Serverless](#5-deployment-option-c-google-cloud-run--serverless)
6. [Database Setup, Migrations & Backup Strategy](#6-database-setup-migrations--backup-strategy)
7. [SSL/TLS & Domain Configuration](#7-ssltls--domain-configuration)
8. [Zero-Downtime Updates & Rollbacks](#8-zero-downtime-updates--rollbacks)
9. [Security Hardening Checklist](#9-security-hardening-checklist)

---

## 1. Architecture Overview

```
                      +------------------------------------------+
                      |         CDN / Edge Proxy (Cloudflare)    |
                      |   - Edge Caching (Vite Chunks 1yr)       |
                      |   - DDoS & SSL/TLS Termination           |
                      +------------------------------------------+
                                     |            \
                          (Static /assets)     (/api/* Gateway)
                                     v              v
                      +-------------------+   +------------------+
                      | Nginx Web Server  |   | FastAPI Backend  |
                      | (Frontend Port 80)|-->| (Gunicorn/Uvicorn|
                      +-------------------+   +------------------+
                                                       |
                                      +----------------+----------------+
                                      |                                 |
                                      v                                 v
                             +------------------+             +-------------------+
                             |  PostgreSQL 16   |             |  Prometheus Scrape|
                             |  (Managed DB)    |             |  (/api/metrics)   |
                             +------------------+             +-------------------+
```

---

## 2. Prerequisites & System Sizing

### Minimum Recommended Production Specs:
- **CPU:** 2 vCPU cores
- **RAM:** 4 GB (2 GB for Backend + ML inference, 1 GB for PostgreSQL, 1 GB for OS & Nginx)
- **Disk:** 40 GB NVMe SSD
- **Operating System:** Ubuntu 22.04 LTS or Debian 12

---

## 3. Deployment Option A: Docker Compose (Single VM / VPS)

### Step 1: Clone Repository on the Server
```bash
git clone https://github.com/your-username/flux.git /opt/flux
cd /opt/flux
```

### Step 2: Configure Environment Variables
```bash
cp deploy/docker.env.example .env
# Edit credentials and domain names
nano .env
```

### Step 3: Launch Production Stack
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

### Step 4: Verify Deployment Health
```bash
# Check container status
docker compose -f docker-compose.prod.yml ps

# Check API health
curl -f http://localhost/api/health
curl -f http://localhost/api/health/ready
```

---

## 4. Deployment Option B: Kubernetes (Production Cluster)

### Step 1: Create Namespace and Secrets
```bash
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/configmap.yaml
kubectl apply -f deploy/k8s/secret.yaml
```

### Step 2: Deploy PostgreSQL StatefulSet (or use Managed RDS/Cloud SQL)
```bash
kubectl apply -f deploy/k8s/postgres.yaml
```

### Step 3: Deploy Backend & Frontend Workloads
```bash
kubectl apply -f deploy/k8s/backend.yaml
kubectl apply -f deploy/k8s/frontend.yaml
```

### Step 4: Apply Autoscaling & Ingress
```bash
kubectl apply -f deploy/k8s/hpa.yaml
kubectl apply -f deploy/k8s/ingress.yaml
```

### Step 5: Verify Rollout Status
```bash
kubectl -n flux rollout status deployment/flux-backend
kubectl -n flux rollout status deployment/flux-frontend
kubectl -n flux get pods -o wide
```

---

## 5. Deployment Option C: Google Cloud Run / Serverless

Execute the automated Cloud Run deployment script:
```bash
chmod +x deploy/cloudrun/deploy.sh
./deploy/cloudrun/deploy.sh
```

---

## 6. Database Setup, Migrations & Backup Strategy

### Automated Migrations on Startup
The container entrypoint (`backend/docker-entrypoint.sh`) executes `alembic upgrade head` before booting worker processes.

### Manual Migration Verification
```bash
docker compose -f docker-compose.prod.yml exec backend alembic current
```

### Daily Automated Backup Cron
Add the following cronjob to `/etc/cron.daily/flux-db-backup`:
```bash
#!/usr/bin/env bash
BACKUP_DIR="/var/backups/flux"
mkdir -p "$BACKUP_DIR"
DATE=$(date +\%Y\%m\%d_\%H\%M\%S)
docker exec flux_prod_postgres pg_dump -U flux_user -d flux_db | gzip > "$BACKUP_DIR/flux_db_$DATE.sql.gz"
# Retain backups for 30 days
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +30 -delete
```

---

## 7. SSL/TLS & Domain Configuration

When deploying behind Nginx or Cert-Manager:
- Use Let's Encrypt automated ACME certificates:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d flux.example.com
```

---

## 8. Zero-Downtime Updates & Rollbacks

### Rolling Update (Docker Compose)
```bash
# Pull new image and restart with zero drop in traffic
docker compose -f docker-compose.prod.yml pull backend frontend
docker compose -f docker-compose.prod.yml up -d --no-deps backend frontend
```

### Rolling Update (Kubernetes)
```bash
kubectl -n flux set image deployment/flux-backend backend=ghcr.io/your-username/flux-backend:v1.1.0
```

### Instant Rollback (Kubernetes)
```bash
kubectl -n flux rollout undo deployment/flux-backend
```

---

## 9. Security Hardening Checklist

- [x] Non-root user in Docker container (`fluxuser:fluxgroup`, UID 10001).
- [x] HTTP Security Headers configured (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`).
- [x] Strict CORS origin validation configured via `CORS_ORIGINS`.
- [x] Sensitive environment variables isolated in `.env` / Kubernetes Secrets.
- [x] Ephemeral secrets removed from container images via `.dockerignore`.
- [x] Prometheus metrics and health probes enabled for 24/7 uptime monitoring.
