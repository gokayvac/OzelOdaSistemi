import os, asyncio, discord
from discord.ext import commands
from BotModules.Config import TOKEN, get_intents
from BotModules.VoiceManager import VoiceManager
from BotModules.EventHandlers import EventHandlers

os.makedirs("data", exist_ok=True)

async def main():
    bot = commands.Bot(command_prefix="porno", intents=get_intents())
    voice_manager = VoiceManager(bot)
    event_handlers = EventHandlers(bot, voice_manager)
    await event_handlers.setup_event_listeners()
    
    try:
        print("ancho.today")
        await bot.start(TOKEN)
    except Exception as ancho:
        print({ancho}) 
    finally:
        if not bot.is_closed(): await bot.close()

if __name__ == "__main__":
    asyncio.run(main())