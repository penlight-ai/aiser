import typing

from aiser.job_management.timer import RealTimeTimer, SimpleTimer


class AsyncStartJob:
    pass


AsyncStartJobT = typing.TypeVar(
    "AsyncStartJobT",
    bound=AsyncStartJob
)


class AsyncStartJobManager(typing.Generic[AsyncStartJobT]):
    """
    This class is intended to be used for endpoints that use server-sent-events where
    a POST request (job definition) and a GET request (job wait) will be sent at the same time.
    It should enable the GET request to wait (up to a timeout) for the POST request.
    """

    def __init__(self, timeout_seconds: float = 10.0, timer: SimpleTimer = RealTimeTimer()):
        super().__init__()
        self._jobs: typing.Dict[str, AsyncStartJobT] = {}
        self._timeout_seconds = timeout_seconds
        self._timer = timer

    def define_job(self, job_id: str, job: AsyncStartJobT):
        self._jobs[job_id] = job

    async def wait_for_job(self, job_id):
        start_time = self._timer.get_time_in_seconds()
        while self._timer.get_time_in_seconds() - start_time < self._timeout_seconds:
            if job_id in self._jobs:
                return self._jobs[job_id]
            self._timer.sleep(seconds=0.1)
