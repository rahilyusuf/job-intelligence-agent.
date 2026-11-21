import json
from pathlib import Path

from .jobs import Job

_FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "jobs.json"


class FixtureJobRepository:
    def __init__(self) -> None:
        with _FIXTURE_PATH.open(encoding="utf-8") as fixture:
            records = json.load(fixture)
        jobs = (Job(**record) for record in records)
        self._jobs = {job.job_id: job for job in jobs}

    def get_by_id(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)
