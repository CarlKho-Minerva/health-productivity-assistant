#!/usr/bin/env bash
# ============================================================
# CODELAB 2 - Building AI Agents with ADK: The Foundation
# Run this ENTIRE script in Google Cloud Shell
# Usage: bash setup.sh
# ============================================================
set -e

# ---- CONFIG ----
PROJECT_ID="dee-md"
REGION="us-central1"
# ----------------

echo ""
echo "==> [1/4] Setting project to ${PROJECT_ID}"
gcloud config set project "${PROJECT_ID}"

echo ""
echo "==> [2/4] Enabling Vertex AI API..."
gcloud services enable aiplatform.googleapis.com

echo ""
echo "==> [3/4] Setting up Python environment..."
cd ~/codelab2
uv venv --python 3.12 2>/dev/null || python3 -m venv .venv
source .venv/bin/activate

echo ""
echo "==> Installing google-adk..."
uv pip install google-adk 2>/dev/null || pip install google-adk

echo ""
echo "==> Writing .env for personal_assistant..."
cat > personal_assistant/.env << EOF
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=${PROJECT_ID}
GOOGLE_CLOUD_LOCATION=${REGION}
EOF

echo ""
echo "================================================================"
echo " [4/4] DONE with setup! Now run the agent web UI:"
echo ""
echo "   source .venv/bin/activate"
echo "   adk web"
echo ""
echo " Then click the Web Preview button (top right of Cloud Shell),"
echo " select port 8000, and chat with the agent."
echo ""
echo " Test it:"
echo "   Type: hello. What can you do for me?"
echo ""
echo " SCREENSHOT the chat response in the web UI."
echo " Upload screenshot to Hack2skill > Forms Tab > Lab Completion 2"
echo "================================================================"
