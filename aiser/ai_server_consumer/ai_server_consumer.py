from pydantic import BaseModel, HttpUrl


class AiServerConsumer(BaseModel):
    publicKeyInfoUrl: HttpUrl
