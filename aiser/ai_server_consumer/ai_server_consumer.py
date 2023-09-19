from pydantic import BaseModel, AnyHttpUrl


class AiServerConsumer(BaseModel):
    publicKeyInfoUrl: AnyHttpUrl
