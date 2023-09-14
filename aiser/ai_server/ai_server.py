from abc import ABC, abstractmethod


class AiServer(ABC):
    def __init__(self, port: int):
        super().__init__()
        self._port = port

    @abstractmethod
    def run(self):
        raise NotImplementedError
