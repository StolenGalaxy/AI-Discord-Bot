from EdgeGPT import Chatbot, ConversationStyle


async def ask(prompt):
    bot = await Chatbot.create()
    response = (await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative))
    response = str(response["item"]["result"]["message"])
    await bot.close()
    return response
