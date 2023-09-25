import typing
from abc import ABC, abstractmethod
from typing import List

from ..identifiable_entities import IdentifiableEntity
from aiser.knowledge_base.semantic_search_result import SemanticSearchResult


class KnowledgeBase(IdentifiableEntity, ABC):
    def __init__(self, knowledge_base_id: str):
        super().__init__(entity_id=knowledge_base_id)

    @abstractmethod
    def perform_semantic_search(self, query_text: str, desired_number_of_results: int) -> List[SemanticSearchResult]:
        raise NotImplementedError
