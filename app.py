#!/usr/bin/env python3
"""Backend for the IAM demo console.

Serves the static frontend and proxies invoke requests to the deployed
IAM platform, so the browser never needs to deal with CORS and the IAM
URL/credentials stay editable per-request instead of hardcoded.
"""
from pathlib import Path

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="IAM Console")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvokeRequest(BaseModel):
    iam_url: str
    agent_id: str
    secret: str
    tool_id: str
    operation: str
    payload: dict = {}


@app.post("/api/invoke")
def api_invoke(req: InvokeRequest):
    url = f"{req.iam_url.rstrip('/')}/agents/{req.agent_id}/invoke"
    try:
        r = requests.post(
            url,
            json={
                "secret": req.secret,
                "tool_id": req.tool_id,
                "operation": req.operation,
                "payload": req.payload or {},
            },
            timeout=15,
        )
    except requests.RequestException as e:
        return {"error": f"could not reach IAM at {url}: {e}"}

    try:
        body = r.json()
    except ValueError:
        body = {"raw": r.text}

    return {"http_status": r.status_code, "response": body}


static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
