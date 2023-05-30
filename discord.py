import requests
from datetime import datetime


class Discord:
    def __init__(self, authToken, channelID):
        self.channelID = channelID
        self.authHeader = {"Authorization" : authToken}
        
    def readMessages(self):
        json = requests.get(f"https://discord.com/api/v9/channels/{self.channelID}/messages?limit=15", headers=self.authHeader).json()
        
        messages = []
        
        for message in json:
            if(not message["content"]):
                continue
            time = (datetime.fromisoformat(message["timestamp"])).strftime("%d %m %Y %X")
            
            item = message["author"]["username"] + " : '" + message["content"] + "' : " + time
            messages.append(item)

        messages.reverse()
        print(f"Response of retrieving message: {messages}")
        return messages

    def sendMessage(self, text):
        data = {"content" : text}
        json  = requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", data=data, headers=self.authHeader)
        print(f"Response of sending message: {json.content}")
        
    def uploadImage(self, imagePath):
        file = open(imagePath, "rb")
        
        json = requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", files={"file" : file}, headers=self.authHeader)
        
        print(f"Response of uploading image: {json.content}")
        
    
