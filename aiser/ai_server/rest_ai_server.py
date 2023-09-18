import time

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2
from .ai_server import AiServer
from ..ai_server_consumer import AiServerConsumer
from ..job_management import AsyncStartJobManager, AsyncStartJob
from ..models.dtos import SemanticSearchRequest, AgentChatRequest, SemanticSearchResultDto, \
    SemanticSearchResultResponseDto, AgentChatResponse, ChatMessageDto, PublicKeyInfo
from ..models import ChatMessage
import typing
import httpx
import jwt

from ..utils import base64_to_pem


class AgentChatJob(AsyncStartJob):
    def __init__(self, agent_chat_request: AgentChatRequest):
        super().__init__(creation_timestamp=time.time())
        self._agent_chat_request = agent_chat_request

    def get_agent_chat_request(self) -> AgentChatRequest:
        return self._agent_chat_request


class PublicKeyInfoClient:
    def __init__(self, consumer: AiServerConsumer):
        self._consumer = consumer

    async def fetch_public_key_info(self) -> PublicKeyInfo:
        async with httpx.AsyncClient() as client:
            url = str(self._consumer.publicKeyInfoUrl)
            response = await client.get(url)
            response.raise_for_status()
            public_key_info = PublicKeyInfo(**response.json())
            return public_key_info


class PublicKeyInfoGetter:
    def __init__(
            self,
            public_key_info_client: PublicKeyInfoClient,
            refresh_interval_in_seconds: float = 60,
    ):
        self._public_key_info_client = public_key_info_client
        self._public_key_info: typing.Optional[PublicKeyInfo] = None
        self._last_refresh_timestamp: float = 0
        self._refresh_interval_in_seconds = refresh_interval_in_seconds

    async def get_public_key_info(self) -> PublicKeyInfo:
        if (self._public_key_info is None
                or (time.time() - self._last_refresh_timestamp) > self._refresh_interval_in_seconds):
            self._public_key_info = await self._public_key_info_client.fetch_public_key_info()
            self._last_refresh_timestamp = time.time()
        return self._public_key_info


class RestAiServer(AiServer):
    def _get_app(self) -> FastAPI:
        app = FastAPI()
        public_key_info_client = PublicKeyInfoClient(consumer=self._config.consumer)
        public_key_info_getter = PublicKeyInfoGetter(public_key_info_client=public_key_info_client)

        auth_scheme = OAuth2()

        async def verify_token(token: str = Depends(auth_scheme)) -> None:
            try:
                token_without_prefix = token.split(" ")[1]
                public_key = (await public_key_info_getter.get_public_key_info()).publicKey
                public_key_pem = base64_to_pem(public_key)
                decoded_jwt = jwt.decode(jwt=token_without_prefix, key=public_key_pem, algorithms=["RS256"], options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "verify_aud": False,
                })
                if decoded_jwt['aud'] != self._config.complete_url:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            except jwt.exceptions.InvalidTokenError as error:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        @app.get("/version")
        async def version(token: str = Depends(verify_token)) -> str:
            return "0.1.0"

        @app.post("/knowledge-base/{kb_id}/semantic-search")
        async def knowledge_base(
                kb_id: str, request: SemanticSearchRequest,
                token: str = Depends(verify_token)
        ) -> SemanticSearchResultResponseDto:
            for kb in self._knowledge_bases:
                if kb.accepts_id(kb_id):
                    results = kb.perform_semantic_search(
                        query_text=request.text,
                        desired_number_of_results=request.numResults
                    )
                    result_dto = SemanticSearchResultResponseDto(results=[
                        SemanticSearchResultDto(content=result.content, score=result.score)
                        for result in results
                    ])
                    return result_dto
            raise HTTPException(status_code=404, detail="Knowledge base not found")

        async def convert_agent_message_gen_to_streaming_response(
                message_gen: typing.AsyncGenerator[ChatMessage, None]) -> typing.AsyncGenerator[str, None]:
            async for item in message_gen:
                message_dto = ChatMessageDto(textContent=item.text_content)
                yield AgentChatResponse(outputMessage=message_dto).model_dump_json(by_alias=True) + "\n"

        job_manager = AsyncStartJobManager()

        @app.post("/agent/{agent_id}/chat/{job_id}")
        async def agent_chat(
                agent_id: str,
                job_id: str, request: AgentChatRequest,
                token: str = Depends(verify_token)
        ):
            for agent in self._agents:
                if agent.accepts_id(agent_id):
                    new_job = AgentChatJob(agent_chat_request=request)
                    job_manager.define_job(job_id=job_id, job=new_job)
                    return
            raise HTTPException(status_code=404, detail="Agent not found")

        @app.get("/agent/{agent_id}/chat/{job_id}")
        async def agent_chat(
                agent_id: str,
                job_id: str,
                token: str = Depends(verify_token)
        ) -> StreamingResponse:
            for agent in self._agents:
                if agent.accepts_id(agent_id):
                    job = await job_manager.wait_for_job(job_id=job_id)
                    if job is None:
                        raise HTTPException(status_code=404, detail="Job not found")
                    request = job.get_agent_chat_request()
                    messages = [ChatMessage(text_content=messageDto.textContent) for messageDto in request.messages]
                    response_generator = agent.reply(messages=messages)
                    response_generator = convert_agent_message_gen_to_streaming_response(message_gen=response_generator)
                    return StreamingResponse(
                        response_generator,
                        media_type="text/event-stream"
                    )
            raise HTTPException(status_code=404, detail="Agent not found")

        return app

    def run(self):
        uvicorn.run(app=self._get_app(), port=self._port)
