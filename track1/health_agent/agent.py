"""
Health Record Query Agent
Google Cloud GenAI Academy APAC — Track 1: Build and Deploy AI Agents

Single ADK agent deployed on Cloud Run.
Task: answer natural language questions about personal health records.
"""

from pathlib import Path
from google.adk.agents import Agent

HEALTH_VAULT_DIR = Path(__file__).parent.parent / "health_vault"

# Files excluded from health record search (internal config, not data)
_PROMPT_FILES = [
    "system_prompt.md",
    "prompt_output_style.md",
    "prompt_tool_policy.md",
    "prompt_transparency.md",
]
_EXCLUDED_FROM_SEARCH = set(_PROMPT_FILES)


def search_health_records(query: str) -> str:
    """Search personal health vault markdown files for records matching the query.

    Use this for any health question: medications, lab results, eye prescription,
    diagnoses, supplements, biometrics, conditions.

    Args:
        query: Natural language question or keyword.

    Returns:
        Relevant markdown content with source file citations.
    """
    if not HEALTH_VAULT_DIR.exists():
        return "Health vault not found."

    records = {
        str(f.relative_to(HEALTH_VAULT_DIR)): f.read_text(encoding="utf-8")
        for f in HEALTH_VAULT_DIR.rglob("*.md")
        if f.name not in _EXCLUDED_FROM_SEARCH
    }

    if not records:
        return "Health vault is empty."

    words = [w for w in query.lower().split() if len(w) > 2]
    matched = [
        f"--- Source: {fname} ---\n{content}"
        for fname, content in records.items()
        if any(w in content.lower() for w in words)
    ] or [f"--- Source: {fname} ---\n{content}" for fname, content in records.items()]

    return "\n\n".join(matched)


def write_health_record(file_name: str, content: str) -> str:
    """Create or fully overwrite a health record markdown file.

    Use to create a new file or do a complete rewrite.
    For small targeted changes prefer patch_health_record.

    Args:
        file_name: Simple .md filename, e.g. 'lab_baselines.md'. No paths or subdirs.
        content: Full markdown content to write.

    Returns:
        Confirmation or error message.
    """
    if not file_name.endswith(".md") or "/" in file_name or ".." in file_name:
        return "Error: file_name must be a plain .md filename with no path components."
    target = HEALTH_VAULT_DIR / file_name
    target.write_text(content, encoding="utf-8")
    return f"OK: wrote {len(content)} chars to {file_name}."


def patch_health_record(file_name: str, old_text: str, new_text: str) -> str:
    """Find and replace an exact piece of text inside a health record file.

    Use this for targeted updates (single value, row, or section).
    The old_text must match exactly including whitespace.

    Args:
        file_name: Simple .md filename, e.g. 'lab_baselines.md'. No paths.
        old_text: Exact text to find (must appear exactly once).
        new_text: Replacement text.

    Returns:
        Confirmation or error message.
    """
    if not file_name.endswith(".md") or "/" in file_name or ".." in file_name:
        return "Error: file_name must be a plain .md filename with no path components."
    target = HEALTH_VAULT_DIR / file_name
    if not target.exists():
        return f"Error: {file_name} not found in health vault."
    current = target.read_text(encoding="utf-8")
    if old_text not in current:
        return f"Error: exact text not found in {file_name}. First call search_health_records to read the current content."
    updated = current.replace(old_text, new_text, 1)
    target.write_text(updated, encoding="utf-8")
    return f"OK: patched {file_name} ({len(old_text)} chars → {len(new_text)} chars)."


_DEFAULT_PROMPTS = {
    "system_prompt.md": """\
You are a Health Record Agent managing a personal health vault (markdown files).

Core constraints:
- Never fabricate data.
- Never give medical advice.
- Only report what is explicitly present in the records or the attached image.
- Always cite source file names.
""",
    "prompt_output_style.md": """\
Output contract:
- Prefer table-based outputs whenever data is tabular.
- Use short section headers.
- End every answer with a source line, for example: Source: lab_baselines.md
- If multiple files are used, include all relevant sources on one final line.
- If nothing relevant is found, say that clearly in one short paragraph.
""",
    "prompt_tool_policy.md": """\
Tool policy:
- Always call search_health_records before answering a health record question.
- For updates, first read current content with search_health_records.
- Use patch_health_record for targeted changes.
- Use write_health_record only for full rewrites or new files.
- Never tell the user to edit files manually if a tool can do it.
- If an image is attached, extract structured values from it before answering.
""",
    "prompt_transparency.md": """\
Transparency:
- These prompt files are editable in the Files tab and are the exact backend prompt stack in use.
- Runtime prompt order:
  1. system_prompt.md
  2. prompt_output_style.md
  3. prompt_tool_policy.md
  4. prompt_transparency.md
""",
}


def _ensure_prompt_files() -> None:
    for file_name, default_text in _DEFAULT_PROMPTS.items():
        target = HEALTH_VAULT_DIR / file_name
        if not target.exists():
            target.write_text(default_text, encoding="utf-8")


_ensure_prompt_files()


def _load_instruction(*args, **kwargs) -> str:
    """Load instruction from editable prompt stack files.
    Accepts any args/kwargs so ADK can call it with or without a context object.
    """
    parts = []
    for file_name in _PROMPT_FILES:
        prompt_file = HEALTH_VAULT_DIR / file_name
        if prompt_file.exists():
            parts.append(prompt_file.read_text(encoding="utf-8").strip())
    return "\n\n".join(part for part in parts if part)


root_agent = Agent(
    name="health_record_agent",
    model="gemini-3-flash-preview",
    description="Answers questions and manages personal health records.",
    instruction=_load_instruction,
    tools=[search_health_records, write_health_record, patch_health_record],
)
