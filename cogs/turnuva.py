import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from ossapi import Ossapi, UserLookupKey
from dotenv import load_dotenv
import os
import asyncio
import csv
import aiofiles
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter

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
    async def sil(self, interaction: Interaction):
        namesDict = {}
        u = 1
        async with aiofiles.open("data.csv", "r") as f:
            async for line in AsyncReader(f):
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
                async with aiofiles.open("data.csv", 'r', newline="") as csvfile:
                    async for line in AsyncReader(csvfile):
                        dataList.append(line)       
                index = namesDict[f"{user.username}"]
                dataList.pop(index-1)
                async with aiofiles.open("data.csv", 'w', newline="") as csvfile:
                    csvwriter = AsyncWriter(csvfile)
                    await csvwriter.writerows(dataList)

                em = nextcord.Embed(color=0x00FF00, title="**Başarılı!** :white_check_mark:", description="Turnuva kaydınız silindi.")
            else:
                em = nextcord.Embed(color=0xff0000, title="**Başarısız!** :x:", description=f"Turnuvada zaten kaydın yok.")
        await interaction.send(embed=em)
    @register.subcommand(
        name="ol",
        description="Turnuvaya kaydınızı yapar."
    )
    async def ol(self, interaction: Interaction):
        await interaction.response.defer()
        namesDict = {}
        u = 1
        async with aiofiles.open("data.csv", "r") as f:
            async for line in AsyncReader(f):
                namesDict.update({line[0]: int(u)})
                u += 1
        try:
            user = api.user(interaction.user.display_name, key=UserLookupKey.USERNAME)
        except ValueError:
            em = nextcord.Embed(color=0xff0000, title="**Kullanıcı doğrulanamadı!** :x:", description=f"Kullanıcı ismin osu! isminle eşleşmiyor. Yetkililere ulaş.")
            pass
        else:
            if interaction.user.display_name in namesDict.keys():
                em = nextcord.Embed(color=0xff0000, title="**Başarısız!** :x:", description="Turnuvaya kaydınız daha önce yapılmış.")
            else:
                async with aiofiles.open("data.csv", 'a', newline="") as csvfile:
                    csvwriter = AsyncWriter(csvfile)
                    await csvwriter.writerow([user.username, user.id, f"{user.statistics.global_rank}", f"{interaction.user.name}#{interaction.user.discriminator}"])
                em = nextcord.Embed(color=0x00FF00, title="**Başarılı!** :white_check_mark:", description="Turnuvaya kaydınız gerçekleştirildi.")
                await interaction.user.add_roles(interaction.guild.get_role(1109884538626261022))
        await interaction.followup.send(embed=em)

    @nextcord.slash_command(
        name="takım",
        description="Takımlarla ilgili işlemler gerçekleştirir."
    )
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