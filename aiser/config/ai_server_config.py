from .ai_server_env_variables import get_ai_server_env_variables, AiServerEnvVariables
from ..ai_server_consumer import AiServerConsumer, get_default_consumer
import typing
from pydantic import BaseModel


class AiServerConfig(BaseModel):
    consumer: AiServerConsumer
    complete_url: str


def make_ai_server_config(
        complete_url: str,
        consumer: typing.Optional[AiServerConsumer] = None
) -> AiServerConfig:
    env_variables = get_ai_server_env_variables()

    final_consumer = _determine_consumer(consumer=consumer, env_variables=env_variables)

    return AiServerConfig(
        complete_url=complete_url,
        consumer=final_consumer
    )


def _determine_consumer(consumer: typing.Optional[AiServerConsumer], env_variables: AiServerEnvVariables):
    if consumer is not None:
        return consumer
    if env_variables.CONSUMER_PUBLIC_KEY_INFO_URL is not None:
        return AiServerConsumer(
            publicKeyInfoUrl=env_variables.CONSUMER_PUBLIC_KEY_INFO_URL
        )
    return get_default_consumer()
