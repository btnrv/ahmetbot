import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import csv
from ossapi import Ossapi, UserLookupKey
import cooldowns
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
api = Ossapi(client_id, client_secret)

class Register(commands.Cog):
    def __init__(self, client):
        self.client=client

    @nextcord.slash_command(
        name="kayıt",
        description="Turnuvaya kaydınızı yapar."
    )
    async def register(self, interaction: Interaction):
        pass

    @register.subcommand(
        name="sil",
        description="Turnuvadaki kaydınızı siler."
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def sil(self, interaction: Interaction):
        namesDict = {}
        u = 1
        with open("data.csv", 'r') as f:
            for line in csv.reader(f):
                namesDict.update({line[0]: int(u)})
                u += 1
        try:
            user = api.user(interaction.user.display_name, key=UserLookupKey.USERNAME)
        except ValueError:
            em = nextcord.Embed(color=0xff0000, title="**Kullanıcı doğrulanamadı!** :x:", description=f"Kullanıcı ismin osu! isminle eşleşmiyor. Yetkililere ulaş.")
            pass
        else:
            dataList = []
            if user.username in namesDict.keys():
                with open("data.csv", 'r', newline="") as csvfile:
                    for line in csv.reader(csvfile):
                        dataList.append(line)        
                index = namesDict[f"{user.username}"]
                dataList.pop(index-1)
                with open("data.csv", 'w', newline="") as csvfile:
                    for i in dataList:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(i)

                dataList = []
                with open("screening.csv", 'r', newline="") as csvfile:
                    for line in csv.reader(csvfile):
                        dataList.append(line)        
                dataList.pop(index-2)
                with open("screening.csv", 'w', newline="") as csvfile:
                    for i in dataList:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(i)        
                em = nextcord.Embed(color=0x00FF00, title="**Başarılı!** :white_check_mark:", description="Turnuva kaydınız silindi.")
            else:
                em = nextcord.Embed(color=0xff0000, title="**Başarısız!** :x:", description=f"Turnuvada zaten kaydın yok.")
        await interaction.send(embed=em)
    @register.subcommand(
        name="ol",
        description="Turnuvaya kaydınızı yapar."
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def ol(self, interaction: Interaction):
        namesDict = {}
        u = 1
        with open("data.csv", 'r') as f:
            for line in csv.reader(f):
                namesDict.update({line[0]: int(u)})
                u += 1
        try:
            user = api.user(interaction.user.display_name, key=UserLookupKey.USERNAME)
        except ValueError:
            em = nextcord.Embed(color=0xff0000, title="**Kullanıcı doğrulanamadı!** :x:", description=f"Kullanıcı ismin osu! isminle eşleşmiyor. Yetkililere ulaş.")
            pass
        else:
            if user.username in namesDict.keys():
                em = nextcord.Embed(color=0xff0000, title="**Başarısız!** :x:", description="Turnuvaya kaydınız daha önce yapılmış.")
            else:
                with open("data.csv", 'a', newline="") as csvfile:
                    csvwriter = csv.writer(csvfile) 
                    csvwriter.writerow([user.username, user.id, f"{user.statistics.global_rank}", f"{interaction.user.name}#{interaction.user.discriminator}", interaction.user.id])
                with open("screening.csv", 'a', newline="") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([user.username, user.id])
                    em = nextcord.Embed(color=0x00FF00, title="**Başarılı!** :white_check_mark:", description="Turnuvaya kaydınız gerçekleştirildi.")
        await interaction.send(embed=em)

    @nextcord.slash_command(
        name="takım",
        description="Takımlarla ilgili işlemler gerçekleştirir."
    )
    @cooldowns.cooldown(1, 3, bucket=cooldowns.SlashBucket.author)
    async def takım(self, interaction: Interaction):
        pass
    @takım.subcommand(
        description="Kayıtlı takımları aratır."
    )
    async def liste(self, interaction: Interaction, takım_ismi: str):
        matchingList = []
        desc = ""
        with open("teams.csv", "r") as csvfile:
            for row in csv.reader(csvfile):
                if takım_ismi.lower() == row[2].lower():
                    matchingList.append(row[0])
                    teamName = row[2]
            if not matchingList:
                em = nextcord.Embed(color=interaction.user.color, title=f"Aranan takım: **{takım_ismi}**", description="Sonuç yok! :x:") 
            else:
                for i in matchingList:
                    i = str(i)
                    desc = desc + i + "\n"
                em = nextcord.Embed(color=interaction.user.color, title=f"Aranan takım: **{teamName}** :white_check_mark:", description=desc)
        await interaction.send(embed=em)

def setup(client):
    client.add_cog(Register(client))