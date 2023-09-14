import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from .ai_server import AiServer
import asyncio
from ..models.dtos import SemanticSearchRequest


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
                    return kb.perform_semantic_search(query_text=request.query, desired_number_of_results=request.top_k)
            raise HTTPException(status_code=404, detail="Knowledge base not found")

        async def stream_hello_world():
            message = 'hello world'
            for character in message:
                await asyncio.sleep(0.1)
                yield character

        @app.get("/agent/{agent_id}/chat")
        async def agent(agent_id: str):
            return StreamingResponse(stream_hello_world(), media_type="text/event-stream")

        return app

    def run(self):
        uvicorn.run(app=self._get_app(), port=self._port)
