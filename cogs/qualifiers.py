import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from ossapi import OssapiAsync, UserLookupKey
import cooldowns
from dotenv import load_dotenv
import os
import gspread
from pathlib import Path

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
api = OssapiAsync(client_id, client_secret)

class Qualifiers(commands.Cog):
    def __init__(self, client):
        self.client = client     
    @nextcord.slash_command(
        name="qualifier",
    )
    async def qualifier(self, interaction: Interaction):
        pass
    @qualifier.subcommand(
        name="kayıt",
        description="Qualifier lobisine kayıt ol!",
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def kayıt(self, interaction: Interaction, oda_numarası: int):
        await interaction.response.defer()
        filepath = Path("ahmetbot.json")
        gc = gspread.service_account(filename=filepath)
        sh = gc.open("Referee - osu!TR Open '23")
        worksheet = sh.worksheet("Qualifiers Schedule")
        values_list = worksheet.col_values(25)
        values_list2 = worksheet.col_values(24)
        values_list3 = worksheet.col_values(4)
        values_list3.pop(0)
        if str(oda_numarası) not in values_list3:
            em = nextcord.Embed(color=0xff0000, title="**Oda bulunamadı!** :x:", description=f"Bu numaraya sahip bir oda yok.")
        else:    
            try:
                user = await api.user(interaction.user.display_name, key=UserLookupKey.USERNAME)
            except ValueError:
                em = nextcord.Embed(color=0xff0000, title="**Kullanıcı doğrulanamadı!** :x:", description=f"Kullanıcı ismin osu! isminle eşleşmiyor. Yetkililere ulaş.")
                pass
            else:
                if user.username in values_list:
                    em = nextcord.Embed(color=0xff0000, title="**Zaten bir odaya kayıtlısın!** :x:", description=f"Tarih değişikliği için yetkililere ulaş.")
                elif user.username in values_list2:
                    values_list = worksheet.row_values(oda_numarası + 1)
                    for i in range(8,25):
                        if values_list[i-1] == "":
                            worksheet.update_cell(oda_numarası+1, i, user.username)
                            checker = True
                            break
                    if checker is not True:
                        em = nextcord.Embed(color=0xff0000, title="**Bu oda dolu!** :x:", description=f"Başka bir oda seç.")
                    else:
                        em = nextcord.Embed(color=0x00ff00, title="**Başarılı!** :white_check_mark:", description=f"`{oda_numarası}` numaralı odaya kaydın gerçekleşti.")
                else:
                    em = nextcord.Embed(color=0xff0000, title="**Kullanıcı bulunamadı!** :x:", description=f"Turnuvaya kayıtlı değilsin.")
        await interaction.followup.send(embed=em)
def setup(client):
    client.add_cog(Qualifiers(client))