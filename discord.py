import requests
from datetime import datetime
from random import choice, randint
import string

class Discord:
    def __init__(self, authToken, channelID):
        self.channelID = channelID
        self.authHeader = {"Authorization" : authToken}
        
        
    def generateKey(self):
        key = ""
        for i in range(5):
            key = key + choice(string.ascii_letters)
        return key
            
    def readMessages(self, limit):
        json = requests.get(f"https://discord.com/api/v9/channels/{self.channelID}/messages?limit={limit}", headers=self.authHeader).json()
        
        messages = []
        i = 0
        recentAuthor = ""
        
        secretKey = self.generateKey()
        
        for message in json:
            if(not message["content"]):
                continue
            time = (datetime.fromisoformat(message["timestamp"])).strftime("%d %m %Y %X")
            
            item = message["author"]["username"] + " : " + message["author"]["id"] + " : " + secretKey + message["content"] + secretKey + " : " + message["id"] + " : " + time
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
        
    def replyMessage(self, messageID, text):
        data = {"content": text, "message_reference" : {
            "message_id": messageID
        }}
        json = requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/messages", json=data, headers=self.authHeader)
        print(f"Response of replying to message: {json.content}")
    
    
    def findGif(self, search):
        #Search for gif
        json = requests.get(f"https://discord.com/api/v9/gifs/search?q={search}&media_format=mp4&provider=tenor").json()
        
        gifs = []
        for gif in json:
            gifs.append(gif["url"])
            
        return choice(gifs)

    def reactToMessage(self, messageID, emojiURLEncode):
        requests.put(f"https://discord.com/api/v9/channels/{self.channelID}/messages/{messageID}/reactions/{emojiURLEncode}/@me", headers=self.authHeader)
        
    def showTyping(self):
        requests.post(f"https://discord.com/api/v9/channels/{self.channelID}/typing", headers=self.authHeader)
        
    def getOwnInfo(self):
        json = requests.get("https://discord.com/api/v9/users/@me", headers=self.authHeader).json()
        return json
    
    def getChatInfo(self):
        json = requests.get(f"https://discord.com/api/v9/channels/{self.channelID}", headers=self.authHeader).json()
        return json
