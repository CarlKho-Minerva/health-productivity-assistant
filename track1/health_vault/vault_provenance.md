# Vault Provenance

This app answers from markdown files in `track1/health_vault`.

Visible file groups:
- Core health files: `conditions.md`, `eyes.md`, `lab_baselines.md`, `medications.md`
- Added demo/mock files: `allergies.md`, `appointments.md`, `biometrics.md`, `medical_expenses.md`, `therapy.md`, `vaccinations.md`
- Prompt stack files: `system_prompt.md`, `prompt_output_style.md`, `prompt_tool_policy.md`, `prompt_transparency.md`

Commit provenance for demo/mock content:
- `ee5ab90` added `vaccinations.md`, `medical_expenses.md`, initial editable `system_prompt.md`, and initial `biometrics.md`
- `3b5c34b` added `allergies.md`, `appointments.md`, `therapy.md`, and expanded `biometrics.md`
- `4595e48` updated prompt files and refreshed some demo record content for the final demo

Important:
- The agent does not read hidden database rows or hidden backend memory.
- It reads the visible markdown files shown in the Files tab.
- If those files are edited or deleted, the output changes accordingly.
