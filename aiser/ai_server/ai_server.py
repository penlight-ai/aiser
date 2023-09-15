from abc import ABC, abstractmethod
from typing import List, Optional
from ..knowledge_base import KnowledgeBase
from ..agent import Agent


class AiServer(ABC):
    _knowledge_bases: List[KnowledgeBase]
    _agents: List[Agent]
    _port: int

    def __init__(
            self,
            knowledge_bases: Optional[List[KnowledgeBase]] = None,
            agents: Optional[List[Agent]] = None,
            port: int = 5000,
    ):
        super().__init__()
        self._port = port
        self._knowledge_bases = [] if knowledge_bases is None else knowledge_bases
        self._agents = [] if agents is None else agents

    @abstractmethod
    def run(self):
        raise NotImplementedError
