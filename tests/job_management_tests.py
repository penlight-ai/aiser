import typing
import unittest
import asyncio
import time

from aiser.job_management import AsyncStartJobManager, AsyncStartJob
from aiser.job_management.timer import SimpleTimer


class MockJob(AsyncStartJob):
    def __init__(self):
        super().__init__()


class MockTimer(SimpleTimer):
    def __init__(self):
        super().__init__()
        self.time_in_seconds = 0.0
        self._actions_list: typing.List[typing.Tuple[float, typing.Callable]] = []

    def add_action(self, time_in_seconds: float, action: typing.Callable):
        self._actions_list.append((time_in_seconds, action))

    def sleep(self, seconds: float):
        self.time_in_seconds += seconds
        for time_in_seconds, action in self._actions_list:
            if time_in_seconds <= self.time_in_seconds:
                action()
                self._actions_list.remove((time_in_seconds, action))

    def _get_time_in_seconds(self) -> float:
        return self.time_in_seconds

    def get_time_in_seconds(self) -> float:
        return self.time_in_seconds


class AsyncStartJobManagerTestCase(unittest.TestCase):
    TIMEOUT_SECONDS: int = 2.0

    def setUp(self) -> None:
        self.timer = MockTimer()
        self.job_id = "test"

        self.manager: AsyncStartJobManager[MockJob] = AsyncStartJobManager(
            timer=self.timer, timeout_seconds=self.TIMEOUT_SECONDS
        )
        self.loop = asyncio.get_event_loop()

    def test_job_is_found_if_is_defined_then_waited_for(self):
        async def run_test():
            job = MockJob()
            self.manager.define_job(job_id=self.job_id, job=job)
            job_from_manager: typing.Optional[MockJob] = await self.manager.wait_for_job(job_id=self.job_id)
            self.assertTrue(job == job_from_manager)

        self.loop.run_until_complete(run_test())

    def test_is_not_found_if_not_defined(self):
        async def run_test():
            job_from_manager: typing.Optional[MockJob] = await self.manager.wait_for_job(job_id=self.job_id)
            self.assertTrue(job_from_manager is None)

        self.loop.run_until_complete(run_test())

    def create_job_at_seconds(self, seconds: float) -> MockJob:
        job = MockJob()
        self.timer.add_action(seconds, lambda: self.manager.define_job(job_id=self.job_id, job=job))
        return job

    def create_task_to_wait_for_job(self) -> asyncio.Task:
        return asyncio.create_task(self.manager.wait_for_job(job_id=self.job_id))

    def test_is_found_if_defined_within_timeout(self):
        async def run_test():
            manager_job_task = self.create_task_to_wait_for_job()
            job = self.create_job_at_seconds(self.TIMEOUT_SECONDS - 1.0)
            manager_job = await manager_job_task
            self.assertTrue(job == manager_job)

        self.loop.run_until_complete(run_test())

    def test_is_not_found_if_defined_after_timeout(self):
        async def run_test():
            manager_job_task = self.create_task_to_wait_for_job()
            _ = self.create_job_at_seconds(self.TIMEOUT_SECONDS + 1.0)
            job_from_manager = await manager_job_task
            self.assertIsNone(job_from_manager)

        self.loop.run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()
