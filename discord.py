import requests
from datetime import datetime
from random import choice, randint


class Discord:
    def __init__(self, authToken, channelID):
        self.channelID = channelID
        self.authHeader = {"Authorization" : authToken}
        
    def readMessages(self):
        json = requests.get(f"https://discord.com/api/v9/channels/{self.channelID}/messages?limit=30", headers=self.authHeader).json()
        
        messages = []
        i = 0
        recentAuthor = ""
        
        secretKey = str(randint(0, 9999))
        
        for message in json:
            if(not message["content"]):
                continue
            time = (datetime.fromisoformat(message["timestamp"])).strftime("%d %m %Y %X")
            
            item = message["author"]["username"] + " : " + message["author"]["id"] + message["content"] + " : " + time
            messages.append(item)
            
            #So the author of the most recent message can be stored
            if not i:
                recentAuthor = message["author"]["username"]
                i+=1

        messages.reverse()
        #print(f"Response of retrieving message: {messages}")
        print("Retrieved recent messages successfully.")

        return[messages, recentAuthor, secretKey]

    def sendMessage(self, text):
        data = {"content" : text}
        json  = requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", data=data, headers=self.authHeader)
        print(f"Response of sending message: {json.content}")
    
    def uploadImage(self, imagePath, message):
        file = open(imagePath, "rb")
        data = {"content" : message}
        
        json = requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", files={"file" : file}, data = data, headers=self.authHeader)
        
        print(f"Response of uploading image: {json.content}")
        
    def findGif(self, search):
        #Search for gif
        json = requests.get(f"https://discord.com/api/v9/gifs/search?q={search}&media_format=mp4&provider=tenor").json()
        
        gifs = []
        for gif in json:
            gifs.append(gif["url"])
            
        return choice(gifs)

    def showTyping(self):
        requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/typing", headers=self.authHeader)