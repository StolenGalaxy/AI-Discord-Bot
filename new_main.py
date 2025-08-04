from openai import OpenAI

from dotenv import load_dotenv
from os import environ

load_dotenv()

OPENAI_AUTH = environ["OPENAI"]
DISCORD_AUTH = environ["DISCORD"]

SYSTEM_PROMPT = """


"""


class client(OpenAI):
    def __init__(self, *, api_key=OPENAI_AUTH):
        super().__init__(api_key=api_key)

    def get_prompt(self):
        prompt = SYSTEM_PROMPT

        return prompt

    def get_response(self):
        completion = self.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": self.get_prompt()
                }
            ]
        )

        response = completion.choices[0].message.content

        return response
