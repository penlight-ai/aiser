from pydantic import BaseModel
from typing import List
import humps


class CamelCaseBaseModel(BaseModel):
    class Config:
        alias_generator = humps.camelize
        allow_population_by_field_name = True


class SemanticSearchRequest(CamelCaseBaseModel):
    text: str
    num_results: int


class SemanticSearchResultDto(CamelCaseBaseModel):
    content: str
    score: float


class SemanticSearchResultResponseDto(CamelCaseBaseModel):
    results: List[SemanticSearchResultDto]


class ChatMessageDto(CamelCaseBaseModel):
    text_content: str


class AgentChatRequest(CamelCaseBaseModel):
    input_message: ChatMessageDto
