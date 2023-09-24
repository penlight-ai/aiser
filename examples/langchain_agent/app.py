from typing import List, Any
import typing
from aiser import RestAiServer, Agent
from aiser.models import ChatMessage
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os
import asyncio


class CustomCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self._tokens: List[str] = []
        self._has_finished: bool = False

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self._tokens.append(token)

    def on_llm_end(self, response, **kwargs: Any) -> None:
        self._has_finished = True

    async def get_generated_tokens(self) -> typing.AsyncGenerator[List[str], None]:
        while (not self._has_finished) or (len(self._tokens) > 0):
            if len(self._tokens) > 0:
                yield self._tokens
                self._tokens = []
            await asyncio.sleep(0.05)


class AgentExample(Agent):
    def __init__(self, openai_api_key: str, model_name: str):
        super().__init__()
        self._openai_api_key = openai_api_key
        self._model_name = model_name

    async def _execute_model(self, chat_model, combined_messages_as_str: str):
        await chat_model.apredict_messages(messages=[
            HumanMessage(content=combined_messages_as_str)
        ])

    async def reply(self, messages: typing.List[ChatMessage]) -> typing.AsyncGenerator[ChatMessage, None]:
        callback_handler = CustomCallbackHandler()
        ai_model = self._make_model(
            callback_handler=callback_handler
        )
        messages_combined_str = self._make_messages_combined_str(messages=messages)
        task = asyncio.create_task(self._execute_model(
            chat_model=ai_model,
            combined_messages_as_str=messages_combined_str
        ))

        async for tokens in callback_handler.get_generated_tokens():
            for token in tokens:
                yield ChatMessage(
                    text_content=token,
                )
        await task

    def _make_model(self, callback_handler: CustomCallbackHandler) -> ChatOpenAI:
        return ChatOpenAI(
            openai_api_key=self._openai_api_key,
            model=self._model_name,
            streaming=True,
            temperature=0,
            callbacks=[callback_handler],
            verbose=True
        )

    def _make_messages_combined_str(self, messages: typing.List[ChatMessage]) -> str:
        starting_message = ChatMessage(
            text_content='''
You are Opposite Agent. Whenever you receive a message from the user, you should reply with the opposite of that message.
Don't reply with anything other than the exact opposite of the user's message.
''',
        )
        messages_combined = [starting_message] + list(messages)
        messages_combined_str = self._messages_to_prompt_string(messages_combined)
        return messages_combined_str

    def _messages_to_prompt_string(self, messages: List[ChatMessage]) -> str:
        final_prompt = ""
        for i, message in enumerate(messages):
            final_prompt += f"message {i}: {message.text_content}\n"
        final_prompt += f"message {len(messages)}:"
        return final_prompt


if __name__ == '__main__':
    # Loading Environment Variables:
    # Duplicate the file sample.env and rename it to .env then fill in the values in the .env file.
    # Set the environment variable AISER_ENVIRONMENT to "Development" only for local development.
    # Otherwise, you can leave it empty or set it to "Production"
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    server = RestAiServer(
        complete_url="http://127.0.0.1:5000",
        agents=[
            AgentExample(
                openai_api_key=OPENAI_API_KEY,
                model_name='gpt-3.5-turbo'
            ),
        ],
        port=5000
    )
    server.run()
