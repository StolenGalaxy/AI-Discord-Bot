import requests
from datetime import datetime

data = {
    "content" : "hello again"
}
#res = requests.post("https://discord.com/api/v9/channels/1112721985697480765/messages", headers=headers, json=data)

class Discord:
    def __init__(self, authToken, channelID):
        self.channelID = channelID
        self.authHeader = {"Authorization" : authToken}
        
    def readMessages(self):
        json = requests.get(f"https://discord.com/api/v9/channels/{self.channelID}/messages?limit=100", headers=self.authHeader).json()
        
        messages = []
        
        for message in json:
            if(not message["content"]):
                continue
            time = (datetime.fromisoformat(message["timestamp"])).strftime("%d %m %Y %X")
            
            item = message["author"]["username"] + " : '" + message["content"] + "' : " + time
            messages.append(item)

        messages.reverse()
        print(f"Response of retrieving message: {messages}")

    def sendMessage(self, text):
        data = {"content" : text}
        json  = requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", data=data, headers=self.authHeader)
        print(f"Response of sending message: {json.content}")
        
    def uploadImage(self, imagePath):
        file = open(imagePath, "rb")
        
        json = requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", files={"file" : file}, headers=self.authHeader)
        
        print(f"Response of uploading image: {json.content}")
        
        
discord = Discord("NjEyNjM4ODE3MzgzMzUwMjcy.GMP9-V.Dy0RKiBhQkHFGN1OIzkJhjuOXjOiTTXkbH52c0", "1112806138451349668").uploadImage("E:\Downloads\pickaxe.png")
