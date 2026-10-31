# DSHA Agent / Anges MCP Hub

A small first step toward a phone-managed, extensible Agent. GitHub stores the code and runs tests; a separate host is required to keep the MCP server online.

## Included in this first milestone

- `create_study_plan`: a deterministic, time-boxed study-plan helper.
- `split_task`: converts a goal into a short checklist.
- Bearer-token guard for the MCP HTTP endpoint and a non-sensitive `/healthz` endpoint.
- GitHub Actions tests on pushes and pull requests.

## Deliberate limits

This is **not yet a full AI Agent**. It does not call a language model, retain conversation history, browse the web, access your phone, run shell commands, or modify files. Those capabilities should be added individually with explicit permission checks and tests.

## Local run (Python 3.11+)

1. `python -m pip install -r requirements.txt`
2. Set environment variable `MCP_BEARER_TOKEN` to a random secret of at least 32 characters. Do not commit it.
3. Set `MCP_ALLOWED_HOSTS` to comma-separated hostnames allowed to reach the service.
4. Run `python server.py`.
5. Health check: `http://127.0.0.1:8000/healthz`; MCP endpoint: `http://127.0.0.1:8000/mcp`.

Every MCP request must send `Authorization: Bearer <token>`. Use HTTPS for remote deployment.

## Deploy from a phone

You can edit/upload files through the GitHub mobile website and use Actions to run tests. GitHub Actions is not a permanent web server. A separate host is needed for a public HTTPS MCP endpoint; free-tier availability and sleep/usage limits depend on the provider and can change.

For a host such as Render, configure build command `pip install -r requirements.txt` and start command `uvicorn server:app --host 0.0.0.0 --port $PORT`. Add secret environment variable `MCP_BEARER_TOKEN` and set `MCP_ALLOWED_HOSTS` to the exact deployed hostname. Test `/healthz` and an authenticated MCP connection before connecting Anges.

## Secrets and safety

- Never commit `.env`, API keys, access tokens, or bearer tokens.
- Do not paste secrets into ChatGPT or public issues.
- Do not expose shell/file-management tools to an internet-facing server without strong authentication, authorization, and tests.
- Rotate a token immediately if it is exposed.
