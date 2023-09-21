![aiser banner](https://raw.githubusercontent.com/penlight-ai/aiser/b60ec4dcdd676a106df5fc1a0f5ead784a463986/media/banner.svg)

Aiser is an open source server of AI agents and knowledge bases. It uses [FastAPI](https://github.com/tiangolo/fastapi)
and [Pydantic](https://github.com/pydantic/pydantic) to create a unified REST API interface for these AI resources 
and it allows access only to authenticated consumers. 
For local development, You can disable authentication and you can explore the API
through a graphical user interface, resulting in a straightforward developer experience.

By Default, Aiser comes preconfigured with [Penlight AI]() as the default consumer that it authenticates against.
This is so that you can easily publish your AI agents and knowledge bases to the Penlight AI marketplace.
However, you can easily change this to another consumer or create you own.

## Installation

You can install Aiser using pip:
```bash
pip install aiser
```

## Getting Started

Please follow the [Quickstart Guide](https://docs.penlight.ai/docs/quick-start) to learn how to create an agent
and a knowledge base and test them out on your local machine.