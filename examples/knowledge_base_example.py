from typing import List
from aiser import SimpleAiServer, KnowledgeBase, SemanticSearchResult


class KnowledgeBaseExample(KnowledgeBase):
    def perform_semantic_search(self, query_text: str, desired_number_of_results: int) -> List[SemanticSearchResult]:
        result_example = SemanticSearchResult(
            content="This is an example of a semantic search result",
            score=0.5,
        )
        return [result_example for _ in range(desired_number_of_results)]


if __name__ == '__main__':
    server = SimpleAiServer(
        knowledge_bases=[
            KnowledgeBaseExample(knowledge_base_id="kb_example"),
        ],
        port=5000
    )
    server.run()
