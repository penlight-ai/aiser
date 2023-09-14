import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .ai_server import AiServer
import asyncio

app = FastAPI()


@app.get("/knowledge-base/{kb_id}")
async def knowledge_base(kb_id: str):
    return {"message": "Hello World"}


async def stream_hello_world():
    message = 'hello world'
    for character in message:
        await asyncio.sleep(0.1)
        yield character


@app.get("/agent/{agent_id}/chat")
async def agent(agent_id: str):
    return StreamingResponse(stream_hello_world(), media_type="text/event-stream")


class SimpleAiServer(AiServer):
    def run(self):
        uvicorn.run(app=app, port=self._port)
