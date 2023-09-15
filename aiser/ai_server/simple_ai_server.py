import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from .ai_server import AiServer
from ..models.dtos import SemanticSearchRequest, AgentChatRequest
from ..models import ChatMessage


class SimpleAiServer(AiServer):
    def _get_app(self) -> FastAPI:
        app = FastAPI()

        @app.get("/version")
        async def version() -> str:
            return "0.1.0"

        @app.post("/knowledge-base/{kb_id}/semantic-search")
        async def knowledge_base(kb_id: str, request: SemanticSearchRequest):
            for kb in self._knowledge_bases:
                if kb.id == kb_id:
                    return kb.perform_semantic_search(
                        query_text=request.text,
                        desired_number_of_results=request.num_results
                    )
            raise HTTPException(status_code=404, detail="Knowledge base not found")

        @app.post("/agent/{agent_id}/chat")
        async def agent_chat(agent_id: str, request: AgentChatRequest):
            for agent in self._agents:
                if agent.id == agent_id:
                    return StreamingResponse(
                        agent.reply(input_message=ChatMessage(text_content=request.input_message.text_content)),
                        media_type="text/event-stream"
                    )
            raise HTTPException(status_code=404, detail="Agent not found")

        return app

    def run(self):
        uvicorn.run(app=self._get_app(), port=self._port)
