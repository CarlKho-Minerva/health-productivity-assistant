"""
Health Productivity Assistant — Google Cloud GenAI Academy APAC, Track 1 + Hackathon
Built with Google ADK + Gemini 2.0 Flash, deployed on Cloud Run.

Multi-agent architecture:
  root_agent (coordinator)
      ├── health_record_agent  — queries personal health vault (markdown files)
      └── tasks_agent          — manages tasks & reminders (SQLite database)

Health Passport (Android) → CAPTURE layer (on-device, private, offline)
Health Productivity Assistant → QUERY + MANAGE layer (cloud, Gemini-powered)
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from google.adk.agents import Agent

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HEALTH_VAULT_DIR = Path(__file__).parent / "health_vault"
DB_PATH = Path(__file__).parent / "tasks.db"


# ---------------------------------------------------------------------------
# Database init
# ---------------------------------------------------------------------------

def _init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                title     TEXT    NOT NULL,
                category  TEXT    NOT NULL DEFAULT 'general',
                priority  TEXT    NOT NULL DEFAULT 'normal',
                done      INTEGER NOT NULL DEFAULT 0,
                created_at TEXT   NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


_init_db()


# ---------------------------------------------------------------------------
# Health tools
# ---------------------------------------------------------------------------

def search_health_records(query: str) -> str:
    """Search the personal health vault for medical records matching the query.

    Use this for questions about: eye prescription, medications, lab results,
    BMI, blood pressure, cholesterol, diagnosed conditions, supplements,
    genetic variants, or any other health data.

    Args:
        query: Natural language question or keyword.

    Returns:
        Relevant markdown sections with source file citations.
    """
    if not HEALTH_VAULT_DIR.exists():
        return "Health vault directory not found."

    records: dict[str, str] = {}
    for md_file in HEALTH_VAULT_DIR.rglob("*.md"):
        records[str(md_file.relative_to(HEALTH_VAULT_DIR))] = md_file.read_text(encoding="utf-8")

    if not records:
        return "Health vault is empty."

    query_words = [w for w in query.lower().split() if len(w) > 2]
    matched = [
        f"--- Source: {fname} ---\n{content}"
        for fname, content in records.items()
        if any(w in content.lower() for w in query_words)
    ]

    if not matched:
        matched = [f"--- Source: {fname} ---\n{content}" for fname, content in records.items()]

    return "\n\n".join(matched)


# ---------------------------------------------------------------------------
# Task management tools (SQLite-backed)
# ---------------------------------------------------------------------------

def add_task(title: str, category: str = "general", priority: str = "normal") -> str:
    """Add a new task or health reminder to the database.

    Args:
        title:    Description of the task or reminder.
        category: One of 'health', 'medication', 'appointment', 'general'.
        priority: One of 'high', 'normal', 'low'.

    Returns:
        Confirmation with the new task ID.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, category, priority) VALUES (?, ?, ?)",
            (title, category, priority),
        )
        conn.commit()
        return f"Task #{cur.lastrowid} added: '{title}' [{category} / {priority}]"


def list_tasks(category: str = "all", show_done: bool = False) -> str:
    """List tasks from the database.

    Args:
        category:  Filter by category ('health', 'medication', 'appointment',
                   'general') or 'all' for everything.
        show_done: If True, include completed tasks.

    Returns:
        Formatted table of tasks.
    """
    query = "SELECT id, title, category, priority, done, created_at FROM tasks WHERE 1=1"
    params: list = []

    if category != "all":
        query += " AND category = ?"
        params.append(category)
    if not show_done:
        query += " AND done = 0"

    query += " ORDER BY done ASC, priority DESC, id ASC"

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(query, params).fetchall()

    if not rows:
        return "No tasks found."

    lines = ["| ID | Title | Category | Priority | Done | Created |",
             "|----|-------|----------|----------|------|---------|"]
    for row in rows:
        done = "✅" if row[4] else "⬜"
        lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {done} | {row[5][:10]} |")
    return "\n".join(lines)


def complete_task(task_id: int) -> str:
    """Mark a task as complete.

    Args:
        task_id: The numeric ID of the task to mark done.

    Returns:
        Confirmation or error.
    """
    with sqlite3.connect(DB_PATH) as conn:
        affected = conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)
        ).rowcount
        conn.commit()

    if affected:
        return f"Task #{task_id} marked as complete."
    return f"No task found with ID #{task_id}."


def delete_task(task_id: int) -> str:
    """Permanently delete a task by ID.

    Args:
        task_id: The numeric ID of the task to delete.

    Returns:
        Confirmation or error.
    """
    with sqlite3.connect(DB_PATH) as conn:
        affected = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,)).rowcount
        conn.commit()

    if affected:
        return f"Task #{task_id} deleted."
    return f"No task found with ID #{task_id}."


# ---------------------------------------------------------------------------
# Sub-agent: Health Record Agent
# ---------------------------------------------------------------------------

health_record_agent = Agent(
    name="health_record_agent",
    model="gemini-3-flash-preview",
    description=(
        "Queries the personal health vault. Use this sub-agent for any question "
        "about medical records: medications, lab results, eye prescription, "
        "diagnoses, supplements, genetic variants, biometrics."
    ),
    instruction="""\
You are the Health Record Agent. You have access to a personal health vault.

Rules:
1. ALWAYS call search_health_records before answering any health question.
2. Return structured markdown answers (headers, bullets, tables).
3. Always cite the source file (e.g., "Source: medications.md").
4. Never fabricate medical data. If not found, say so clearly.
5. You are not a doctor — do not give medical advice beyond what the records say.
""",
    tools=[search_health_records],
)


# ---------------------------------------------------------------------------
# Sub-agent: Tasks & Reminders Agent
# ---------------------------------------------------------------------------

tasks_agent = Agent(
    name="tasks_agent",
    model="gemini-3-flash-preview",
    description=(
        "Manages tasks, reminders, and to-dos. Use this sub-agent to add, list, "
        "complete, or delete tasks. Supports categories: health, medication, "
        "appointment, general."
    ),
    instruction="""\
You are the Tasks & Reminders Agent. You manage a personal task database.

Rules:
1. Use add_task to create new tasks or reminders.
2. Use list_tasks to show current tasks (default: incomplete only).
3. Use complete_task when the user marks something done.
4. Use delete_task only when explicitly asked to delete.
5. For health-related tasks (medication reminders, appointments), use the
   appropriate category ('medication', 'appointment', 'health').
6. Confirm every action with the task ID.
""",
    tools=[add_task, list_tasks, complete_task, delete_task],
)


# ---------------------------------------------------------------------------
# Root coordinator agent
# ---------------------------------------------------------------------------

root_agent = Agent(
    name="health_productivity_assistant",
    model="gemini-3-flash-preview",
    description=(
        "Primary coordinator for personal health and productivity management. "
        "Routes health questions to the health_record_agent and task/reminder "
        "requests to the tasks_agent."
    ),
    instruction="""\
You are the Health Productivity Assistant — a personal AI that helps users
manage their health records and daily tasks.

You coordinate two specialist sub-agents:
- health_record_agent: use for ANY question about health records, medications,
  lab results, diagnoses, prescriptions, or biometrics.
- tasks_agent: use for adding/listing/completing tasks, reminders, or to-dos.

Routing rules:
- "What's my eye prescription?" → health_record_agent
- "List my active medications" → health_record_agent
- "Remind me to take my vitamin D" → tasks_agent
- "What's on my health to-do list?" → tasks_agent
- "Add a task to book a cardiology follow-up" → tasks_agent
- Complex requests (e.g., "What medications do I take and remind me to refill fish oil")
  → call BOTH sub-agents sequentially and combine results.

Always greet the user briefly and present the answer in clean markdown.
Never fabricate data — only return what the sub-agents provide.
""",
    sub_agents=[health_record_agent, tasks_agent],
)
