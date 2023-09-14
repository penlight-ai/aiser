from pydantic import BaseModel


class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int
