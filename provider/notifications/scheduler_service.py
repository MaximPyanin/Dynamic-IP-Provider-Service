from typing import Callable, Any

from apscheduler.job import Job
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler


class SchedulerService:
    def __init__(self):
        self.scheduler = BlockingScheduler()

    def add_job(self, func: Callable[..., Any]) -> Job:
        return self.scheduler.add_job(
            func, CronTrigger(minute="0", hour="0", day="*", month="*", day_of_week="*")
        )

    def start(self) -> None:
        return self.scheduler.start()

    def stop(self) -> None:
        return self.scheduler.shutdown()
