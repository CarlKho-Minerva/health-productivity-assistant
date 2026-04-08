# Health Passport ADK — Final Slide Content
*Google Cloud GenAI Academy APAC | Updated for final hackathon submission*

---

## Slide 1 — Problem + Idea

**Project Name:** Health Passport AI

**Problem Statement:**
Medical history is fragmented across hospitals, cities, camera rolls, paper receipts, lab PDFs, and memory. Patients repeatedly re-explain medications, prescriptions, and recent lab values during every new consultation.

**Short validation lines to say on-slide:**
- Patients often cannot accurately recall their medication names and dosages.
- Incomplete patient-reported history contributes to preventable clinical errors.
- Health records are still frequently trapped in paper, PDF, or image form.
- Privacy concerns stop many users from adopting cloud-only health apps.

**Solution:**
Health Passport is a privacy-first health record assistant with two layers:

1. **Capture layer (existing Android app):** on-device document capture and structuring
2. **Query layer (new ADK agent):** natural-language Q&A over structured health records on Cloud Run

**Core idea:**
Keep raw capture private, but make records queryable with Gemini.

---

## Slide 2 — Architecture

| Layer | What it does | Tech |
|---|---|---|
| Mobile capture | Converts medical documents into structured records on-device | Android app + VLM pipeline |
| Health vault | Stores normalized markdown records | Editable `.md` files |
| Query agent | Answers questions, updates records, cites sources | Google ADK + Gemini 3 Flash Preview |
| API + UI | Serves chat, files, image, and audio flows | FastAPI + custom web UI |
| Deployment | Public serverless runtime | Google Cloud Run |

**Privacy split:**
- Raw document capture stays local-first
- Cloud side works on structured records and user queries
- Source citations and editable prompts keep the system transparent

---

## Slide 3 — What I Built

**Final prototype capabilities:**

- Natural-language health Q&A
- Table-based answers for labs, meds, vitals, appointments, and vaccines
- Clickable source citations that open the exact record file
- Editable Files tab for raw markdown records
- AI-powered file writing and patching
- Image upload for lab/photo extraction
- Audio / voice-note input using Gemini multimodal support
- Editable backend prompt stack visible in the app
- Dev mode that opens ADK Studio locally for inspection

**Why this is not a toy demo:**
- Public Cloud Run deployment
- Working GitHub repository
- Real ADK tool-calling workflow
- Multimodal input in one agent
- Transparent prompt stack instead of a hidden black box

---

## Slide 4 — End-to-End Flow

```text
User asks a question / attaches image / records a voice note
        ↓
FastAPI app packages text + multimodal attachments
        ↓
ADK Runner sends request to Gemini 3 Flash Preview
        ↓
Agent calls search_health_records()
        ↓
If user requests an update:
  patch_health_record() or write_health_record()
        ↓
Gemini returns a structured answer with source citations
        ↓
User clicks Source → exact file opens in Files tab
```

**Example queries:**
- “What is my current eye prescription?”
- “Latest lab results?”
- “My cholesterol is 102 now, update it.”
- “Extract this lab image and save it.”
- “Summarise this voice note and add it to my records.”

---

## Slide 5 — Feature List + Outcomes

| Feature | Outcome |
|---|---|
| Search across health vault | Fast retrieval across multiple record types |
| Table-first output style | Easy for doctors/users to scan |
| Clickable source chips | Verifiable answers, no hidden citations |
| Files tab editor | Manual transparency + quick correction workflow |
| AI patch/write tools | Users can update records from chat |
| Image input | Turns visual reports into structured data |
| Audio input | Supports spoken notes and quick updates |
| Editable prompt files | Makes backend behavior inspectable |
| Cloud Run deployment | Public, shareable submission URL |

**Current vault categories in prototype:**
allergies, appointments, biometrics, conditions, eyes, labs, medical expenses, medications, therapy, vaccinations, and prompt files.

---

## Slide 6 — Technologies + Submission Links

| Layer | Technology |
|---|---|
| Agent framework | Google ADK |
| Model | Gemini 3 Flash Preview |
| Backend | FastAPI + Python 3.11 |
| Frontend | Custom HTML/CSS/JS chat UI |
| Multimodal inputs | Text, image, audio |
| Deployment | Google Cloud Run |
| Repository | GitHub |

**Submission links:**
- Cloud Run: https://health-record-agent-hd4kqp35da-uc.a.run.app
- GitHub: https://github.com/CarlKho-Minerva/health-productivity-assistant

**Closing line:**
Health Passport turns scattered medical history into a portable, privacy-aware, queryable health record system built with ADK and Gemini.
