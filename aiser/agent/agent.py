from abc import ABC, abstractmethod
import typing

from ..identifiable_entities import IdentifiableEntity
from ..models import ChatMessage


class Agent(IdentifiableEntity, ABC):
    def __init__(self, agent_id: str):
        super().__init__(entity_id=agent_id)

    @abstractmethod
    def reply(self, messages: typing.List[ChatMessage]) -> typing.AsyncGenerator[ChatMessage, None]:
        raise NotImplementedError
