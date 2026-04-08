# Health Passport AI — Demo Video Script
*Loom · target ~3 min · solo by default, optional 4-person cold open*

---

## Setup before hitting record
- [ ] Browser open at `http://0.0.0.0:8080` (or the Cloud Run URL) — Chat tab, clean state
- [ ] Local ADK web UI open at `http://localhost:8000` in a separate tab (for the Dev jump)
- [ ] Health vault files intact (`lab_baselines.md`, `medications.md`, `eyes.md`, `conditions.md`)
- [ ] Have a lab report photo ready on your phone or desktop (any old receipt/screenshot works for the image demo)
- [ ] Browser mic permission enabled if you want to record a voice note live
- [ ] Kill any old session: open DevTools → Application → Local Storage → delete `hp_sess`

---

## The Script

### [0:00 – 0:12] Optional cold open — 4 quick validation voices

> *Use only if you want outside voices. Keep each clip under 3 seconds.*

Person 1: "I never remember my latest lab numbers when a doctor asks."

Person 2: "My records are scattered across screenshots, PDFs, and random emails."

Person 3: "I hate uploading medical documents to cloud apps I don't trust."

Person 4: "I wish I could just ask one system what matters and get the source."

Then cut immediately to your screen.

---

### [0:12 – 0:35] Hook — the real problem

> *Show: just you, talking. Or start on the welcome screen of the app.*

"Right now I'm in Hyderabad for a semester — BITS Pilani campus. Before this, San Francisco. Next semester, somewhere else entirely.

Every time I arrive in a new city and walk into a clinic, the first thing the doctor asks is: *'Do you have your previous records?'* And I'm digging through my camera roll, forwarding PDFs to myself, trying to remember if my Vitamin D was flagged two months ago and whether I updated my glasses prescription since then.

This is the demo patient — Arjun Mukherjee, a student here in Hyderabad. But this scenario? It's real.

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

**Query 2 — "My Vitamin D result just came back at 32 ng/mL — I've been on supplements 3 months, update it"**

> "Watch this one — I'm telling it to write, not just read. Arjun was Vitamin D insufficient at 21.2 — now supplemented and rechecked."

> *Let it respond — it calls `search_health_records` then `patch_health_record`*

"It found the existing lab entry, located the exact value, patched it in-place, added the updated date. No manual file editing.

**[6]** That's the core loop — a recheck comes back, you tell the agent, it updates the record. Values stay current without you ever opening a markdown file."

---

### [1:40 – 2:00] Image upload demo

> *Show: click the paperclip icon in the input bar*

"Here's the feature I'm most excited about for the full product.

**[7]** 80% of medical records are still generated as paper or scanned PDFs — never structured, never searchable.

I'll attach a photo of a lab report."

> *Select any lab slip image from your files*

> *Type: "Extract the values from this and save them to my records"*

> *Hit send — let it process*

"Gemini reads the image — **[8]** multimodal models now match specialist-level accuracy on medical document parsing — extracts the values, and writes them directly to the health vault. Photo to structured, searchable record in one message."

---

### [2:00 – 2:20] Audio / voice-note demo

> *Show: click the mic button and record one short sentence*

Say into the mic:

"I had a therapy session last week, felt less anxious, and my next follow-up is April 22. Summarise this and tell me where it belongs in my records."

> *Stop recording, then hit send*

"This uses the same Gemini 3 Flash Preview agent, but now with audio input. It can process a voice note, extract the medically relevant information, and turn spoken context into structured output. That matters because health updates often happen in conversation, not in typed form."

---

### [2:20 – 2:40] Dev mode

> *Click 'Dev' button in the header — ADK Studio opens in new tab*

"The Dev button opens ADK Studio — that's the official Google ADK inspection UI. You can see the full agent run: tool calls, function responses, token counts, the exact prompt chain.

**[9]** Built entirely with Google ADK's `Agent` class and the Runner API — exactly the pattern from the GenAI Academy curriculum, extended with custom FastAPI endpoints for the chat UI, file CRUD, and multimodal input."

> *Switch back to the chat tab*

---

### [2:40 – 3:00] Close

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
| Voice note | `search_health_records()` | "audio → structured summary" |
