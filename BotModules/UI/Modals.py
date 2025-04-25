import discord
from discord import InputText

class KanalIsimModal(discord.ui.Modal):
    def __init__(self, channel_id, bot):
        super().__init__(title="Kanal İsmini Değiştir")
        self.channel_id = channel_id
        self.bot = bot
        self.add_item(
            InputText(
                label="Yeni Kanal İsmi",
                placeholder="Kanal ismini girin...",
                style=discord.InputTextStyle.short,
                max_length=100
            )
        )

    async def callback(self, interaction: discord.Interaction):
        yeni_isim = self.children[0].value
        try:
            kanal = self.bot.get_channel(self.channel_id)
            if kanal:
                eski_isim = kanal.name
                await kanal.edit(name=yeni_isim)
                await interaction.response.send_message(f"Kanal ismi `{eski_isim}` ➠ `{yeni_isim}` olarak değiştirildi!", ephemeral=True)
            else:
                await interaction.response.send_message("Kanal bulunamadı!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Kanal ismi değiştirilirken hata oluştu: {e}", ephemeral=True) 