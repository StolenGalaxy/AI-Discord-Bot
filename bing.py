from EdgeGPT.EdgeUtils import Query, Cookie 
from uuid import uuid4

async def ask(prompt):
    bot = await Chatbot.create() # Passing cookies is optional
    response = (await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative))
    response = str(response["item"]["result"]["message"])
    await bot.close()
    return response