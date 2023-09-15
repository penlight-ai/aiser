from typing import List, Generator
from aiser import SimpleAiServer, KnowledgeBase, SemanticSearchResult, Agent
from aiser.models import ChatMessage
import asyncio


class KnowledgeBaseExample(KnowledgeBase):
    def perform_semantic_search(self, query_text: str, desired_number_of_results: int) -> List[SemanticSearchResult]:
        result_example = SemanticSearchResult(
            content="This is an example of a semantic search result",
            score=0.5,
        )
        return [result_example for _ in range(desired_number_of_results)]


class AgentExample(Agent):
    async def reply(self, input_message: ChatMessage) -> Generator[str, None, None]:
        reply_message = "This is an example of a reply from an agent"
        for character in reply_message:
            yield character
            await asyncio.sleep(0.1)


if __name__ == '__main__':
    server = SimpleAiServer(
        agents=[
            AgentExample(agent_id="agent_example"),
        ],
        knowledge_bases=[
            KnowledgeBaseExample(knowledge_base_id="kb_example"),
        ],
        port=5000
    )
    server.run()