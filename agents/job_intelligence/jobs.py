from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Job:
    job_id: str
    title: str
    company: str
    location: str
    job_url: str


class JobRepository(Protocol):
    def get_by_id(self, job_id: str) -> Job | None: ...


def lookup_job(repository: JobRepository, job_id: str) -> Job | None:
    job_id = job_id.strip()
    if not job_id:
        return None
    return repository.get_by_id(job_id)
