from .comparer import Comparator
from .dataclasses import Change


class ServiceA:
    def __init__(self, adapter, logger):
        self.adapter = adapter
        self.logger = logger

    def change_class_id(self):
        return id(Change)

    def sync(self):
        records = self.adapter.fetch()
        changes = [self.adapter.transform(record) for record in records]

        if changes:
            sample = type(changes[0])
            self.logger.info(
                "ServiceA built changes: type=%s id(type)=%s id(Change imported in services)=%s",
                sample.__name__,
                id(sample),
                id(Change),
            )

        comparator = Comparator(self.logger)
        result = comparator.compare(changes)

        self.logger.info(
            "Change-id snapshot: adapter=%s services=%s comparator=%s",
            self.adapter.change_class_id(),
            self.change_class_id(),
            comparator.change_class_id(),
        )

        return result
