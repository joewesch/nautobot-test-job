import time
from random import randint

from nautobot.apps.jobs import Job, register_jobs

name = "Test Jobs"


class RandomSleep(Job):
    class Meta:
        name = "Randomly sleep and end."
        description = "Randomly sleep an amount of seconds between 1 and 10 and then complete/"

    def run(self):
        time.sleep(randint(1, 10))
        self.logger.info("Done")


register_jobs(RandomSleep)
