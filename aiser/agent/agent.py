from abc import ABC, abstractmethod
import typing
from ..models import ChatMessage


class Agent(ABC):
    def __init__(self, agent_id: str):
        super().__init__()
        self.id = agent_id

    @abstractmethod
    def reply(self, messages: typing.List[ChatMessage]) -> typing.AsyncGenerator[ChatMessage, None]:
        raise NotImplementedError
