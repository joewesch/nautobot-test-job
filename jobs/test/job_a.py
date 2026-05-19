from nautobot.core.celery import register_jobs

from .adapters.adapter_a import AdapterA
from .base.base_job import BaseJob


class JobA(BaseJob):
    adapter_class = AdapterA

    class Meta:
        name = "NTC-5779 Reproducer: Job A"
        description = "Exercises AdapterA -> ServiceA -> Result.count() comparison."


register_jobs(JobA)
