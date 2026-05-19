import sys

from nautobot.apps.jobs import Job

from .dataclasses import Change
from .services import ServiceA


class BaseJob(Job):
    adapter_class = None

    class Meta:
        abstract = True
        name = "NTC-5779 Reproducer: Base Job"
        description = "Base job for the NTC-5779 Reproducer."

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls, "adapter_class", None) is None:
            raise ValueError(f"{cls.__name__} must set adapter_class")

    def _change_class_id(self):
        return id(Change)

    def _dump_change_classes_in_sys_modules(self):
        seen = {}
        for name, mod in list(sys.modules.items()):
            change = getattr(mod, "Change", None)
            if change is None or not isinstance(change, type):
                continue
            if getattr(change, "__name__", None) != "Change":
                continue
            seen.setdefault(id(change), []).append(name)
        self.logger.info("Distinct Change class objects alive in sys.modules: %d", len(seen))
        for cid, holders in seen.items():
            self.logger.info("  Change id=%s held by %d module(s): %s", cid, len(holders), holders)

    def run(self):
        adapter = self.adapter_class()
        service = ServiceA(adapter, self.logger)

        self.logger.info(
            "Pre-sync Change-id snapshot: base_job=%s adapter=%s services=%s",
            self._change_class_id(),
            adapter.change_class_id(),
            service.change_class_id(),
        )

        self._dump_change_classes_in_sys_modules()

        result = service.sync()

        if not result.changes:
            self.logger.warning("Adapter %s produced no changes; nothing to compare.", adapter.name)
            return

        sample = type(result.changes[0])
        job_view = Change

        self.logger.info(
            "Adapter's Change: id=%s module=%s file=%s mro=%s",
            id(sample),
            sample.__module__,
            getattr(sys.modules.get(sample.__module__), "__file__", "?"),
            [c.__name__ for c in sample.__mro__],
        )
        self.logger.info(
            "Job's    Change: id=%s module=%s file=%s mro=%s",
            id(job_view),
            job_view.__module__,
            getattr(sys.modules.get(job_view.__module__), "__file__", "?"),
            [c.__name__ for c in job_view.__mro__],
        )

        if sample is job_view:
            self.logger.info("Class identity MATCHES between adapter result and job-level Change.")
        else:
            self.logger.error(
                "Class identity DIFFERS: adapter Change id=%s vs job Change id=%s.", id(sample), id(job_view)
            )
