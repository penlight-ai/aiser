from typing import Optional

from pydantic import BaseModel


class SemanticSearchResult(BaseModel):
    """
    Represents one result of a semantic search operation.

    Attributes:
        content (str): The content of the result.
        score (float): The confidence score obtained during similarity search.
    """

    content: str
    score: Optional[float] = None
