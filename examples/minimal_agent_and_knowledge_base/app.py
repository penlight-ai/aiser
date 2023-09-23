from typing import List
import typing
from aiser import RestAiServer, KnowledgeBase, SemanticSearchResult, Agent
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
    async def reply(self, messages: typing.List[ChatMessage]) -> typing.AsyncGenerator[ChatMessage, None]:
        reply_message = "This is an example of a reply from an agent"
        for character in reply_message:
            yield ChatMessage(text_content=character)
            await asyncio.sleep(0.1)


if __name__ == '__main__':
    server = RestAiServer(
        complete_url="http://127.0.0.1:5000",
        agents=[
            AgentExample(),
        ],
        knowledge_bases=[
            KnowledgeBaseExample(),
        ],
        port=5000
    )
    server.run()
