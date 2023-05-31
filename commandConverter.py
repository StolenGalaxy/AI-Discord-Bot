from bing import askBing

oddNumbers = [1, 3, 5, 7, 9]

def convert(command: str, discordSession):
    number = command.count("#=")
    
    commands = []
    
    for i in range(number):
        commands.append(command.split("#=")[oddNumbers[i]])
    
    for command in commands:
        if "SENDTEXT" in command:
            print("sending text")
            content = (command.split("SENDTEXT")[1])
            discordSession.sendMessage(content)

        if "GENIMAGE" in command:
            print("Generating and sending image.")
            content = (command.split("GENIMAGE")[1])
            try:
                images = askBing(content, "image")
                discordSession.uploadAndGenerateImage(images[0])
            except:
                discordSession.sendMessgage("Sorry, I can't seem to create that image right now.")
            
                