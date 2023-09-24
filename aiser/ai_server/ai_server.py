from abc import ABC, abstractmethod
from typing import List, Optional

from ..identifiable_entities import IdentifiableGroupValidator
from ..knowledge_base import KnowledgeBase
from ..agent import Agent
from ..config import AiServerConfig, make_ai_server_config


class AiServer(ABC):
    _knowledge_bases: List[KnowledgeBase]
    _agents: List[Agent]
    _port: int

    def __init__(
            self,
            complete_url: str,
            knowledge_bases: Optional[List[KnowledgeBase]] = None,
            agents: Optional[List[Agent]] = None,
            port: int = 5000,
            host: str = "127.0.0.1",
            config: Optional[AiServerConfig] = None
    ):
        super().__init__()
        self._port = port
        self._host = host
        self._knowledge_bases = [] if knowledge_bases is None else knowledge_bases
        self._agents = [] if agents is None else agents
        self._config: AiServerConfig = config or make_ai_server_config(
            complete_url=complete_url
        )
        IdentifiableGroupValidator.assert_group_is_valid(self._knowledge_bases, group_name='Knowledge bases')
        IdentifiableGroupValidator.assert_group_is_valid(self._agents, group_name='Agents')

    @abstractmethod
    def run(self):
        raise NotImplementedError
