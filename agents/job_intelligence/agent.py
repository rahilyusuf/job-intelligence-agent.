import os

from google.adk.agents import Agent

from .fixture_repository import FixtureJobRepository
from .tools import build_get_job_tool

root_agent = Agent(
    name="job_intelligence",
    model=os.getenv("JOB_INTELLIGENCE_MODEL", "gemini-3.5-flash-lite"),
    description="Looks up job records by ID in the local development fixture.",
    instruction=(
        "Use get_job to look up a job when the user supplies a job ID. "
        "Ask for the job ID if it is missing. Answer from the returned record, "
        "including the job URL when relevant. If the result contains a null job, "
        "say that the job ID was not found in the development fixture."
    ),
    tools=[build_get_job_tool(FixtureJobRepository())],
)
