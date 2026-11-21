# Project Guidelines

## Build and Test

- Use Python 3.13 and `uv`. Setup: `uv python install 3.13` followed by `uv sync --locked`.
- Run the full offline test suite with `uv run --locked python -m pytest`.
- Run one test file with `uv run --locked python -m pytest tests/test_jobs.py`; run one test by name with `uv run --locked python -m pytest tests/test_jobs.py::test_lookup_job_trims_whitespace`.
- Run lint and formatting checks with `uv run --locked ruff check .` and `uv run --locked ruff format --check .`.
- Launch the local ADK web UI with `uv run --locked adk web agents`; launch the terminal agent with `uv run --locked adk run agents/job_intelligence`.
- Copy `.env.example` to `agents/job_intelligence/.env` for local API configuration. Keep credentials in that local file; tests do not require API keys.

## Architecture

- `agents/job_intelligence/agent.py` defines the ADK-discoverable `root_agent`, selects the Gemini model from `JOB_INTELLIGENCE_MODEL`, and binds the `get_job` tool to a repository instance.
- `jobs.py` contains the framework-independent `Job` model, `JobRepository` protocol, and `lookup_job` application behavior.
- `tools.py` adapts repository lookups to the ADK tool contract and serializes a successful result as `{"job": {...}}` or a missing result as `{"job": null}`.
- `fixture_repository.py` implements the repository protocol by loading `fixtures/jobs.json` once into an ID-indexed mapping.
- `tests/` verifies both pure lookup behavior and the ADK tool registration/result shape. See `docs/architecture.md` for repository boundaries and planned BigQuery and Agent Platform integration.

## Conventions

- Preserve the repository boundary: ADK setup belongs in `agent.py` and `tools.py`; lookup rules belong in `jobs.py`; storage adapters implement `JobRepository`.
- Use the existing `JobRepository.get_by_id(job_id)` protocol for future adapters. It returns `Job | None` and should keep storage details out of the tool and lookup layers.
- Keep job IDs case-sensitive. `lookup_job` trims surrounding whitespace but must not alter or normalize the ID's case.
- Keep `Job` immutable and ensure fixture and future adapter records include `job_id`, `title`, `company`, `location`, and `job_url`.
- Return `null` from the tool for blank or unknown IDs; do not add fallback records or invented job data.
- Keep fixture-backed tests offline and deterministic. ADK agent tests may inspect `root_agent.tools`, but do not require Gemini API calls.
