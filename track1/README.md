# Track 1 — Health Record Query Agent
**Google Cloud GenAI Academy APAC | Carl Kho | kho@uni.minerva.edu**

Single ADK agent on Cloud Run that answers natural language health record questions using Gemini.

## Quick Deploy
```bash
export GOOGLE_API_KEY=your_key_here
bash deploy.sh
```

## Test
```bash
curl -X POST YOUR_CLOUD_RUN_URL/run \
  -H "Content-Type: application/json" \
  -d '{"app_name":"health_record_agent","user_id":"demo","session_id":"s1","new_message":{"role":"user","parts":[{"text":"What is my eye prescription?"}]}}'
```

## Stack
- Google ADK + Gemini 2.5 Flash Preview
- Cloud Run (serverless)
- Health vault: 4 markdown files (eyes, medications, lab baselines, conditions)
