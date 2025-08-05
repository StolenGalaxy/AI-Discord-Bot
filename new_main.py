from openai import OpenAI

from dotenv import load_dotenv
from os import environ

from pydantic import BaseModel

import requests

load_dotenv()

DISCORD_AUTH = environ["DISCORD"]

DISCORD_CHANNEL_ID = environ["DISCORD_CHANNEL_ID"]

SYSTEM_PROMPT = """

You will be shown messages from a Discord group/server.

You must respond to these messages as if you are a human.

Your responses should be informal and short unless told otherwise.

When responding, set the corresponding values as such:
    response_type:
        0 - Send a message
        1 - Reply to a message
        2 - React to a message with an emoji
        3 - Send a gif
    target_message:
        The ID of the message you wish to target
        Used if replying or reacting to a message, leave blank
    content:
        If sending or replying to a message - Set the content of the message here
        If sending a gif - Put a short, one word description of the gif here
        If reacting to a message with an emoji - Set the ID of the emoji here

The messages, provided below are in the format TIMESTAMP:USERNAME:MESSAGE_ID:CONTENT

MESSAGES:

"""

headers = {
    'Authorization': DISCORD_AUTH
}


class ResponseFormat(BaseModel):
    response_type: int
    target_message: str
    content: str


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

    def send_message(self, message):

        json_data = {
            'content': message
        }

        return requests.post(f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages", headers=headers, json=json_data)

    def get_messages(self, limit: int = 50):

        params = {
            "limit": limit
        }

        response = requests.get(f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages", headers=headers, params=params)
        return response


my_client = Client()

print(my_client.get_messages(1).json())
