from .ai_server_consumer import AiServerConsumer


class PredefinedConsumers:
    penlight_ai = AiServerConsumer(
        publicKeyInfoUrl="https://api.penlight.ai/public-key"
    )


def get_default_consumer() -> AiServerConsumer:
    return PredefinedConsumers.penlight_ai
