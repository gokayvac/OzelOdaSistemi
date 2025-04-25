import discord

TOKEN = ""
VC_JOIN = 
KATEGORI = 
KANAL = 

KULLANICI_LIMIT_SECENEK = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 50, 99]
BITRATE_SECENEK = [8000, 16000, 32000, 64000, 96000, 128000]
REGION_SECENEK = [
    ("Otomatik", None),
    ("Amerika", discord.VoiceRegion.us_west),
    ("Avrupa", discord.VoiceRegion.europe),
    ("Asya", discord.VoiceRegion.singapore),
    ("Brezilya", discord.VoiceRegion.brazil)
]

DATA = "data/data.json"

def get_intents():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    intents.voice_states = True
    return intents 
