#!/usr/bin/env bash
# deploy.sh — Deploy Track 1 Health Record Agent to Cloud Run
# Usage: GOOGLE_API_KEY=xxx bash deploy.sh
set -euo pipefail

PROJECT_ID="dee-md"
REGION="us-central1"
SERVICE_NAME="health-record-agent"

echo "==> Project: ${PROJECT_ID} | Service: ${SERVICE_NAME}"

gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com \
    --project="${PROJECT_ID}" --quiet

IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "==> Building container image with Cloud Build..."
gcloud builds submit --tag "${IMAGE}" --project="${PROJECT_ID}" .

echo "==> Deploying image to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE}" \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY}" \
    --project="${PROJECT_ID}"

echo ""
echo "==> Your Cloud Run URL (paste this into the submission form):"
gcloud run services describe "${SERVICE_NAME}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --format="value(status.url)"
