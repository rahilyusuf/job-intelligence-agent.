import json

import pytest
from job_intelligence.agent import root_agent


def test_agent_registers_get_job():
    assert root_agent.name == "job_intelligence"
    (tool,) = root_agent.tools
    assert tool.__name__ == "get_job"


@pytest.mark.parametrize(
    ("job_id", "expected"),
    [
        (
            "JOB-001",
            {
                "job_id": "JOB-001",
                "title": "Python Engineer",
                "company": "Example Software",
                "location": "Seattle, WA",
                "job_url": "https://example.com/jobs/job-001",
            },
        ),
        ("JOB-999", None),
        (" ", None),
    ],
)
def test_get_job_tool_returns_json(job_id, expected):
    (tool,) = root_agent.tools
    result = tool(job_id)
    assert json.loads(json.dumps(result)) == {"job": expected}
