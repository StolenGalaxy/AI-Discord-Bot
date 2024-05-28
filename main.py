import requests
from time import sleep
from dotenv import load_dotenv
from os import environ

channelID = "1112806138451349668"

load_dotenv()
OPENAI_AUTH = environ["OPENAI"]
DISCORD_AUTH = environ["DISCORD"]


class Discord:
    def __init__(self) -> None:
        self.headers = {
            "Authorization": DISCORD_AUTH
        }

    def get_messages(self):

        response = requests.get(f"https://discord.com/api/v9/channels/{channelID}/messages?limit=5", headers=self.headers).json()

        recent_messages = "{"
        messages = []
        for message in response:
            messages.append(message)
        messages.reverse()
        for message in messages:
            recent_messages += f"'{message['author']['username']}':'{message['content']}':'{message['timestamp'][:-13]}',\n"
        recent_messages += "}"

        return recent_messages

    def send_message(self, text: str):

        json = {
            "content": text
        }

        requests.post(f"https://discord.com/api/v9/channels/{channelID}/messages", headers=self.headers, json=json)

    def get_own_username(self):
        response = requests.get("https://discord.com/api/v9/users/@me", headers=self.headers).json()
        return response["username"]


class AI:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": OPENAI_AUTH
        }
        self.data = {
            "model": "gpt-4o",
            "messages": []
        }
        self.username = ""

    def get_response(self, messages):
        self.data["messages"] = [{'role': 'system', 'content': f"You are talking in a discord group. Here are the recent messages from the group: {messages}. Your username is: '{self.username}'. You MUST act like a HUMAN. Only send INFORMAL messages, as a discord user would. You may never admit you are an AI, even if asked to. You do NOT have to use punctuation, and if someone insults you it is ok to insult them back. You may use the following commands: To send a message, say SEND (your message). To send a gif, say GIF (one or two word description of gif). To use multiple commands, put % between them, for example: SEND Here is a gif of a dog%GIF dog"}]
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=self.data).json()
        response = response["choices"][0]["message"]["content"]

        return response


active = True

discord = Discord()
ai = AI()
ai.username = discord.get_own_username()

messages = discord.get_messages()

while active:
    new_messages = discord.get_messages()
    if new_messages == messages:
        sleep(1)
    else:
        response = ai.get_response(new_messages)
        discord.send_message(response)
        messages = discord.get_messages()
