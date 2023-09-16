from pydantic import BaseModel
from typing import List


class SemanticSearchRequest(BaseModel):
    text: str
    numResults: int


class SemanticSearchResultDto(BaseModel):
    content: str
    score: float


class SemanticSearchResultResponseDto(BaseModel):
    results: List[SemanticSearchResultDto]


class ChatMessageDto(BaseModel):
    textContent: str


class AgentChatRequest(BaseModel):
    messages: List[ChatMessageDto]


class AgentChatResponse(BaseModel):
    outputMessage: ChatMessageDto
