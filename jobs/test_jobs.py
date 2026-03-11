import time
from random import randint

from nautobot.apps.jobs import Job, register_jobs

name = "Test Jobs"


class RandomSleep(Job):
    class Meta:
        name = "Randomly sleep and end."
        description = "Randomly sleep an amount of seconds between 1 and 10 and then complete/"

    def run(self):
        rand_int = randint(1, 10)
        self.logger.info(f"Sleeping {rand_int} seconds...")
        time.sleep(rand_int)
        self.logger.info("Done")


register_jobs(RandomSleep)
