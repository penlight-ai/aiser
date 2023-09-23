import typing
from aiser import RestAiServer, Agent
from aiser.models import ChatMessage
from aiser.env_tools import load_dotenv_if_available


class AgentExample(Agent):
    async def reply(self, messages: typing.List[ChatMessage]) -> typing.AsyncGenerator[ChatMessage, None]:
        yield 'a'


if __name__ == '__main__':
    load_dotenv_if_available()
    server = RestAiServer(
        complete_url="http://127.0.0.1:5000",
        agents=[
            AgentExample(),
        ],
        port=5000
    )
    server.run()
