# Job Intelligence Agent

A Google ADK agent for conversational job intelligence. The Sprint 0 agent looks up
synthetic jobs by ID from a local fixture. Use `JOB-001` to try the lookup.

## Set up on Windows

Install uv with WinGet, then open a new PowerShell window if `uv` is missing from
the current `PATH`.

```powershell
winget install --id=astral-sh.uv -e
```

From the repository root, install Python 3.13 and sync the locked dependencies.

```powershell
uv python install 3.13
uv sync --locked
```

If Windows Application Control blocks a module in uv-managed Python, install the
Python.org distribution and open a new PowerShell window. Then sync the project
with the system interpreter.

```powershell
winget install --id=Python.Python.3.13 -e --source winget
uv sync --locked --no-managed-python
```

## Configure the Gemini Developer API

For first-time setup, copy the template to the agent directory so ADK can load it.

```powershell
Copy-Item .env.example agents/job_intelligence/.env
```

Set `GOOGLE_API_KEY` in that local file using a key from [Google AI Studio](https://aistudio.google.com/app/apikey).
Leave `GOOGLE_GENAI_USE_ENTERPRISE=FALSE` for the Developer API. Set
`JOB_INTELLIGENCE_MODEL` to override the default `gemini-3.5-flash-lite` model.
Keep the local `.env` out of version control.

## Run locally

Launch the ADK development web UI from the repository root.

```powershell
uv run --locked adk web agents
```

Open [the local ADK UI](http://localhost:8000), select `job_intelligence`, and ask
“What is job JOB-001?”

For the terminal interface, run the following command and enter `exit` when done.

```powershell
uv run --locked adk run agents/job_intelligence
```

If Windows Application Control blocks the generated `adk.exe` launcher, run the
installed CLI entry point through Python. Choose either the web or terminal command.

```powershell
uv run --locked python -c 'from google.adk.cli import main; main()' web agents
uv run --locked python -c 'from google.adk.cli import main; main()' run agents/job_intelligence
```

## Run checks

The test suite uses local fixture data. After dependency setup, it runs offline
without any API keys.

```powershell
uv run --locked python -m pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

See [the architecture notes](docs/architecture.md) for the repository boundary and
future Google Cloud Agent Platform authentication.
