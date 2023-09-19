import os
import typing
from pydantic import BaseModel, AnyHttpUrl


class AiServerEnvVariables(BaseModel):
    CONSUMER_PUBLIC_KEY_INFO_URL: typing.Optional[AnyHttpUrl]
    AISER_ENVIRONMENT: typing.Optional[str]


def get_ai_server_env_variables() -> AiServerEnvVariables:
    return AiServerEnvVariables(
        CONSUMER_PUBLIC_KEY_INFO_URL=os.environ.get("CONSUMER_PUBLIC_KEY_INFO_URL"),
        AISER_ENVIRONMENT=os.environ.get("AISER_ENVIRONMENT")
    )
