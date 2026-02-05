#!/usr/bin/env python3
"""Minimal FastAPI gateway for RapidLink demos."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="RapidLink Gateway", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse("<h1>RapidLink Gateway</h1><p>Gateway bootstrap is running.</p>")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8081)
