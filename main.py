import requests
from time import sleep

channelID = "1112806138451349668"

DISCORD_AUTH = ""
OPENAI_AUTH  = ""


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
            "messages": [],
        }
        self.username = ""

    def get_response(self, messages):
        self.data["messages"] = [{'role': 'system', 'content': f'You are talking in a discord group. Here are the recent messages from the group: {messages}. Your username is: {self.username} You must respond with just the message you wish to send. You MUST act like a HUMAN. Only send INFORMAL messages, as a discord user would. You do NOT have to use punctuation.'}]
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=self.data).json()
        response = response["choices"][0]["message"]["content"]

        return response


active = True

discord = Discord()
ai = AI()
ai.username = discord.get_own_username()

messages = discord.get_messages()


while active:
    if discord.get_messages() == messages:
        sleep(1)
    else:
        new_messages = discord.get_messages()
        response = ai.get_response(new_messages)
        messages = new_messages
        discord.send_message(response)