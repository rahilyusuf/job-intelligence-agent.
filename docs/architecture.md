# Architecture

## Repository responsibility

`job-intelligence-agent` answers conversational questions about job records.
`agentic-job-harvester` owns ingestion, normalization, BigQuery persistence, and
embeddings. Sprint 0 exercises the local lookup path with synthetic records.

## Lookup flow

1. ADK discovers `root_agent` in `agents/job_intelligence/agent.py`. That module
   registers `get_job(job_id: str)` with a fixture repository supplied at startup.
2. The tool delegates to the application lookup in `jobs.py` and returns an object
   with a `job` key. Its value is a job record or `null` for a blank or unknown ID.
3. The application trims surrounding whitespace and uses the read-only
   `JobRepository.get_by_id` protocol. IDs are case-sensitive. The fixture adapter
   loads bundled JSON once per repository instance, indexes it by ID, and returns
   job records that include `job_url`.

The application and fixture adapter can be imported and exercised without ADK.
The fixture keeps development deterministic. The single-method protocol gives a
future adapter a small contract without exposing storage details to the tool.

## Future read-only BigQuery adapter

Implement `get_by_id` against an agreed harvester-owned table or view. Bind the job
ID as a query parameter in a fixed `SELECT` and map the returned columns to `Job`.
Grant the runtime identity permission to run query jobs and read the approved
data. Confirm the source schema and ID uniqueness with the harvester project
before building the adapter. [BigQuery parameterized queries](https://docs.cloud.google.com/bigquery/docs/parameterized-queries)

## Future Google Cloud Agent Platform authentication

The [local Gemini Developer API setup](../README.md#configure-the-gemini-developer-api)
uses an AI Studio key. A future Agent Platform setup would use Application Default
Credentials. For local development, run `gcloud auth application-default login`.
Set `GOOGLE_GENAI_USE_ENTERPRISE=TRUE`, `GOOGLE_CLOUD_PROJECT`, and
`GOOGLE_CLOUD_LOCATION` for the approved project and location. For a hosted
workload, use a workload identity with the required IAM permissions. [Agent Platform authentication guide](https://adk.dev/get-started/google-cloud/)

BigQuery access, A2A, A2UI, Gemini Enterprise integration, additional agents, and
deployment are deferred to later milestones.
