# Hackathon — Health Productivity Assistant
**Google Cloud GenAI Academy APAC | Carl Kho | kho@uni.minerva.edu**

Multi-agent AI system for personal health + productivity management.

## Architecture
```
root_agent (health_productivity_assistant)
├── health_record_agent  → search_health_records() → markdown health vault
└── tasks_agent          → add/list/complete/delete_task() → SQLite DB
```

## Quick Deploy
```bash
export GOOGLE_API_KEY=your_key_here
bash deploy.sh
```

## Example Queries
- `"What is my eye prescription?"` → health_record_agent
- `"List my active medications"` → health_record_agent
- `"Add a reminder to take vitamin D"` → tasks_agent
- `"What meds do I take AND remind me to refill fish oil"` → both agents

## Stack
- Google ADK + Gemini 2.5 Flash Preview
- Cloud Run · SQLite · Docker · Python
