import discord
import asyncio
from BotModules.Config import VC_JOIN, KATEGORI
from BotModules.JsonManager import JsonManager
from BotModules.UI.Views import OzelOdaView, OzelOdaButtons

class VoiceManager:
    def __init__(self, bot):
        self.bot = bot
        self.ozel_odalar = {}
    
    def load_data(self):
        self.ozel_odalar = JsonManager.load_data()
        return self.ozel_odalar
    
    def save_data(self):
        return JsonManager.save_data(self.ozel_odalar)
    
    async def create_private_channel(self, member, guild):
        user_id_str = str(member.id)
        
        if user_id_str in self.ozel_odalar:
            existing_channel_id = int(self.ozel_odalar[user_id_str])
            existing_channel = self.bot.get_channel(existing_channel_id)
            
            if existing_channel:
                try:
                    await member.move_to(existing_channel)
                    await member.send(f"Zaten aktif bir özel odanız var: {existing_channel.name}")
                    return existing_channel
                except Exception as e: print(f"Kullanıcı taşınırken hata: {e}")
            else:
                del self.ozel_odalar[user_id_str]
                self.save_data()
        
        kategori = self.bot.get_channel(KATEGORI)
        if not kategori:
            try:
                await member.send("Özel oda kategorisi bulunamadı! Lütfen sunucu yetkililerine başvurun.")
                await member.move_to(None)
            except Exception as e: print(f"Kullanıcıya mesaj gönderirken hata: {e}")
            return None
        
        try:
            kanal_ismi = f"{member.display_name}'in Odası"
            yeni_kanal = await guild.create_voice_channel(
                name=kanal_ismi, category=kategori, bitrate=64000,
                user_limit=0, reason=f"{member}'in özel odası"
            )
            
            await yeni_kanal.set_permissions(
                member, manage_channels=True, move_members=True,
                mute_members=True, deafen_members=True, priority_speaker=True
            )
            
            self.ozel_odalar[user_id_str] = str(yeni_kanal.id)
            self.save_data()
            
            try:
                await asyncio.sleep(1)
                await member.move_to(yeni_kanal)
                return yeni_kanal
            except Exception as e:
                print(f"Kullanıcı ses kanalına taşınırken hata: {e}")
                return None
            
        except Exception as e:
            print(f"Özel oda oluşturulurken hata: {e}")
            try:
                await member.send(f"Özel oda oluşturulurken bir hata oluştu: {e}")
                await member.move_to(None)
            except: pass
            return None
    
    async def send_control_panel(self, member, channel):
        """Kullanıcıya özel oda kontrol paneli gönder"""
        embed = discord.Embed(
            title=f"🔊 Özel Oda Kontrol Paneli",
            description=f"Aşağıdaki menülerden özel ses odanızı özelleştirebilirsiniz.",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Kanal Adı", value=channel.name, inline=True)
        embed.add_field(name="Kullanıcı Limiti", value=f"{channel.user_limit if channel.user_limit else 'Sınırsız'}", inline=True)
        embed.add_field(name="Ses Kalitesi", value=f"{channel.bitrate//1000}kbps", inline=True)
        embed.add_field(
            name="📋 Kontrol Paneli Kullanımı",
            value="• Oda ayarlarını yapmak için aşağıdaki menüleri kullanın.\n• Düğmeler ile kanal adını, görünürlüğünü ve erişimini değiştirebilirsiniz.\n• Odanızı silmek için **Sil** düğmesini kullanabilirsiniz.",
            inline=False
        )
        embed.set_footer(text=f"{member.name}'in Özel Ses Odası")
        
        # Kontrol panelini mesaj olarak gönder
        view1 = OzelOdaView(member.id, channel.id, self.bot)
        view2 = OzelOdaButtons(member.id, channel.id, self.bot, self.ozel_odalar)
        
        try:
            dm_channel = await member.create_dm()
            await dm_channel.send(embed=embed, view=view1)
            await dm_channel.send("Oda Kontrol Düğmeleri:", view=view2)
        except Exception as e:
            print(f"DM gönderilemedi: {e}, kanala gönderiliyor")
            await channel.send(member.mention, embed=embed, view=view1)
            await channel.send("Oda Kontrol Düğmeleri:", view=view2)
    
    async def check_private_channel(self, member, before_channel, after_channel=None):
        """Kullanıcı kanaldan ayrıldığında özel oda kontrolü"""
        user_id_str = str(member.id)
        
        if user_id_str in self.ozel_odalar and str(before_channel.id) == self.ozel_odalar[user_id_str]:
            kanal = before_channel
            
            if len(kanal.members) == 0:
                await asyncio.sleep(15)
                
                kanal = self.bot.get_channel(int(self.ozel_odalar[user_id_str]))
                if kanal and len(kanal.members) == 0:
                    try:
                        await kanal.delete(reason="Özel oda boş kaldığı için silindi")
                        del self.ozel_odalar[user_id_str]
                        self.save_data()
                        print(f"{member.name}'in boş odası silindi")
                    except Exception as e: print(f"Boş oda silinirken hata: {e}")
    
    async def handle_voice_channel_join(self, member, channel):
        if channel.id == VC_JOIN:
            new_channel = await self.create_private_channel(member, channel.guild)
            if new_channel:
                await asyncio.sleep(2)
                await self.send_control_panel(member, new_channel)
    
    async def cleanup_empty_channels(self):
        temizlenecek_odalar = []
        for user_id, channel_id in self.ozel_odalar.items():
            channel = self.bot.get_channel(int(channel_id))
            if not channel: temizlenecek_odalar.append(user_id)
        
        for user_id in temizlenecek_odalar:
            del self.ozel_odalar[user_id]
        
        if temizlenecek_odalar:
            self.save_data()
            print(f"{len(temizlenecek_odalar)} adet eski özel oda kaydı temizlendi.")