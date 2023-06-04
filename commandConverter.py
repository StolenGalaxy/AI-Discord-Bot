from bing import ask
from time import sleep

oddNumbers = [1, 3, 5, 7, 9]

def convert(command: str, discordSession):
    number = command.count("#=")
    
    commands = []
    
    for i in range(number):
        commands.append(command.split("#=")[oddNumbers[i]])
    
    for command in commands:
        if "SENDTEXT" in command:
            print("Sending text.")
            content = command.split("SENDTEXT")[1]
            discordSession.sendMessage(content)

        elif "SENDGIFMESSAGE" in command:
            print("Finding and sending gif.")
            content = command.split("SENDGIFMESSAGE")[1]
            gifSearch = content.split("@")[1]
            message = content.split("@")[2]
            
            gifURL = discordSession.findGif(gifSearch)
            discordSession.sendMessage(message)
            discordSession.sendMessage(gifURL)
            
        elif "REACT" in command:
            print("Reacting to message.")
            content = command.split("REACT")[1]
            
            messageID = content.split("@;")[1].strip()

            URLEmoji = content.split("@;")[2].strip()

            message = content.split("@;")[3]

            
            discordSession.reactToMessage(messageID, URLEmoji)
            sleep(3)
            discordSession.sendMessage(message)
            
        elif "REPLYTEXT" in command:
            print("Replying to message.")
            content = command.split("REPLYTEXT")[1]
            
            replyMessageID = content.split("@;")[1].strip()
            
            message = content.split("@;")[2].strip()
            
            discordSession.replyMessage(replyMessageID, message)
        
            
            
            
                