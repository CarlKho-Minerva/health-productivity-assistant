"""
Custom FastAPI server for Health Passport AI.
Serves a beautiful chat UI + proxies to ADK agent via Runner API.
"""
import os
import uuid
import asyncio
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# --- ADK setup ---
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from health_agent.agent import root_agent

APP_NAME = "health_agent"
STATIC_DIR = Path(__file__).parent / "static"

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

app = FastAPI(title="Health Passport AI")


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    user_id: str = "user"


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/chat")
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    user_id = req.user_id

    # Ensure session exists
    try:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        if session is None:
            await session_service.create_session(
                app_name=APP_NAME, user_id=user_id, session_id=session_id
            )
    except Exception:
        try:
            await session_service.create_session(
                app_name=APP_NAME, user_id=user_id, session_id=session_id
            )
        except Exception:
            pass

    content = types.Content(role="user", parts=[types.Part(text=req.message)])
    response_text = ""
    tools_used = []

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            # Capture tool calls
            if hasattr(event, "content") and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        fn = part.function_call.name
                        if fn and fn not in tools_used:
                            tools_used.append(fn)

            # Capture final text
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            response_text += part.text
    except Exception as e:
        response_text = f"Error: {str(e)}"

    return {
        "response": response_text or "I couldn't find relevant records. Try rephrasing.",
        "session_id": session_id,
        "tools_used": tools_used,
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
