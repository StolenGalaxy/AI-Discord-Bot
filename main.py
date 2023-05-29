from discord import Discord
from bing import askBing

images = askBing("France", "image")

Discord("", "1112806138451349668").uploadImage(images[0])