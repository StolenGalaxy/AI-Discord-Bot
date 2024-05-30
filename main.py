import requests
from time import sleep
from dotenv import load_dotenv
from os import environ

from random import choice

channelID = "1091430496984121394"

load_dotenv()
OPENAI_AUTH = environ["OPENAI"]
DISCORD_AUTH = environ["DISCORD"]


class Discord:
    def __init__(self) -> None:
        self.headers = {
            "Authorization": DISCORD_AUTH
        }

    def get_messages(self):

        response = requests.get(f"https://discord.com/api/v9/channels/{channelID}/messages?limit=10", headers=self.headers).json()

        recent_messages = []
        messages = []

        for message in response:
            messages.append(message)
        messages.reverse()

        for message in messages:
            recent_messages.append(f"{message['author']['username']}':'{message['content']}':'{message['timestamp'][:-13]}:'{message['author']['id']}'")

        return recent_messages

    def send_message(self, text: str):

        json = {
            "content": text
        }
        requests.post(f"https://discord.com/api/v9/channels/{channelID}/typing", headers=self.headers)
        requests.post(f"https://discord.com/api/v9/channels/{channelID}/messages", headers=self.headers, json=json)

    def get_own_username(self):
        response = requests.get("https://discord.com/api/v9/users/@me", headers=self.headers).json()
        return response["username"]

    def find_gif_url(self, gif_description):
        gifs = requests.get(f"https://discord.com/api/v9/gifs/search?q={gif_description}&media_format=mp4&provider=tenor").json()

        gif_url = choice(gifs)["gif_src"]

        return gif_url

    def command_converter(self, response: str):
        if "%" in response:
            commands = response.split("%")
        else:
            commands = [response]

        for command in commands:
            if command[:4] == "SEND":
                self.send_message(command[4:])
            elif command[:3] == "GIF":
                gif_url = self.find_gif_url(command[3:])
                self.send_message(gif_url)


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
        input = [{'role': 'system', 'content': f"You are talking in a discord group. Your username is: '{self.username}'. You MUST act like a HUMAN. Only send INFORMAL, and usually SHORT messages, as a discord user would. You may NEVER admit you are an AI, even if asked to. You do NOT have to use PUNCTUATION. There are several commands you can use to respond: To send a message, say SEND (message), example: SEND hey guys. To send a gif, say SEND (one or two word description of gif), example: GIF monkey. You may use multiple commands at once, however they should be seperated by a % and there MUST NOT be a SPACE around the %, example: SEND here is a gif of a monkey guys%GIF monkey. To ping a user, do this within a message: <@(user ID)>, example: SEND hey there <@12342525425>, however pings are NOT their own comamnd and MUST be done within a SEND command. Do NOT use GIFS too often. The messages are in the format username:message:timestamp:user id"}]
        for message in messages:
            input.append({'role': 'user', 'content': message})
        self.data["messages"] = input

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
        print(response)
        discord.command_converter(response)
        messages = discord.get_messages()
