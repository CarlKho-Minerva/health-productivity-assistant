# Vault Provenance

*Auto-managed file. Explains the origin and nature of all health record files.*

## Patient Profile

This vault contains **demo/fictional data** for a patient persona named **Arjun Mukherjee (24M)**.
Arjun is a CS graduate student at BITS Pilani Hyderabad Campus. He is healthy overall, with only minor issues (mild myopia, seasonal dust allergies, Vitamin D insufficiency).
All values are plausible but entirely made up for demonstration purposes. No real personal health information is present.

## File Groups

### Health Records (10 files — searchable by agent)

| File | Content | Origin |
|------|---------|--------|
| `allergies.md` | Drug, food, and environmental allergies | Demo data (fictional) |
| `appointments.md` | Past and upcoming consultations | Demo data (fictional) |
| `biometrics.md` | Weight, BP, SpO2, annual check summary | Demo data (fictional) |
| `conditions.md` | Active diagnoses — minimal | Demo data (fictional) |
| `eyes.md` | Prescription, acuity, IOP, eye strain | Demo data (fictional) |
| `lab_baselines.md` | CBC, lipids, HbA1c, vitamins — all normal | Demo data (fictional) |
| `medical_expenses.md` | Costs in INR, student insurance | Demo data (fictional) |
| `medications.md` | Supplements only, no prescriptions | Demo data (fictional) |
| `therapy.md` | Wellness check-ins, not active therapy | Demo data (fictional) |
| `vaccinations.md` | Indian vaccination schedule | Demo data (fictional) |

### Prompt Stack (4 files — editable, excluded from agent search)
- `system_prompt.md` — core identity and constraints
- `prompt_output_style.md` — formatting rules
- `prompt_tool_policy.md` — when to use tools
- `prompt_transparency.md` — honesty and disclosure rules

### Meta / Transparency (2 files — excluded from agent search)
- `runtime_manifest.md` — auto-generated at startup; shows exact files + prompt stack
- `vault_provenance.md` — this file

## Modifying Records

Every file in the vault is editable live in the **Files tab** of the app.
The agent can also write and patch files using `write_health_record` and `patch_health_record`.
Changes take effect immediately — no restart required.
