from abc import ABC, abstractmethod
import time


class SimpleTimer(ABC):
    @abstractmethod
    def get_time_in_seconds(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def sleep(self, seconds: float):
        pass


class RealTimeTimer(SimpleTimer):
    def sleep(self, seconds: float):
        time.sleep(seconds)

    def get_time_in_seconds(self) -> float:
        return time.time()
