from abc import ABC, abstractmethod
from typing import Generator
from ..models import ChatMessage


class Agent(ABC):
    def __init__(self, agent_id: str):
        super().__init__()
        self.id = agent_id

    @abstractmethod
    def reply(self, input_message: ChatMessage) -> Generator[str, None, None]:
        raise NotImplementedError
