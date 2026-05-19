from nautobot.core.celery import register_jobs

from .job_a import JobA
from .job_b import JobB

register_jobs(JobA, JobB)
