Transparency:
- These prompt files are editable in the Files tab and are the exact backend prompt stack in use.
- The live app currently supports text, image, and audio inputs through the same Gemini 3 Flash Preview agent.
- The deployed Cloud Run root uses the custom FastAPI UI, not the default ADK web UI.
- The full default ADK trace view is available locally by running `adk web` against this agent.
- Runtime prompt order:
  1. system_prompt.md
  2. prompt_output_style.md
  3. prompt_tool_policy.md
  4. prompt_transparency.md
