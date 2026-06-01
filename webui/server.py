#!/usr/bin/env python3
"""Local web UI for the E-commerce Ops Analyst.

Run:
  OPENAI_API_KEY=... python3 webui/server.py

Optional:
  OPENAI_MODEL=gpt-5-mini PORT=8787 python3 webui/server.py
"""

from __future__ import annotations

import json
import os
import sys
import time
import traceback
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "webui" / "static"
DEFAULT_MODEL = "gpt-5-mini"
PORT = int(os.getenv("PORT", "8787"))
DEBUG_RESPONSE_FILE = ROOT / "outputs" / "webui_last_openai_response.json"
TRANSIENT_OPENAI_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504, 520, 522, 524}


CONTEXT_FILES = [
    "agent/ecommerce_ops_analyst_system_prompt.md",
    "outputs/business_recommendations/WEEKLY_OPS_BRIEF.md",
    "outputs/business_recommendations/BUSINESS_RECOMMENDATIONS.md",
    "outputs/business_recommendations/business_recommendations.csv",
    "outputs/AI_ANALYST_DEMO_QA.md",
    "ontology/actions.yml",
    "ontology/objects.yml",
    "ontology/links.yml",
    "wiki/ecommerce-ops-ontology/06-ai-analyst-behavior.md",
    "wiki/ecommerce-ops-ontology/07-evals-and-governance.md",
]


def read_text(path: str, limit: int | None = None) -> str:
    full_path = ROOT / path
    if not full_path.exists():
        return f"[missing: {path}]"
    text = full_path.read_text(encoding="utf-8", errors="replace")
    if limit and len(text) > limit:
        return text[:limit] + "\n[truncated]\n"
    return text


def load_context() -> str:
    parts = []
    for path in CONTEXT_FILES:
        parts.append(f"\n\n--- FILE: {path} ---\n{read_text(path)}")
    return "\n".join(parts)


PROJECT_CONTEXT = load_context()


def load_env_file() -> None:
    for name in [".env.local", ".env", "webui/.env.local", "webui/.env"]:
        path = ROOT / name
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def extract_output_text(response: dict[str, Any]) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"]

    chunks: list[str] = []
    for item in response.get("output", []) or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []) or []:
            if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                chunks.append(content["text"])
    if chunks:
        return "\n".join(chunks).strip()

    # Be tolerant of minor API shape changes: recursively collect text fields
    # from message content only, while avoiding ids, metadata, and tool payloads.
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("text"), str) and value.get("type") in {"output_text", "text", "message"}:
                chunks.append(value["text"])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(response.get("output", []))
    return "\n".join(dict.fromkeys(chunk.strip() for chunk in chunks if chunk.strip()))


def response_debug_summary(response: dict[str, Any]) -> str:
    output = response.get("output", []) or []
    output_types = []
    for item in output:
        if not isinstance(item, dict):
            continue
        content_types = [
            content.get("type")
            for content in item.get("content", []) or []
            if isinstance(content, dict)
        ]
        output_types.append({"type": item.get("type"), "content_types": content_types})
    return (
        f"OpenAI returned no final text. status={response.get('status')}; "
        f"incomplete_details={response.get('incomplete_details')}; output={output_types}"
    )


def call_openai(question: str, history: list[dict[str, str]]) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "ok": False,
            "error": "OPENAI_API_KEY is not set. Start the server with OPENAI_API_KEY=your_key python3 webui/server.py",
        }

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    history_text = "\n".join(
        f"{message.get('role', 'user').upper()}: {message.get('content', '')}"
        for message in history[-8:]
        if message.get("content")
    )

    instructions = f"""
You are running inside the local E-commerce Ops Analyst web UI.

Follow the analyst system prompt and ontology rules below. Answer as an operator-facing analyst, not as a generic assistant.

Critical behavior:
- Use BusinessRecommendation records as the action memory.
- Give direct recommendations with evidence.
- Keep every action status as proposed unless context says otherwise.
- Do not claim real actions were executed.
- Use cautious causal language.
- If asked "what should I do", return the top operating actions, not a table explanation.
- Write for a business operator, not a data engineer.
- Avoid raw field names like low_review_rate, late_delivery_rate, target_id, source_view.
- Translate action types into plain English before showing formal names.
- Always start with "Bottom line:" and end with "Recommended next step:" when explaining a recommendation.
- Prefer 3 prioritized items unless the user asks for more.

PROJECT CONTEXT:
{PROJECT_CONTEXT}
""".strip()

    input_text = f"""
Conversation so far:
{history_text or "(none)"}

Current user question:
{question}
""".strip()

    payload = {
        "model": model,
        "instructions": instructions,
        "input": input_text,
        "max_output_tokens": 3000,
        "reasoning": {"effort": "minimal"},
        "text": {"verbosity": "medium"},
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    last_error = ""
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                data = json.loads(response.read().decode("utf-8"))
            answer = extract_output_text(data)
            if answer:
                return {"ok": True, "answer": answer, "model": model}
            DEBUG_RESPONSE_FILE.parent.mkdir(parents=True, exist_ok=True)
            DEBUG_RESPONSE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return {"ok": False, "error": response_debug_summary(data), "debug_file": str(DEBUG_RESPONSE_FILE)}
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            last_error = f"OpenAI API error {exc.code}: {body}"
            if exc.code not in TRANSIENT_OPENAI_STATUS_CODES or attempt == 2:
                return {"ok": False, "error": last_error}
            time.sleep(2**attempt)
        except Exception as exc:  # pragma: no cover - local demo diagnostics
            return {"ok": False, "error": f"{type(exc).__name__}: {exc}", "trace": traceback.format_exc()}

    return {"ok": False, "error": last_error or "OpenAI API request failed."}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/":
            path = "/index.html"
        if path == "/api/status":
            self.send_json(
                {
                    "ok": True,
                    "model": os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
                    "has_api_key": bool(os.getenv("OPENAI_API_KEY")),
                    "recommendations": 94,
                }
            )
            return

        file_path = (STATIC / path.lstrip("/")).resolve()
        if not str(file_path).startswith(str(STATIC.resolve())) or not file_path.exists():
            self.send_error(404)
            return

        content_type = "text/plain"
        if file_path.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        elif file_path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif file_path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"

        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/api/chat":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            question = str(payload.get("message", "")).strip()
            history = payload.get("history", [])
            if not question:
                self.send_json({"ok": False, "error": "Message is required."}, status=400)
                return
            if not isinstance(history, list):
                history = []
            result = call_openai(question, history)
            self.send_json(result, status=200 if result.get("ok") else 500)
        except Exception as exc:
            self.send_json({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, status=500)


def main() -> None:
    load_env_file()
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"E-commerce Ops Analyst UI: http://127.0.0.1:{PORT}")
    print(f"Model: {os.getenv('OPENAI_MODEL', DEFAULT_MODEL)}")
    print("Set OPENAI_API_KEY before asking live questions.")
    server.serve_forever()


if __name__ == "__main__":
    main()
