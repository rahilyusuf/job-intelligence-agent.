from collections.abc import Callable
from dataclasses import asdict

from .jobs import JobRepository, lookup_job


def build_get_job_tool(
    repository: JobRepository,
) -> Callable[[str], dict[str, dict[str, str] | None]]:
    def get_job(job_id: str) -> dict[str, dict[str, str] | None]:
        """Look up a job by its case-sensitive ID, such as JOB-001.

        Args:
            job_id: The exact job ID to look up.

        Returns:
            A job record with its URL, or a null job if no record matches.
        """
        job = lookup_job(repository, job_id)
        return {"job": asdict(job) if job is not None else None}

    return get_job
