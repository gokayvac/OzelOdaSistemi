import discord
from discord.ui import View, Select, Button
from BotModules.Config import KULLANICI_LIMIT_SECENEK, BITRATE_SECENEK, REGION_SECENEK
from BotModules.UI.Modals import KanalIsimModal
from BotModules.JsonManager import JsonManager

class OzelOdaView(View):
    def __init__(self, user_id, channel_id, bot):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.channel_id = channel_id
        self.bot = bot
        self.add_item(self.create_limit_select())
        self.add_item(self.create_bitrate_select())
        self.add_item(self.create_region_select())

    def create_limit_select(self):
        select = Select(
            placeholder="Kullanıcı Limiti Ayarla",
            options=[discord.SelectOption(label=f"{limit} Kullanıcı", value=str(limit)) for limit in KULLANICI_LIMIT_SECENEK],
            custom_id="limit_select"
        )
        select.callback = self.limit_callback
        return select

    def create_bitrate_select(self):
        select = Select(
            placeholder="Ses Kalitesi Ayarla",
            options=[discord.SelectOption(label=f"{bitrate//1000}kbps", value=str(bitrate)) for bitrate in BITRATE_SECENEK],
            custom_id="bitrate_select"
        )
        select.callback = self.bitrate_callback
        return select

    def create_region_select(self):
        select = Select(
            placeholder="Bölge Ayarla",
            options=[discord.SelectOption(label=name, value=str(i)) for i, (name, _) in enumerate(REGION_SECENEK)],
            custom_id="region_select"
        )
        select.callback = self.region_callback
        return select

    async def limit_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return

        limit = int(interaction.data["values"][0])
        kanal = self.bot.get_channel(self.channel_id)
        if kanal:
            await kanal.edit(user_limit=limit)
            await interaction.response.send_message(f"Kullanıcı limiti {limit} olarak ayarlandı!", ephemeral=True)
        else:
            await interaction.response.send_message("Kanal bulunamadı!", ephemeral=True)

    async def bitrate_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return

        bitrate = int(interaction.data["values"][0])
        kanal = self.bot.get_channel(self.channel_id)
        if kanal:
            await kanal.edit(bitrate=bitrate)
            await interaction.response.send_message(f"Kanal ses kalitesi {bitrate//1000}kbps olarak ayarlandı!", ephemeral=True)
        else:
            await interaction.response.send_message("Kanal bulunamadı!", ephemeral=True)

    async def region_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return

        region_index = int(interaction.data["values"][0])
        region_name, region_value = REGION_SECENEK[region_index]
        
        kanal = self.bot.get_channel(self.channel_id)
        if kanal:
            await kanal.edit(rtc_region=region_value)
            await interaction.response.send_message(f"Kanal bölgesi {region_name} olarak ayarlandı!", ephemeral=True)
        else:
            await interaction.response.send_message("Kanal bulunamadı!", ephemeral=True)


class OzelOdaButtons(View):
    def __init__(self, user_id, channel_id, bot, ozel_odalar):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.channel_id = channel_id
        self.bot = bot
        self.ozel_odalar = ozel_odalar

    @discord.ui.button(label="İsim Değiştir", style=discord.ButtonStyle.primary, emoji="✏️", custom_id="isim_degistir")
    async def isim_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return
        await interaction.response.send_modal(KanalIsimModal(self.channel_id, self.bot))

    @discord.ui.button(label="Kitleme", style=discord.ButtonStyle.secondary, emoji="🔒", custom_id="kitle")
    async def kitle_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return
        kanal = self.bot.get_channel(self.channel_id)
        if not kanal:
            await interaction.response.send_message("Kanal bulunamadı!", ephemeral=True)
            return
        await kanal.set_permissions(interaction.guild.default_role, connect=False)
        await interaction.response.send_message("Kanal kapatıldı artık sadece sizin izin verdiğiniz kişiler girebilir.", ephemeral=True)

    @discord.ui.button(label="Kilit Aç", style=discord.ButtonStyle.success, emoji="🔓", custom_id="kilidi_ac")
    async def kilidi_ac_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return
        kanal = self.bot.get_channel(self.channel_id)
        if not kanal:
            await interaction.response.send_message("Kanal bulunamadı!", ephemeral=True)
            return
        await kanal.set_permissions(interaction.guild.default_role, connect=True)
        await interaction.response.send_message("Kanal herkese açıldı!", ephemeral=True)

    @discord.ui.button(label="Görünmez Yap", style=discord.ButtonStyle.secondary, emoji="👁", custom_id="gorunmez")
    async def gorunmez_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return
        kanal = self.bot.get_channel(self.channel_id)
        if not kanal:
            await interaction.response.send_message("Kanal bulunamadı!", ephemeral=True)
            return
        await kanal.set_permissions(interaction.guild.default_role, view_channel=False)
        await interaction.response.send_message("Kanal sadece izin verilenler için görünür yapıldı!", ephemeral=True)

    @discord.ui.button(label="Görünür Yap", style=discord.ButtonStyle.success, emoji="👁", custom_id="gorunur")
    async def gorunur_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return
        kanal = self.bot.get_channel(self.channel_id)
        if not kanal:
            await interaction.response.send_message("Kanal bulunamadı!", ephemeral=True)
            return
        await kanal.set_permissions(interaction.guild.default_role, view_channel=True)
        await interaction.response.send_message("Kanal herkes için görünür yapıldı!", ephemeral=True)

    @discord.ui.button(label="Sil", style=discord.ButtonStyle.danger, emoji="🗑", custom_id="sil", row=2)
    async def sil_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Bu panel size ait değil!", ephemeral=True)
            return
        kanal = self.bot.get_channel(self.channel_id)
        if not kanal:
            await interaction.response.send_message("Kanal zaten silinmiş!", ephemeral=True)
            return
        await interaction.response.send_message("Kanal siliniyor...", ephemeral=True)
        if str(self.user_id) in self.ozel_odalar:
            del self.ozel_odalar[str(self.user_id)]
            JsonManager.save_data(self.ozel_odalar)
        await kanal.delete(reason=f"{interaction.user} tarafından silindi") 