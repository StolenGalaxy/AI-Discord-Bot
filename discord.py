import requests
from datetime import datetime
from random import choice, randint
import string

class Discord:
    def __init__(self, authToken, channelID):
        self.channelID = channelID
        self.rSession = requests.Session()
        self.rSession.headers = {"Authorization" : authToken}
            
    def readMessages(self, limit):
        json = self.rSession.get(f"https://discord.com/api/v9/channels/{self.channelID}/messages?limit={limit}").json()
        
        messages = []
        i = 0
        recentAuthor = ""
        
        
        for message in json:
            if(not message["content"]):
                continue
            time = (datetime.fromisoformat(message["timestamp"])).strftime("%d %m %Y %X")
            
            item = message["author"]["username"] + " : " + message["author"]["id"] + " : " + message["content"] + " : " + message["id"] + " : " + time
            messages.append(item)
            
            #So the author of the most recent message can be stored
            if not i:
                recentAuthor = message["author"]["username"]
                i+=1

        messages.reverse()
        #print(f"Response of retrieving message: {messages}")
        print("Retrieved recent messages successfully.")

        return[messages, recentAuthor]

    def sendMessage(self, text):
        data = {"content" : text}
        json  = self.rSession.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", data=data)
        print(f"Response of sending message: {json.content}")
    
    def uploadImage(self, imagePath, message):
        file = open(imagePath, "rb")
        data = {"content" : message}
        
        json = self.rSession.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", files={"file" : file}, data = data)
        
        print(f"Response of uploading image: {json.content}")
        
    def replyMessage(self, messageID, text):
        data = {"content": text, "message_reference" : {
            "message_id": messageID
        }}
        json = self.rSession.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", json=data)
        print(f"Response of replying to message: {json.content}")
    
    
    def findGif(self, search):
        #Search for gif
        json = self.rSession.get(f"https://discord.com/api/v9/gifs/search?q={search}&media_format=mp4&provider=tenor").json()
        
        gifs = []
        for gif in json:
            gifs.append(gif["url"])
            
        return choice(gifs)

    def reactToMessage(self, messageID, emojiURLEncode):
        self.rSession.put(f"https://discord.com/api/v9/channels/{self.channelID}/messages/{messageID}/reactions/{emojiURLEncode}/@me")
        
    def showTyping(self):
        self.rSession.post(f"https://discord.com/api/v9/channels/{self.channelID}/typing")
        
    def getOwnInfo(self):
        json = self.rSession.get("https://discord.com/api/v9/users/@me").json()
        return json
    
    def getChatInfo(self):
        json = self.rSession.get(f"https://discord.com/api/v9/channels/{self.channelID}").json()
        return json
