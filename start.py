from main import Main
from discord import Discord

authToken = "NjEyNjM4ODE3MzgzMzUwMjcy.G9hEP8.WYXSO2Gt2xulGhn-tYo3S6gxvGhxlx5a8wurPA"
channelID = "1114346991556771911"

discordSession = Discord(authToken, channelID)

Main(discordSession)
