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
_EXCLUDED_FROM_SEARCH = {"system_prompt.md"}


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


_DEFAULT_INSTRUCTION = """\
You are a Health Record Agent managing a personal health vault (markdown files).

**Reading:**
1. ALWAYS call search_health_records before answering any health question.
2. Return structured markdown (headers, bullets, tables).
3. Cite the source file (e.g., "Source: lab_baselines.md").
4. Never fabricate data. If not found, say clearly.
5. You are not a doctor — only report what the records contain.

**Writing / Updating:**
6. When the user asks to update, change, add, or record a new value:
   a. Call search_health_records first to read the exact current content.
   b. Use patch_health_record for targeted changes (single value or row).
   c. Use write_health_record only when creating a new file or doing a full rewrite.
   d. After patching, confirm the change and show the updated value.
   e. NEVER tell the user to edit files manually — do it yourself with the tools.

**Images:**
7. If the user provides an image (e.g. a lab report photo), extract all values from it.
   Then offer to update the health vault automatically using patch/write tools.
"""


def _load_instruction(*args, **kwargs) -> str:
    """Load instruction from system_prompt.md if present, else use default.
    Accepts any args/kwargs so ADK can call it with or without a context object.
    """
    prompt_file = HEALTH_VAULT_DIR / "system_prompt.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return _DEFAULT_INSTRUCTION


root_agent = Agent(
    name="health_record_agent",
    model="gemini-3-flash-preview",
    description="Answers questions and manages personal health records.",
    instruction=_load_instruction,
    tools=[search_health_records, write_health_record, patch_health_record],
)
