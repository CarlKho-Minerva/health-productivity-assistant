#!/usr/bin/env bash
# deploy.sh — Deploy Track 1 Health Record Agent to Cloud Run
# Usage: bash deploy.sh
#   GOOGLE_API_KEY is auto-fetched from the live service if not set in env.
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
# Auto-fetch GOOGLE_API_KEY from live service if not set in shell
if [ -z "${GOOGLE_API_KEY:-}" ]; then
  echo "==> GOOGLE_API_KEY not in env — fetching from live Cloud Run service..."
  GOOGLE_API_KEY=$(gcloud run services describe "${SERVICE_NAME}" \
    --region="${REGION}" --project="${PROJECT_ID}" --format=json 2>/dev/null \
    | python3 -c "
import sys, json
s = json.load(sys.stdin)
envs = s.get('spec',{}).get('template',{}).get('spec',{}).get('containers',[{}])[0].get('env',[])
v = [e.get('value','') for e in envs if e.get('name') == 'GOOGLE_API_KEY']
print(v[0] if v else '')
" 2>/dev/null || true)
fi
if [ -z "${GOOGLE_API_KEY:-}" ]; then
  echo "ERROR: GOOGLE_API_KEY not set and not found in live service."
  echo "Run: export GOOGLE_API_KEY=your_key  then re-run."
  exit 1
fi
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
