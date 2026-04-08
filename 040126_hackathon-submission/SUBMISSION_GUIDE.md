# H2S Submission Guide

## Paste these into the form

**Cloud Run Deployment Link**
https://health-record-agent-hd4kqp35da-uc.a.run.app

**GitHub Repository Link**
https://github.com/CarlKho-Minerva/health-productivity-assistant

**Final Project PPT / PDF to upload**
- PDF: `040126_hackathon-submission/final_project_ppt.pdf`
- PPTX: `040126_hackathon-submission/final_project_pptx.pptx`

**Demo Video Link**
- Record Loom, then paste the Loom share URL here

---

## Fastest submit order

1. Record Loom using `040126_hackathon-submission/DEMO_SCRIPT.md`
2. Copy Loom share link
3. Upload `final_project_ppt.pdf`
4. Paste Cloud Run URL
5. Paste GitHub URL
6. Paste Loom URL
7. Submit

---

## Slide-by-slide fixes for Google Slides template

### Slide 1 — Problem + Idea
**Title:** Health Passport AI

**Keep on slide:**
- Problem: medical history is fragmented across hospitals, cities, PDFs, images, and memory
- Idea: privacy-first health record assistant with local capture + cloud query

**Use these validation lines:**
- Patients often cannot accurately recall their medication names and dosages.
- Incomplete patient-reported history contributes to preventable clinical errors.
- Health records are still frequently trapped in paper, PDF, or image form.
- Privacy concerns stop many users from adopting cloud-only health apps.

### Slide 2 — Architecture
Use the table from `track1/slide_content.md`.

**Key visual point:**
- Left side: Android on-device capture
- Right side: Cloud Run + ADK + Gemini 3 Flash Preview
- Footer callout: raw capture stays local, cloud only handles structured records and queries

### Slide 3 — What I Built
Replace any old feature list with:
- natural-language Q&A
- table-based outputs
- clickable source citations
- Files tab editor
- AI patch/write tools
- image upload
- audio / voice note input
- editable prompt stack
- ADK Studio dev inspection

### Slide 4 — End-to-End Flow
Use the exact flow from `track1/slide_content.md`.

**On-slide examples:**
- What is my current eye prescription?
- Latest lab results?
- My cholesterol is 102 now, update it.
- Extract this lab image and save it.
- Summarise this voice note and add it to my records.

### Slide 5 — Feature List + Outcomes
Use the table from `track1/slide_content.md`.

**Important line to keep:**
Current vault categories: allergies, appointments, biometrics, conditions, eyes, labs, medical expenses, medications, therapy, vaccinations, and prompt files.

### Slide 6 — Technologies + Links
Keep it simple:
- Google ADK
- Gemini 3 Flash Preview
- FastAPI + Python 3.11
- custom HTML/CSS/JS frontend
- text + image + audio input
- Cloud Run
- GitHub repo

**Include these links in small text:**
- Cloud Run: https://health-record-agent-hd4kqp35da-uc.a.run.app
- GitHub: https://github.com/CarlKho-Minerva/health-productivity-assistant

**Closing line:**
Health Passport turns scattered medical history into a portable, privacy-aware, queryable health record system built with ADK and Gemini.

---

## Demo order for the Loom

1. Ask: "What is my current eye prescription?"
2. Click the source chip to open the file
3. Ask: "My total cholesterol is 102 now, update it"
4. Attach one image and say: "Extract this and save it"
5. Record one short voice note and send it
6. Click Dev to mention ADK Studio
7. End on Cloud Run + GitHub

---

## Optional 4-person cold open
If you use the 4 people with you, keep each line under 3 seconds and keep the total cold open under 12 seconds.
