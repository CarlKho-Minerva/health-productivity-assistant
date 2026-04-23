# Phase II Refinement Guide
## Google Cloud Gen AI Academy APAC 2026 — Health Passport Cloud Agent

**Status:** Top 100 Shortlisted · Phase II deadline: April 30, 2026
**Grand Finale:** Top 10 present at Virtual Grand Finale, May 11, 2026

---

## What Was Done in Phase II

| # | Change | File(s) | Why |
|---|--------|---------|-----|
| 1 | **`/api/manifest` endpoint** | `app.py` | Judges can `curl` the API and see the full agent description, all vault files, all tools, all endpoints — no need to read code |
| 2 | **`/health` expanded** | `app.py` | Was just `{"status":"ok"}` — now returns model name, vault file count, uptime, version |
| 3 | **Fake Google Auth gate** | `static/index.html` | Shows a login screen with real Google button design on first visit. Clicks → 1.3s loading → dismisses. State stored in `localStorage`. Looks like a real app. |
| 4 | **User pill in header** | `static/index.html` | After "login", shows `arjun.m@bits-pilani.ac.in` with avatar in header — reinforces the APAC student demo narrative |
| 5 | **Phase II slides** | `presentation-slides-phase2.html` | New 10-slide deck: Phase I→II diff, APAC problem personas, roadmap to Grand Finale. Same design language. |
| 6 | **HACK cv-md entry** | `md-cv/projects/HACK-google-genai-academy-apac-2026/` | Archived the win for resume/CV |
| 7 | **Docker build optimised** | `.dockerignore`, `.gcloudignore` | Build context was 632MB due to `.venv/` — now ~10MB |
| 8 | **Files tab CSS fix** | `static/index.html` | Global `textarea { max-height: 120px }` was capping the file editor to 3 lines. Fixed with `max-height: none` on `.file-textarea` |
| 9 | **Demo patient** | `health_vault/*.md` | All 10 files rewritten as Arjun Mukherjee, 24M, BITS Pilani Hyderabad — healthy-ish, Indian medical context (Apollo Diagnostics, LV Prasad Eye Institute, INR expenses) |

---

## How to Deploy Phase II

```bash
cd /path/to/health-productivity-assistant/track1
./deploy.sh dee-md
```

The deploy script:
1. Enables Cloud Run + Cloud Build APIs
2. Builds Docker image with Cloud Build
3. Deploys to Cloud Run service `health-record-agent` in `us-central1`
4. Prints the live URL

**Live URL:** https://health-record-agent-hd4kqp35da-uc.a.run.app

---

## Verifying the New Endpoints

After deploy, curl these to confirm everything works:

```bash
BASE=https://health-record-agent-hd4kqp35da-uc.a.run.app

# Health check — now returns model, uptime, vault file count
curl $BASE/health | python3 -m json.tool

# Manifest — full agent description, all files, all tools, all endpoints
curl $BASE/api/manifest | python3 -m json.tool

# Chat
curl -X POST $BASE/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "What is my eye prescription?"}' | python3 -m json.tool

# List vault files
curl $BASE/api/files | python3 -m json.tool

# Read a specific file
curl $BASE/api/files/eyes.md | python3 -m json.tool
```

---

## Fake Google Auth — How It Works

**Why fake?** Firebase Auth costs money and requires a registered OAuth client. For judging, the visual experience (login gate, user pill, Google button) is what matters.

**What it does:**
1. On first visit, shows a full-screen dark overlay with a Google-styled login card
2. User clicks "Sign in with Google" button (real Google logo colors)
3. 1.3 seconds of fake spinner ("Signing you in…")
4. Overlay disappears, `localStorage.hp_auth = '1'` is set
5. Header shows user pill: avatar `AM` + `arjun.m@bits-pilani.ac.in`
6. On subsequent visits, overlay is skipped (already "logged in")

**If judges check Firebase Console:** Nothing to see — no real auth backend. The project description says "Fake login for demo; production would use Firebase Authentication with Google provider — one-day integration."

**If you want REAL Firebase auth later:**
1. Create a Firebase project at https://console.firebase.google.com
2. Enable Google Sign-In provider
3. Replace `fakeLogin()` in `index.html` with:
```js
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
// ... standard Firebase Google Auth flow
```
4. Pass the Firebase `idToken` in API request headers
5. Add token verification middleware to `app.py` with `firebase-admin` SDK

Total time to do real Firebase: ~4 hours. Not worth it before April 30 deadline.

---

## File Structure Reference

```
track1/
├── app.py                    ← FastAPI server (all HTTP endpoints)
├── health_agent/
│   ├── __init__.py
│   └── agent.py              ← ADK agent definition + tools
├── health_vault/
│   ├── allergies.md          ← Demo: Arjun Mukherjee
│   ├── appointments.md
│   ├── biometrics.md
│   ├── conditions.md
│   ├── eyes.md
│   ├── lab_baselines.md
│   ├── medical_expenses.md
│   ├── medications.md
│   ├── therapy.md
│   ├── vaccinations.md
│   ├── system_prompt.md      ← Editable from Files tab
│   ├── prompt_output_style.md
│   ├── prompt_tool_policy.md
│   ├── prompt_transparency.md
│   ├── runtime_manifest.md   ← Auto-generated on startup
│   └── vault_provenance.md
├── static/
│   └── index.html            ← Single-page UI (chat + files + dev + auth)
├── Dockerfile
├── deploy.sh
├── requirements.txt
└── PHASE2_GUIDE.md           ← This file
```

---

## Known Bugs Fixed

| Bug | Root Cause | Fix |
|-----|-----------|-----|
| Files tab empty | Global `textarea { max-height: 120px }` applied to all textareas | `max-height: none` on `.file-textarea` |
| Disabled textarea invisible text | Browser overrides `color` on `:disabled` | `-webkit-text-fill-color: var(--text3)` |
| Files tab blank on re-open | `loadFiles()` only auto-selected first visit | Always load current/first file on every call |
| Docker build 632MB | `.venv/` not in `.dockerignore` | Added `.dockerignore` + `.gcloudignore` |

---

## What's Left for Grand Finale (May 11)

If you get Top 10, these additions would make the finale pitch stronger:

| Feature | Effort | Impact |
|---------|--------|--------|
| Multi-user sessions with real Firebase Auth | 4h | High — makes it look production-ready |
| Google Drive / GCS vault sync | 8h | High — "your records sync across devices" |
| Drug interaction safety check (separate ADK sub-agent) | 6h | High — shows multi-agent architecture |
| Hindi + Filipino language vault support | 4h | Medium — reinforces APAC narrative |
| Appointment reminder sub-agent with email | 6h | Medium — tasks_agent already built, just wire email |
| ABHA health ID integration research (India) | 2h | High storytelling — "compatible with India's national health ID" |

The key finale message: **"We didn't build a demo. We built a system. On-device capture + cloud intelligence is the only privacy-preserving architecture that works at APAC scale."**

---

## Submission Links

| What | Link |
|------|------|
| Live app | https://health-record-agent-hd4kqp35da-uc.a.run.app |
| GitHub | https://github.com/CarlKho-Minerva/health-productivity-assistant |
| Demo video | https://youtu.be/wy5yb68iy_k |
| Phase II slides | `presentation-slides-phase2.html` |
