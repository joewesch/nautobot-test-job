from .dataclasses import Change, Result


class ServiceA:
    def __init__(self, adapter, logger):
        self.adapter = adapter
        self.logger = logger

    def sync(self):
        records = self.adapter.fetch()
        changes = [Change(**self.adapter.transform(record)) for record in records]
        result = Result(changes=changes)

        unfiltered = result.count()
        filtered = result.count(data_type=Change)

        self.logger.info(
            "Service sync for adapter %s: unfiltered=%d filtered(data_type=Change)=%d",
            self.adapter.name,
            unfiltered,
            filtered,
        )
        for action in ("create", "update", "delete"):
            self.logger.info(
                "  count(action=%s)=%d count(action=%s, data_type=Change)=%d",
                action,
                result.count(action=action),
                action,
                result.count(action=action, data_type=Change),
            )

        if filtered != unfiltered:
            self.logger.error("BUG REPRODUCED: isinstance() check dropped %d change(s).", unfiltered - filtered)
        else:
            self.logger.info("All good: isinstance() check held inside ServiceA.sync().")

        return result
