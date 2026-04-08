"""
Health Record Query Agent
Google Cloud GenAI Academy APAC — Track 1: Build and Deploy AI Agents

Single ADK agent deployed on Cloud Run.
Task: answer natural language questions about personal health records.
"""

from pathlib import Path
from google.adk.agents import Agent

HEALTH_VAULT_DIR = Path(__file__).parent.parent / "health_vault"


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


root_agent = Agent(
    name="health_record_agent",
    model="gemini-2.5-flash",
    description="Answers natural language questions about personal health records.",
    instruction="""\
You are a Health Record Agent for a personal health vault.

1. ALWAYS call search_health_records before answering.
2. Return structured markdown (headers, bullets, tables).
3. Cite the source file in every answer (e.g., "Source: medications.md").
4. Never fabricate data. If not found, say clearly.
5. You are not a doctor — only report what the records contain.
""",
    tools=[search_health_records],
)
