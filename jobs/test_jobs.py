import json
import time
from random import randint

from nautobot.apps.jobs import Job, JobHookReceiver, register_jobs

name = "Test Jobs"


DIFF_FORMAT = """
<details>\n
    <summary>{subject}</summary>\n
\n
```\n
{diff}
```\n
\n
</details>\n
"""


class RandomSleep(Job):
    class Meta:
        name = "Randomly sleep and end."
        description = "Randomly sleep an amount of seconds between 1 and 10 and then complete/"
        has_sensitive_variables = False

    def run(self):
        rand_int = randint(1, 10)
        self.logger.info(f"Sleeping {rand_int} seconds...")
        time.sleep(rand_int)
        self.logger.info("Done")


register_jobs(RandomSleep)


class JobHookReporter(JobHookReceiver):
    """Logs all details about the changed object and ends."""

    def receive_job_hook(self, change, action, changed_object):
        self.logger.info(f"ObjectChange: {change}", extra={"object": changed_object})

        snapshots = change.get_snapshots()
        diff_text = DIFF_FORMAT.format(
            subject="DIFF (Expand)",
            diff=json.dumps(
                snapshots["differences"],
                indent=4,
            ),
        )
        self.logger.info(diff_text)

        self.logger.info(f"Action: {action}")

        if changed_object:
            # Changed object is None when the object is deleted.
            self.logger.info(f"Changed object: {changed_object}", extra={"object": changed_object})


register_jobs(JobHookReporter)
