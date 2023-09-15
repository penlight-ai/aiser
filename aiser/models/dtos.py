from pydantic import BaseModel


class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int


class ChatMessageDto(BaseModel):
    text_content: str


class AgentChatRequest(BaseModel):
    input_message: ChatMessageDto
