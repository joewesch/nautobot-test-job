import sys

from nautobot.apps.jobs import Job

from .base.adapters import BaseAdapter
from .base.dataclasses import Change


class JobA(Job):
    class Meta:
        name = "NTC-5779 Reproducer: Job A"
        description = "Demonstrates split-module-identity bug for a shared base dataclass."

    def run(self):
        adapter = BaseAdapter()
        adapter.populate()

        adapter_class = type(adapter.changes[0])
        job_class = Change

        self.logger.info(
            "Adapter's Change: id=%s module=%s file=%s",
            id(adapter_class),
            adapter_class.__module__,
            getattr(sys.modules.get(adapter_class.__module__), "__file__", "?"),
        )
        self.logger.info(
            "Job's    Change: id=%s module=%s file=%s",
            id(job_class),
            job_class.__module__,
            getattr(sys.modules.get(job_class.__module__), "__file__", "?"),
        )

        if adapter_class is job_class:
            self.logger.info("Class identity MATCHES.")
        else:
            self.logger.error("Class identity DIFFERS. Two distinct class objects from the same source file.")

        unfiltered = adapter.count()
        filtered = adapter.count(data_type=Change)

        self.logger.info("count() unfiltered           = %d", unfiltered)
        self.logger.info("count(data_type=Change) = %d (expected %d)", filtered, unfiltered)

        if filtered != unfiltered:
            self.logger.error("BUG REPRODUCED: isinstance() check failed across split class identities.")
        else:
            self.logger.info("All good: isinstance() check held.")
