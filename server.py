"""Starter MCP service for the DSHA Agent / Anges project.

Initial scope: low-risk deterministic tools only. No shell execution, arbitrary
filesystem access, external network requests, or model API calls.
"""
from __future__ import annotations

import hmac
import os
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from core import build_study_plan, split_task


mcp = FastMCP("DSHA Agent MCP Hub")


@mcp.tool()
def create_study_plan(subjects: list[str], available_minutes: int = 180) -> dict[str, Any]:
    """为给定科目生成一个可执行的分时学习计划。"""
    return build_study_plan(subjects, available_minutes)


@mcp.tool(name="split_task")
def split_task_tool(task: str) -> dict[str, Any]:
    """把目标拆成安全、可执行的下一步清单；本工具不会执行任何操作。"""
    return split_task(task)


class AccessGuardMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # This health check returns no secrets and is intentionally public.
        if request.url.path == "/healthz":
            return await call_next(request)

        allowed_hosts = {
            item.strip().lower().split(":", 1)[0]
            for item in os.getenv("MCP_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")
            if item.strip()
        }
        request_host = request.headers.get("host", "").lower().split(":", 1)[0]
        if not request_host or request_host not in allowed_hosts:
            return JSONResponse({"error": "Host not allowed"}, status_code=421)

        expected = os.getenv("MCP_BEARER_TOKEN", "").strip()
        if len(expected) < 32:
            return JSONResponse(
                {"error": "MCP_BEARER_TOKEN must be configured as a random value of at least 32 characters"},
                status_code=503,
            )
        auth = request.headers.get("authorization", "")
        scheme, _, supplied = auth.partition(" ")
        if scheme.lower() != "bearer" or not supplied or not hmac.compare_digest(supplied, expected):
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)


app = FastAPI(title="DSHA Agent MCP Hub", version="0.1.0")


@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "dsha-agent-mcp-hub"}


app.mount("/", mcp.streamable_http_app())
app.add_middleware(AccessGuardMiddleware)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
