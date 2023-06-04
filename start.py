from main import Main
from discord import Discord

authToken = ""
channelID = ""

discordSession = Discord(authToken, channelID)

Main(discordSession)