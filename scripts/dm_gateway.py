#!/usr/bin/env python3
"""FastAPI gateway with basic cluster process controls."""

from __future__ import annotations

from asyncio.subprocess import Process
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

ROOT_DIR = Path(__file__).resolve().parents[1]
NODE_PROCS: dict[str, Process] = {}
app = FastAPI(title="RapidLink Gateway", version="0.3.0")


class NodeAction(BaseModel):
    node_id: str


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse("<h1>RapidLink Gateway</h1><p>Cluster controls are enabled.</p>")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/cluster/state")
def cluster_state() -> dict[str, list[str]]:
    return {"running": sorted(NODE_PROCS)}


@app.post("/cluster/start")
async def cluster_start() -> dict[str, str]:
    return {"status": "started"}


@app.post("/cluster/kill")
async def kill_node(action: NodeAction) -> dict[str, str]:
    if action.node_id not in NODE_PROCS:
        raise HTTPException(status_code=404, detail="unknown node")
    return {"status": "killed", "node": action.node_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8081)
