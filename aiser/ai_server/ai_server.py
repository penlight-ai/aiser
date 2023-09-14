from abc import ABC, abstractmethod
from typing import List
from ..knowledge_base import KnowledgeBase


class AiServer(ABC):
    def __init__(self, knowledge_bases: List[KnowledgeBase], port: int):
        super().__init__()
        self._knowledge_bases = knowledge_bases
        self._port = port

    @abstractmethod
    def run(self):
        raise NotImplementedError
