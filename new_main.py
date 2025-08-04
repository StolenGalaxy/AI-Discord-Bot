from openai import OpenAI

from dotenv import load_dotenv
from os import environ

from pydantic import BaseModel

load_dotenv()

DISCORD_AUTH = environ["DISCORD"]

SYSTEM_PROMPT = """

You will be shown messages from a Discord group/server.

You must respond to these messages as if you are a human.

Your responses should be informal and short unless told otherwise.

"""


class ResponseFormat(BaseModel):
    messages_to_send: list[str]


class Client(OpenAI):
    def __init__(self):
        super().__init__()

    def get_prompt(self):
        prompt = SYSTEM_PROMPT

        return prompt

    def get_response(self):
        completion = self.chat.completions.parse(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": self.get_prompt()
                }
            ],
            response_format=ResponseFormat,
        )

        response = completion.choices[0].message.content

        return response


my_client = Client()

response = my_client.get_response()
print(response)
