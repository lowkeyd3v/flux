#!/usr/bin/env bash
# ==============================================================================
# Google Cloud Run Automated Deployment Script for FLUX
# ==============================================================================

set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"flux-production"}
REGION=${REGION:-"asia-south1"} # Mumbai region for low latency across India
IMAGE_NAME="gcr.io/${PROJECT_ID}/flux-backend:latest"

echo "=== [FLUX Cloud Run] Deploying to ${PROJECT_ID} (${REGION}) ==="

# 1. Build and push container to Google Container Registry / Artifact Registry
echo "--> Building production container..."
gcloud builds submit --tag "${IMAGE_NAME}" -f backend/Dockerfile .

# 2. Deploy Cloud Run Service
echo "--> Deploying service to Cloud Run..."
gcloud run deploy flux-backend \
  --image "${IMAGE_NAME}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --min-instances 1 \
  --max-instances 10 \
  --port 8000 \
  --set-env-vars APP_ENV=production,API_V1_PREFIX=/api,WEB_CONCURRENCY=4

echo "=== [FLUX Cloud Run] Deployment complete! ==="
