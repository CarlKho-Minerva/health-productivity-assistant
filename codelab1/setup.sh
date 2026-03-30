#!/usr/bin/env bash
# ============================================================
# CODELAB 1 - Build and deploy an ADK agent on Cloud Run
# Run this ENTIRE script in Google Cloud Shell (dee-md project)
# Usage: bash setup.sh
# ============================================================
set -e

# ---- CONFIG (change these if needed) ----
PROJECT_ID="dee-md"
REGION="europe-west1"
SA_NAME="lab2-cr-service"
SERVICE_NAME="zoo-tour-guide"
MODEL="gemini-2.5-flash"
# -----------------------------------------

echo ""
echo "==> [1/6] Setting project to ${PROJECT_ID}"
gcloud config set project "${PROJECT_ID}"

echo ""
echo "==> [2/6] Enabling required APIs (this takes ~1 min)..."
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  compute.googleapis.com

echo ""
echo "==> [3/6] Creating service account ${SA_NAME}..."
gcloud iam service-accounts create "${SA_NAME}" \
  --display-name="Service Account for Codelab 1" 2>/dev/null || echo "  (service account already exists, continuing)"

PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")
SERVICE_ACCOUNT="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo ""
echo "==> [4/6] Granting Vertex AI User role to service account..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/aiplatform.user" --quiet

echo ""
echo "==> [5/6] Setting up Python virtual environment..."
cd ~/codelab1
uv venv 2>/dev/null || python3 -m venv .venv
source .venv/bin/activate || source .venv/bin/activate

echo ""
echo "==> Installing dependencies..."
pip install --quiet google-adk==1.14.0 langchain-community==0.3.27 wikipedia==1.4.0

echo ""
echo "==> Writing .env file for zoo_guide_agent..."
cat > zoo_guide_agent/.env << EOF
PROJECT_ID=${PROJECT_ID}
PROJECT_NUMBER=${PROJECT_NUMBER}
SA_NAME=${SA_NAME}
SERVICE_ACCOUNT=${SERVICE_ACCOUNT}
MODEL="${MODEL}"
EOF

echo ""
echo "==> [6/6] DEPLOYING to Cloud Run..."
echo "    >> When asked 'Do you want to continue (Y/n)?' — type Y"
echo "    >> When asked 'Allow unauthenticated invocations?' — type y"
echo ""

uvx --from google-adk==1.14.0 \
  adk deploy cloud_run \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --service_name="${SERVICE_NAME}" \
  --app_name=zoo_guide_agent \
  --with_ui \
  --service_account="${SERVICE_ACCOUNT}"

echo ""
echo "================================================================"
echo " DONE! Open the Service URL above in your browser."
echo " 1. Toggle ON 'Token Streaming' (top right)"
echo " 2. Type: hello"
echo " 3. Then ask: Where can I find the polar bears and what is their diet?"
echo " 4. SCREENSHOT the response (shows tool invocations: wikipedia, etc.)"
echo " 5. Upload screenshot to Hack2skill > Forms Tab > Lab Completion 1"
echo "================================================================"
echo ""
echo "==> CLEANUP (run AFTER taking screenshot):"
echo "  gcloud run services delete ${SERVICE_NAME} --region ${REGION} --quiet"
echo "  gcloud artifacts repositories delete cloud-run-source-deploy --location ${REGION} --quiet"
