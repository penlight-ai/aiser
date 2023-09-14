from .ai_server import AiServer
import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/knowledge-base/{kb_id}")
async def root(kb_id: str):
    return {"message": "Hello World"}


class SimpleAiServer(AiServer):
    def run(self):
        uvicorn.run(app=app, port=self._port)
