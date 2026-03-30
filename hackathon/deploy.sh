#!/usr/bin/env bash
# deploy.sh — Deploy Hackathon Multi-Agent to Cloud Run
# Usage: GOOGLE_API_KEY=xxx bash deploy.sh
set -euo pipefail

PROJECT_ID="dee-md"
REGION="us-central1"
SERVICE_NAME="health-productivity-assistant"

echo "==> Project: ${PROJECT_ID} | Service: ${SERVICE_NAME}"

gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
    --project="${PROJECT_ID}" --quiet

gcloud run deploy "${SERVICE_NAME}" \
    --source . \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY}" \
    --project="${PROJECT_ID}"

echo ""
echo "==> Cloud Run URL:"
gcloud run services describe "${SERVICE_NAME}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --format="value(status.url)"
