import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
from ossapi import OssapiAsync, UserLookupKey, GameMode, RankingType
from ossapi.enums import Statistics
import gspread
from pathlib import Path
from email_validator import validate_email, EmailNotValidError
import pandas as pd
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

filepath = Path("ahmetbot.json")
gc = gspread.service_account(filename=filepath)
sh = gc.open("Data Sheet - osu!türkiye Open 2023")

class StaffReg(commands.Cog):
    def __init__ (self, client):
        self.client = client

    @nextcord.slash_command(
        name="apply",
        description="Apply for a staff position!"
    )
    async def apply(self, interaction: Interaction):
        pass
    @apply.subcommand(
        name="staff",
        description="Apply for a staff position!"
    )
    async def applystaff(
        self,
        interaction: nextcord.Interaction,
        email: str,
        position: str = SlashOption(
            choices = {"Referee / Hakem": "Referee", "Mappooler": "Mappooler", "Streamer / Yayıncı": "Streamer", "Testplayer": "Testplayer"},
        ),
    ):
        await interaction.response.defer()
        namesDict = {}
        u = 1
        async with aiofiles.open("staffreg.csv", "r") as f:
            async for line in AsyncReader(f):
                namesDict.update({line[0]: int(u)})
                u += 1
        try:
            user = await api.user(interaction.user.display_name, key=UserLookupKey.USERNAME)
        except ValueError:
            em = nextcord.Embed(color=0xff0000, title="**Kullanıcı doğrulanamadı!** :x:", description=f"Kullanıcı ismin osu! isminle eşleşmiyor. Yetkililere ulaş.")
            pass
        else:
            usernameList = []
            async with aiofiles.open("data.csv", "r") as f:
                async for i in AsyncReader(f):
                    usernameList.append(i[0])
            if user.username in usernameList:
                em = nextcord.Embed(color=0xff0000, title="**İzin yok!** :x:", description=f"Turnuvada kaydın bulunduğundan başvurun engellendi.\nYine de başvurmak istiyorsan `/kayıt sil` yaz!")
            else:
                dataList=[]
                if user.username in namesDict.keys():
                    async with aiofiles.open("staffreg.csv", 'r', newline="") as csvfile:
                        async for line in AsyncReader(csvfile):
                            dataList.append(line)
                    index = namesDict[f"{user.username}"]
                    dataList.pop(index-1)
                    async with aiofiles.open("staffreg.csv", 'w', newline="") as csvfile:
                        csvwriter = AsyncWriter(csvfile)
                        await csvwriter.writerows(dataList)
                try:
                    emailinfo = validate_email(email, check_deliverability=True)
                    email = emailinfo.normalized
                except EmailNotValidError:
                    em = nextcord.Embed(color=0xff0000, title="**Error!** :x:", description=f"Invalid email address.")
                    pass
                else:
                    addedData = [user.username, f"{interaction.user.name}#{interaction.user.discriminator}", email, position, f"https://osu.ppy.sh/users/{user.id}", interaction.user.id]
                    async with aiofiles.open("staffreg.csv", "a", newline="") as csvfile:
                        csvwriter = AsyncWriter(csvfile)
                        await csvwriter.writerow(addedData)
                    em = nextcord.Embed(color=0x00FF00, title="**Success!** :white_check_mark:", description=f"Your application has been received.")
        await interaction.followup.send(embed=em, ephemeral=True)
    
    @apply.subcommand(
        name="accept",
        description="Yetkili alımı yap!"
    )
    @application_checks.has_any_role("Yetkili", "Sheets")
    async def acceptstaff(self, interaction: Interaction, name: str):
        await interaction.response.defer()
        namesDict = {}
        u = 0
        async with aiofiles.open("staff.csv", "r") as f:
            async for i in AsyncReader(f):
                namesDict.update({i[0].lower(): u})
                u += 1
        if name.lower() in namesDict.keys():
            em = nextcord.Embed(color=0xff0000, title="**Hata!** :x:", description=f"Kullanıcı zaten kabul edilmiş.")
        else:
            try:
                user = await api.user(name, key=UserLookupKey.USERNAME)
            except ValueError:
                em = nextcord.Embed(color=0xff0000, title="**Kullanıcı bulunamadı!** :x:", description=f"Kullanıcı ismi osu! ile eşleşmiyor.")
                pass
            else:
                worksheet = sh.worksheet("staff_raw")
                async with aiofiles.open("staffreg.csv", "r") as f:
                    positionDict = {}
                    async for i in AsyncReader(f):
                        positionDict.update({i[0]: [i[1],i[3],i[5],i[2]]})
                id = int(positionDict[user.username][2])
                target = interaction.guild.get_member(id)
                if target == None:
                    em = nextcord.Embed(color=0xff0000, title="**Kullanıcı bulunamadı!** :x:", description=f"Kullanıcı ID discord sunucusunda bulunamadı.")
                    pass
                else:
                    worksheet.append_row([user.username, user.id, positionDict[user.username][0], positionDict[user.username][1], positionDict[user.username][3]])
                    df = pd.DataFrame(worksheet.get_all_records())
                    df.to_csv("staff.csv", header=True, index=False)
                    
                    if positionDict[user.username][1] == "Referee":
                        await target.add_roles(interaction.guild.get_role(1098884075902750750))
                    elif positionDict[user.username][1] == "Mappooler":
                        await target.add_roles(interaction.guild.get_role(1098884763223330916))
                    elif positionDict[user.username][1] == "Streamer":
                        await target.add_roles(interaction.guild.get_role(1098884990365859970))
                    elif positionDict[user.username][1] == "Testplayer":
                        await target.add_roles(interaction.guild.get_role(1100184587419783278))
                    else:
                        pass
                    em = nextcord.Embed(color=0x00FF00, title="**Başarılı!** :white_check_mark:", description=f"{target.mention} {positionDict[user.username][1]} pozisyonuna alındı.")
        await interaction.followup.send(embed=em)

def setup(client):
    client.add_cog(StaffReg(client))