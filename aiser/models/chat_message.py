from pydantic import BaseModel


class ChatMessage(BaseModel):
    text_content: str
