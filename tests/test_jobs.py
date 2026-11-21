import pytest
from job_intelligence.fixture_repository import FixtureJobRepository
from job_intelligence.jobs import Job, lookup_job


def test_lookup_job_trims_whitespace():
    assert lookup_job(FixtureJobRepository(), "  JOB-001\t") == Job(
        job_id="JOB-001",
        title="Python Engineer",
        company="Example Software",
        location="Seattle, WA",
        job_url="https://example.com/jobs/job-001",
    )


@pytest.mark.parametrize("job_id", ["", " \t", "JOB-999", "job-001"])
def test_lookup_job_returns_none_for_missing_id(job_id):
    assert lookup_job(FixtureJobRepository(), job_id) is None
