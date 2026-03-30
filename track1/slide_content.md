# Track 1 — PPT Slide Content
*Google Cloud GenAI Academy APAC | Copy-paste directly into the template*

---

## Slide 1 — Participant Details

**a. Participant name:** Carl Kho

**b. Problem Statement:**
Build and deploy a single AI agent using ADK and Gemini that is hosted on Cloud Run and performs one clearly defined task — answering natural language questions about personal health records.

**Brief about the idea:**

I rotate across 7 cities every semester as a Minerva University student. At every new hospital or clinic, I have to re-explain my full medical history from memory — prescriptions buried in camera roll photos, lab reports in 3 languages, no structured record I can hand a doctor.

Health Passport (my existing Android app) already solves the *capture* side: it scans any medical document on-device using a Vision-Language Model on the Qualcomm Hexagon NPU — zero cloud upload, full privacy.

The **Health Record Query Agent** is the cloud complement: a single ADK agent deployed on Cloud Run that lets you ask natural language questions about your health history and get structured, cited answers via Gemini.

- *"What is my current eye prescription?"*
- *"List my active medications and dosages"*
- *"What are my latest cholesterol results?"*

---

## Slide 2 — Meeting the Build Criteria

| Requirement | Implementation |
|---|---|
| Implemented using ADK | `Agent` class from `google.adk`, tool-using architecture |
| Uses a Gemini model | Gemini 2.5 Flash Preview (`gemini-3-flash-preview`) |
| One clearly defined task | Natural language health record Q&A with cited sources |
| Accepts input, returns response | JSON input → structured markdown response |
| HTTP endpoint on Cloud Run | `POST /run` — publicly accessible, serverless |

**How I navigated Track 1 requirements:**

Rather than building a toy demo, I connected ADK to a real personal health vault — 4 markdown files covering eyes/vision, medications, lab baselines, and active conditions — sourced directly from Health Passport's on-device output format. The agent uses a `search_health_records` tool that keyword-searches the vault and hands matching records to Gemini for synthesis. Every response cites its source file. The whole thing deploys in one command via Cloud Build + Cloud Run.

---

## Slide 3 — Opportunities

**How is it different from existing ideas?**
- Most health AI apps require uploading your medical documents to the cloud — Health Passport does not. Capture is entirely local (NPU inference on Qualcomm Snapdragon). The cloud agent only receives the *question*, never the raw documents.
- Backed by a real shipped product: working APK on Google Drive, Play Store listing in progress, YouTube demo, built across 4 countries of real health records.
- Privacy-split architecture is intentional, not incidental — it's the core design decision.

**How does it solve the problem?**
- Capture (Health Passport Android): scan any medical document → structured markdown, on-device
- Query (this agent): ask anything about your health history → Gemini synthesizes and cites

**USP:**
Privacy-first hybrid architecture. On-device capture + cloud intelligence. Real product — not a lab exercise.

---

## Slide 4 — Features

- **Natural Language Q&A** — ask in plain English, get structured answers
- **Source Citations** — every answer references its source file (e.g., "Source: medications.md")
- **Structured Output** — markdown with headers, tables, bullet points
- **Health Vault Search** — `search_health_records` tool scans body systems, protocols, lab baselines, conditions
- **Gemini-Powered Synthesis** — understands medical terminology and context
- **HTTP API** — `POST /run` callable from any client
- **Serverless** — Cloud Run scales to zero, no idle cost

---

## Slide 5 — Process Flow

```
User
  │
  ▼ POST /run {"text": "What is my eye prescription?"}
Cloud Run — ADK api_server
  │
  ▼
root_agent (Gemini 2.5 Flash)
  │  understands intent
  ▼
search_health_records("eye prescription")
  │  keyword search
  ▼
health_vault/eyes.md  ← returns markdown content
  │
  ▼
Gemini synthesizes answer + cites source
  │
  ▼
{"response": "**Myopic Astigmatism** ...\nSource: eyes.md"}
  │
  ▼
User
```

**Privacy architecture:**

```
📱 Health Passport (Android)            ☁️ Health Agent (Cloud Run)
   On-device NPU inference                ADK + Gemini 2.5 Flash
   Camera → VLM → Markdown export→        POST /run ← question only
   ZERO cloud upload                      vault searched locally in container
   ──────────────────────                 ──────────────────────────────────
   CAPTURE (private)                      QUERY (cloud)
```

---

## Slide 6 — Technologies

| Layer | Technology |
|---|---|
| Agent Framework | Google ADK (Agent Development Kit) |
| LLM | Gemini 2.5 Flash Preview |
| Deployment | Google Cloud Run (serverless container) |
| Language | Python 3.11 |
| Container | Docker |
| Data | Markdown health vault (4 files) |
| On-device (existing) | Nexa SDK · Qwen VL · PaddleOCR v4 · Qualcomm Hexagon NPU |
| Repo | github.com/CarlKho-Minerva/health-productivity-assistant |

---

*For the actual PPT file: open `../presentation-slides.html` in Chrome → Cmd+P → Save as PDF*
