from openai import OpenAI

from dotenv import load_dotenv
from os import environ

from pydantic import BaseModel

import requests

import json

from time import sleep
from random import randint

load_dotenv()

DISCORD_AUTH = environ["DISCORD"]

DISCORD_CHANNEL_ID = environ["DISCORD_CHANNEL_ID"]

SYSTEM_PROMPT = """

You will be shown messages from a Discord group/server.

You must respond to these messages as if you are a human.

Your responses should be informal and short, generally lacking punctuation.

When responding, use the following format:
action 1:
    response_type:
        0 - Send a message
        1 - Reply to a message
        2 - React to a message with an emoji
        3 - Send a gif
    target_message:
        The ID of the message you wish to target
        Used if replying or reacting to a message, leave blank otherwise
    content:
        If sending or replying to a message - Set the content of the message here
        If sending a gif - Put a short, one word description of the gif here
        If reacting to a message with an emoji - Put the url encoded form of the emoji here
action 2:
    response_type:
        ... and so on; you can and SHOULD use as many actions as you wish to respond over multiple messages or send messages and gifs and reactions etc

Your username is: {}
The messages, provided below are in the format TIMESTAMP:USERNAME:MESSAGE_ID:```CONTENT``` (or if the message is a sticker, it will be in the format TIMESTAMP:USERNAME:MESSAGE_ID:THIS MESSAGE IS A STICKER:STICKER DESCRIPTION)

MESSAGES:

"""

headers = {
    'Authorization': DISCORD_AUTH
}


class Action(BaseModel):
    response_type: int
    target_message: str
    content: str


class Response(BaseModel):
    actions: list[Action]


class Client(OpenAI):
    def __init__(self):
        super().__init__()

    def get_prompt(self, messages: list):
        messages.reverse()
        prompt = f"{SYSTEM_PROMPT}{messages}"
        prompt = prompt.format(self.get_self_info())
        print(prompt)

        return prompt

    def get_response(self, messages):
        completion = self.chat.completions.parse(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": self.get_prompt(messages)
                }
            ],
            response_format=Response
        )

        response = completion.choices[0].message.content

        return response

    def send_message(self, message):

        json_data = {
            "content": message
        }

        return requests.post(f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages", headers=headers, json=json_data)

    def reply_to_message(self, message, target_id):

        json_data = {
            "content": message,
            "message_reference": {
                "message_id": target_id
            }
        }

        return requests.post(f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages", headers=headers, json=json_data)

    def react_to_message(self, emoji_code, target_id):

        return requests.put(f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages/{target_id}/reactions/{emoji_code}/%40me", headers=headers).text

    def get_messages(self, limit: int = 15):

        params = {
            "limit": limit
        }

        response = requests.get(f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages", headers=headers, params=params)

        if response.status_code == 200:
            messages = response.json()

            messages_formatted = []

            for message in messages:
                content = str(message["content"])
                sanitized_content = content.replace("```", "'''")

                message_to_append = f"{message["timestamp"]}:{message["author"]["username"]}:{message["id"]}:```{sanitized_content}```"
                messages_formatted.append(message_to_append)

                if "sticker_items" in str(message) and "sticker_items" not in sanitized_content:
                    sticker_desc = message["sticker_items"][0]["name"]
                    message_to_append = f"{message["timestamp"]}:{message["author"]["username"]}:{message["id"]}:THIS MESSAGE IS A STICKER:{sticker_desc}"
                    messages_formatted.append(message_to_append)

            return messages_formatted
        else:
            print(response.text)
            return False

    def interpret_response(self, response):
        response = json.loads(response)
        print(response)
        for action in response["actions"]:
            response_type = action["response_type"]
            target_message_id = action["target_message"]
            content = action["content"]

            if not response_type:
                self.send_message(content)
            if response_type == 1:
                self.reply_to_message(content, target_message_id)
            if response_type == 2:
                print(self.react_to_message(content, target_message_id))

            sleep(randint(1, 5))

    def get_self_info(self):
        username = requests.get("https://discord.com/api/v9/users/@me", headers=headers).json()["username"]
        return username


def run():
    client = Client()

    messages = client.get_messages()

    response = client.get_response(messages)

    client.interpret_response(response)


if __name__ == "__main__":
    run()