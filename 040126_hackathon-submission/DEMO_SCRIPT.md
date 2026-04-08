# Health Passport AI — Demo Video Script
*Loom · target ~3 min · no edits needed, one take*

---

## Setup before hitting record
- [ ] Browser open at `http://0.0.0.0:8080` (or the Cloud Run URL) — Chat tab, clean state
- [ ] Local ADK web UI open at `http://localhost:8000` in a separate tab (for the Dev jump)
- [ ] Health vault files intact (`lab_baselines.md`, `medications.md`, `eyes.md`, `conditions.md`)
- [ ] Have a lab report photo ready on your phone or desktop (any old receipt/screenshot works for the image demo)
- [ ] Kill any old session: open DevTools → Application → Local Storage → delete `hp_sess`

---

## The Script

### [0:00 – 0:30] Hook — the real problem

> *Show: just you, talking. Or start on the welcome screen of the app.*

"I'm a Minerva University student. I rotate across seven cities every semester — San Francisco, Seoul, Hyderabad, Buenos Aires, London, Berlin, Taipei.

Every single time I walk into a new clinic or hospital, the doctor asks: *'Do you have your previous records?'* And I'm digging through my camera roll, DMing myself lab PDFs in three languages, trying to remember whether my LDL was flagged last December.

**[1]** 70% of patients can't accurately recall their own medication names and dosages.
**[2]** 1-in-5 medical errors trace back to incomplete patient-reported history.
**[3]** Average patient sees 19 doctors over their lifetime — each one starting from scratch.

That is the problem. And I built Health Passport to fix it."

---

### [0:30 – 1:00] Product context — two halves

> *Show: app header. Point at 'CLOUD AI' badge.*

"Health Passport has two halves.

The **Android app** — already shipped — scans any medical document directly on your phone using a vision-language model running on the Qualcomm NPU. No cloud upload. Zero data leaves your device.

**[4]** 63% of patients cite privacy concerns as the main reason they don't use digital health tools.

That's the capture side: fully private, on-device.

**This web agent** is the query side — built for Google Cloud GenAI Academy using ADK and Gemini, deployed on Cloud Run. You ask a question in plain English, it searches your local health vault and gives you a structured, cited answer.

**[5]** The vault only stores *your* structured markdown. The cloud agent never sees your raw documents — just the question."

---

### [1:00 – 1:40] Live demo — Chat

> *Show: type each query into the chat input, hit send, let the response load*

**Query 1 — "What is my current eye prescription?"**

> While it loads: "Watch the tool badge — it shows `search_health_records()` was called."

> When the answer appears: "Sphere, cylinder, axis — structured. And see that `Source: eyes.md` badge — click it."

> *Click the green `eyes.md` chip — it jumps to the Files tab, opens the raw markdown*

"That opens the raw file directly in the editor. You can fix a typo, update a value, save it — and the agent immediately sees the new version on the next query."

> *Go back to Chat*

**Query 2 — "My total cholesterol is 102 now, update it"**

> "Watch this one — I'm telling it to write, not just read."

> *Let it respond — it calls `search_health_records` then `patch_health_record`*

"It looked up the existing value, found the exact line, patched it in-place. No manual file editing required.

**[6]** That's the core loop for chronic disease management — values change, records should stay current. The agent just closed that loop."

---

### [1:40 – 2:10] Image upload demo

> *Show: click the paperclip icon in the input bar*

"Here's the feature I'm most excited about for the full product.

**[7]** 80% of medical records are still generated as paper or scanned PDFs — never structured, never searchable.

I'll attach a photo of a lab report."

> *Select any lab slip image from your files*

> *Type: "Extract the values from this and save them to my records"*

> *Hit send — let it process*

"Gemini reads the image — **[8]** multimodal models now match specialist-level accuracy on medical document parsing — extracts the values, and writes them directly to the health vault. Photo to structured, searchable record in one message."

---

### [2:10 – 2:35] Dev mode

> *Click 'Dev' button in the header — ADK Studio opens in new tab*

"The Dev button opens ADK Studio — that's the official Google ADK inspection UI. You can see the full agent run: tool calls, function responses, token counts, the exact prompt chain.

**[9]** Built entirely with Google ADK's `Agent` class and the Runner API — exactly the pattern from the GenAI Academy curriculum, extended with custom FastAPI endpoints for the chat UI, file CRUD, and multimodal input."

> *Switch back to the chat tab*

---

### [2:35 – 3:00] Close

> *Show: app header — 'Health Passport · CLOUD AI'*

"**[10]** 425 million people with chronic conditions worldwide need a tool that travels with them, speaks to any doctor, and never compromises their privacy.

Health Passport is that tool. The Android app captures. This agent queries. Together they're a portable, privacy-first medical record system that fits in your pocket and works in any city.

Built with Google ADK, Gemini 3 Flash Preview, deployed on Cloud Run.

The code is on GitHub — link in the description."

---

## Links to add in Loom description

```
Live app:  https://health-record-agent-hd4kqp35da-uc.a.run.app
GitHub:    https://github.com/CarlKho-Minerva/health-productivity-assistant
```

---

## Quick cheat sheet — tool badge appearances

| Query | Tools that fire | What to say |
|---|---|---|
| Eye prescription | `search_health_records()` | "read-only lookup" |
| Update cholesterol | `search_health_records()` → `patch_health_record()` | "search then write" |
| Summarise profile | `search_health_records()` | "scans all files" |
| Lab photo | `search_health_records()` → `write_health_record()` | "image → structured data" |
