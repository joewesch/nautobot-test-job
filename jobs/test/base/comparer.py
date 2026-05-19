from .dataclasses import Change, Result


class Comparator:
    def __init__(self, logger):
        self.logger = logger

    def change_class_id(self):
        return id(Change)

    def compare(self, changes):
        result = Result(changes=changes)

        if changes:
            sample = type(changes[0])
            self.logger.info(
                "Comparator received from adapter: type=%s id(type)=%s id(Change imported here)=%s module=%s",
                sample.__name__,
                id(sample),
                id(Change),
                Change.__module__,
            )

        unfiltered = result.count()
        filtered = result.count(data_type=Change)
        self.logger.info(
            "Comparator counts: unfiltered=%d filtered(data_type=Change)=%d", unfiltered, filtered
        )
        if filtered != unfiltered:
            self.logger.error(
                "BUG REPRODUCED: isinstance() dropped %d change(s) inside Comparator.compare().",
                unfiltered - filtered,
            )
        else:
            self.logger.info("Comparator: isinstance() check held.")

        return result
