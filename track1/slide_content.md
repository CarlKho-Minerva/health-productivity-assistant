# Track 1 Project Submission — Slide Content
**Google Cloud GenAI Academy APAC | Cohort 1**

---

## Slide 1 — Participant Details

**a. Participant name:** Carl Kho

**b. Problem Statement:**
Build and deploy a single AI agent using ADK and Gemini that is hosted on Cloud Run and performs one clearly defined task — answering natural language questions about personal health records.

---

## Slide 2 — Brief About the Idea

I rotate across 7 global cities every semester as a Minerva student. Each new country means re-explaining my complete medical history — prescriptions lost in camera roll photos, lab reports in three languages, no structured record I can hand a doctor.

**Health Passport** (Android app, Feb 2026) solves the capture problem: point camera at any medical document → on-device Vision-Language Model extracts structured data → saved as organized markdown records. Zero cloud upload. Privacy by architecture.

**Health Record Agent** (this submission) is the complementary cloud layer: ask natural language questions about your captured health records and get cited, structured answers via Gemini.

- "What's my current eye prescription?" → returns prescription with source file
- "List my active medications and dosages" → structured table
- "What were my last cholesterol results?" → lab baseline data

---

## Slide 3 — Meeting the Build Criteria

How the solution addresses the Track 1 "What You Must Build" criteria:

| Requirement | Implementation |
|---|---|
| Implemented using ADK | `Agent` defined with `google.adk`, tool-using architecture |
| Uses a Gemini model | Gemini 2.5 Flash Preview for NL understanding + response |
| One clearly defined task | Natural language health record Q&A with source citations |
| Accepts input, returns response | JSON input (query) → structured markdown answer |
| HTTP endpoint on Cloud Run | Deployed serverless container, publicly accessible via POST `/run` |

**Beyond the minimum:** Backed by a real shipped Android app (Health Passport) with a Play Store listing in progress — not synthetic or lab-generated data.

---

## Slide 4 — Opportunities

**How is it different from existing ideas?**
- Most health AI apps require cloud upload of medical documents — this one doesn't. Capture stays fully on-device.
- Architecture intentionally separates capture (private) from queries (cloud) — a real privacy-aware design, not a lab exercise.
- Backed by a working Android APK, YouTube demo, and Play Store listing — not just a demo.

**How will it solve the problem?**
- Scan any medical document on-device → auto-organized health vault
- Ask any health question → Gemini answers from your vault with cited source files
- Works across healthcare systems, countries, and languages

**USP of the proposed solution:**
- Privacy-first hybrid architecture (on-device capture + cloud queries)
- Production-ready: working APK, Play Store listing pending, YouTube demo live
- Battle-tested system prompts refined over 6 months of real multi-country health records
- Complete pipeline: capture → organize → query

---

## Slide 5 — List of Features

**Health Record Agent (Cloud — this submission):**
- Natural language health queries ("What's my eye prescription?" / "List active medications")
- Cited responses — every answer references its source file (e.g., `Source: medications.md`)
- Structured output — markdown with headers, tables, bullet points
- HTTP API endpoint — callable via `POST /run` for programmatic access
- Gemini 2.5 Flash — understands medical terminology and context
- Search across body systems, lab baselines, medications, conditions

**Health Passport (On-Device Android — existing foundation):**
- Document scanning — prescriptions, lab reports, medical receipts
- On-device VLM (Qwen VL on Qualcomm Hexagon NPU) — zero cloud upload
- Auto-organization into body systems, timeline, protocols
- Health vault browser — navigate records by category
- Lab baselines tracking — anthropometrics, blood work, vitals
- Medication tracking — active meds with dosage and frequency

---

## Slide 6 — Process Flow Diagram

```
CAPTURE LAYER (On-Device — Health Passport Android)
┌──────────────────────────────────────────────┐
│  Medical Document                            │
│       ↓ Camera                               │
│  On-Device VLM (Qwen VL · Qualcomm NPU)     │
│       ↓ Zero cloud upload                    │
│  Structured Markdown → Health Vault          │
└──────────────────────────────────────────────┘
                    ↕ user exports vault
QUERY LAYER (Google Cloud — this submission)
┌──────────────────────────────────────────────┐
│  User: "What's my eye prescription?"         │
│       ↓ HTTP POST /run                        │
│  ADK Agent (Cloud Run)                       │
│       ↓ calls tool                           │
│  search_health_records() → markdown files   │
│       ↓ context injected                     │
│  Gemini 2.5 Flash                            │
│       ↓                                      │
│  Structured answer + source citation         │
└──────────────────────────────────────────────┘
```

**Technologies:**
- Agent Framework: Google ADK
- LLM: Gemini 2.5 Flash Preview
- Deployment: Google Cloud Run (serverless)
- Language: Python
- Data: Markdown health vault (4 files: eyes, medications, lab baselines, conditions)
- On-device (existing): Nexa SDK · Qwen VL · PaddleOCR v4 · Qualcomm Hexagon NPU · Android/Kotlin

---

## Slide 7 — Snapshots

- **Track 1 repo:** https://github.com/CarlKho-Minerva/health-productivity-assistant/tree/master/track1
- **Health Passport Android:** https://github.com/CarlKho-Minerva/health-passport-android
- **YouTube demo:** https://www.youtube.com/watch?v=2JNhoXNvsCo
- **Contact:** kho@uni.minerva.edu
