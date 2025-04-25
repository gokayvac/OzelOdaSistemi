import discord
from BotModules.Config import KANAL

class EventHandlers:
    def __init__(self, bot, voice_manager):
        self.bot = bot
        self.voice_manager = voice_manager
    
    async def setup_event_listeners(self):
        self.bot.event(self.on_ready)
        self.bot.event(self.on_voice_state_update)
    
    async def on_ready(self):
        print(f"{self.bot.user} olarak giriş yapıldı!")
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="özel odaları"))
        
        self.voice_manager.load_data()
        print("Özel oda verileri yüklendi!")
        
        ses_kanal = self.bot.get_channel(KANAL)
        if ses_kanal and isinstance(ses_kanal, discord.VoiceChannel):
            try: await ses_kanal.connect(); print(f"{ses_kanal.name} ses kanalına bağlanıldı!")
            except Exception as e: print(f"Ses kanalına bağlanırken hata oluştu: {e}")
        else: print(f"Ses kanalı bulunamadı! ID: {KANAL}")
        
        for guild in self.bot.guilds:
            print(f"{guild.name} sunucusu kontrol ediliyor...")
            await self.voice_manager.cleanup_empty_channels()
    
    async def on_voice_state_update(self, member, before, after):
        if after.channel: await self.voice_manager.handle_voice_channel_join(member, after.channel)
        if before.channel and (not after.channel or after.channel.id != before.channel.id):
            await self.voice_manager.check_private_channel(member, before.channel, after.channel)