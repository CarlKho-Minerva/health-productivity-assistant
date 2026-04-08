# Vault Provenance

*Auto-managed file. Explains the origin and nature of all health record files.*

## Patient Profile

This vault contains **demo/fictional data** for a patient persona named **Alex Rivera (31M)**.
All values are plausible but entirely made up for demonstration purposes. No real personal health information is present.

## File Groups

### Health Records (10 files — searchable by agent)
These are the files the agent reads when you ask health questions:

| File | Content | Origin |
|------|---------|--------|
| `allergies.md` | Drug, food, and environmental allergies | Demo data (fictional) |
| `appointments.md` | Past and upcoming consultations | Demo data (fictional) |
| `biometrics.md` | Weight, BP, SpO2, annual PEC summary | Demo data (fictional) |
| `conditions.md` | Active diagnoses by body system | Demo data (fictional) |
| `eyes.md` | Prescription, acuity, IOP, active symptoms | Demo data (fictional) |
| `lab_baselines.md` | CBC, lipid panel, HbA1c, vitamins, imaging | Demo data (fictional) |
| `medical_expenses.md` | Out-of-pocket costs, insurance, HSA | Demo data (fictional) |
| `medications.md` | Daily protocol + PRN + stopped meds | Demo data (fictional) |
| `therapy.md` | Mental health sessions, PHQ-9, GAD-7, goals | Demo data (fictional) |
| `vaccinations.md` | Routine + travel vaccines | Demo data (fictional) |

### Prompt Stack (4 files — editable, excluded from agent search)
These control the agent's behavior:
- `system_prompt.md` — core identity and constraints
- `prompt_output_style.md` — formatting rules
- `prompt_tool_policy.md` — when to use tools
- `prompt_transparency.md` — honesty and disclosure rules

### Meta / Transparency (2 files — excluded from agent search)
- `runtime_manifest.md` — auto-generated at startup; shows exact files + prompt stack
- `vault_provenance.md` — this file

## Modifying Records

Every file in the vault is editable in the **Files tab** of the app.
The agent can also write and patch files using the `write_health_record` and `patch_health_record` tools.
Changes take effect immediately — no restart required.
