import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from ossapi import OssapiAsync, UserLookupKey
from dotenv import load_dotenv
import os
import asyncio
import csv
import aiofiles
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
api = OssapiAsync(client_id, client_secret)

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
        await interaction.response.defer()
        namesDict = {}
        u = 1
        async with aiofiles.open("data.csv", "r") as f:
            async for line in AsyncReader(f):
                namesDict.update({line[0]: int(u)})
                u += 1
        try:
            user = await api.user(interaction.user.display_name, key=UserLookupKey.USERNAME)
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
                await interaction.user.remove_roles(interaction.guild.get_role(1154480594223370362))
            else:
                em = nextcord.Embed(color=0xff0000, title="**Başarısız!** :x:", description=f"Turnuvada zaten kaydın yok.")
        await interaction.send(embed=em)
    @register.subcommand(
        name="ol",
        description="Turnuvaya kaydınızı yapar."
    )
    async def ol(self, interaction: Interaction, takim_ismi: str, takim_arkadasi: nextcord.User):
        await interaction.response.defer()
        namesDict = {}
        u = 1
        async with aiofiles.open("data.csv", "r") as f:
            async for line in AsyncReader(f):
                namesDict.update({line[0]: int(u)})
                u += 1
        try:
            user = await api.user(interaction.user.display_name, key=UserLookupKey.USERNAME)
        except ValueError:
            em = nextcord.Embed(color=0xff0000, title="**Kullanıcı doğrulanamadı!** :x:", description=f"Kullanıcı ismin osu! isminle eşleşmiyor. Yetkililere ulaş.")
            pass
        else:
            if interaction.user.display_name in namesDict.keys():
                em = nextcord.Embed(color=0xff0000, title="**Başarısız!** :x:", description="Turnuvaya kaydınız daha önce yapılmış.")
            else:
                if len(takim_ismi) > 15:
                    takim_ismi = takim_ismi[0:14]
                async with aiofiles.open("data.csv", 'a', newline="") as csvfile:
                    csvwriter = AsyncWriter(csvfile)
                    await csvwriter.writerow([interaction.user.nick, takim_ismi, f"{interaction.user.nick}", f"{takim_arkadasi.nick}"])
                em = nextcord.Embed(color=0x00FF00, title="**Başarılı!** :white_check_mark:", description=f"Turnuvaya kaydınız gerçekleştirildi.\n\nTakım ismi: **{takim_ismi}**\n Takım Üyeleri: {interaction.user.mention}, {takim_arkadasi.mention} ")
                await interaction.user.add_roles(interaction.guild.get_role(1154480594223370362))
                await takim_arkadasi.add_roles(interaction.guild.get_role(1154480594223370362))
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
    async def bul(self, interaction: Interaction, takım_ismi: str):
        await interaction.response.defer()
        matchingList = []
        playersNames = []
        desc = ""
        async with aiofiles.open("data.csv", "r") as csvfile:
            async for row in AsyncReader(csvfile):
                if takım_ismi.lower() == row[1].lower():
                    matchingList.append(row[0])
                    teamName = row[1]
                    playersNames.append(f"{row[2]}, {row[3]}")
            if not matchingList:
                em = nextcord.Embed(color=interaction.user.color, title=f"Aranan takım: **{takım_ismi}**", description="Sonuç yok! :x:") 
            else:
                for i in playersNames:
                    i = str(i)
                    desc = desc + i + "\n"
                em = nextcord.Embed(color=interaction.user.color, title=f":white_check_mark: Aranan takım: **{teamName}**", description=desc)
        await interaction.followup.send(embed=em)
    @takım.subcommand(
        description="Kayıtlı takımları listeler."
    )
    async def liste(self, interaction: Interaction):
        await interaction.response.defer()
        printList = []
        printText = ""
        i = 0
        async with aiofiles.open("data.csv", "r") as csvfile:
            async for row in AsyncReader(csvfile):
                if i == 0:
                    i += 1
                else:
                    printList.append(f"\n**{row[1]}**: {row[2]}**[C]**, {row[3]}")
        for i in printList:
            printText += i
        em = em = nextcord.Embed(color=interaction.user.color, title=f":white_check_mark: Kayıtlı Takımlar ({len(printList)})", description=printText)
        await interaction.followup.send(embed=em)

def setup(client):
    client.add_cog(Register(client))