from nautobot.core.celery import register_jobs

from .adapters.adapter_b import AdapterB
from .base.base_job import BaseJob


class JobB(BaseJob):
    adapter_class = AdapterB

    class Meta:
        name = "NTC-5779 Reproducer: Job B"
        description = "Exercises AdapterB -> ServiceA -> Result.count() comparison."


register_jobs(JobB)
