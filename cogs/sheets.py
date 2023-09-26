import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import tasks, commands, application_checks
import gspread
from gspread_dataframe import set_with_dataframe 
from pathlib import Path
import pandas as pd
import asyncio

filepath = Path("ahmetbot.json")
gc = gspread.service_account(filename=filepath)
sh = gc.open("Data Sheet - osu!türkiye Bobble League")

class Sheets(commands.Cog):
    def __init__ (self, client):
        self.client = client
    
    @nextcord.slash_command(
        name="sheets",
        description="Sheets management."
    )
    @application_checks.has_any_role("Yetkili", "Sheets")
    async def sheets(self, interaction: Interaction):
        pass
    @sheets.subcommand(
        description="Sheets management."
    )
    @application_checks.has_any_role("Yetkili", "Sheets")
    async def update(
        self,
        interaction: Interaction,
        sheet_name: str = SlashOption(
            choices = {"All (USE WITH CAUTION)": "all", "Data": "data", "Teams": "teams", "Screening": "screening", "Staffreg": "staffreg", "Staff": "staff"},
        ),
    ):
        dataNames = ["data", "teams", "screening", "staffreg", "staff"]
        if sheet_name == "all":
            await interaction.response.defer()
            for i in dataNames:
                filepath = Path(f"{i}.csv")
                df = pd.read_csv(filepath)
                worksheet = sh.worksheet(f"{i}_raw")
                worksheet.clear()
                set_with_dataframe(worksheet, df)
                em = nextcord.Embed(color=0x00FF00, title="**Success!** :white_check_mark:", description=f"**All** of the sheets have been updated successfully.")
        else:
            await interaction.response.defer()
            filepath = Path(f"{sheet_name}.csv")
            df = pd.read_csv(filepath)
            worksheet = sh.worksheet(f"{sheet_name}_raw")
            worksheet.clear()
            set_with_dataframe(worksheet, df)
            em = nextcord.Embed(color=0x00FF00, title="**Success!** :white_check_mark:", description=f"{sheet_name} has been updated successfully.")
        await interaction.followup.send(embed=em, ephemeral=True)
    
    @sheets.subcommand(
        description="Sheets management."
    )
    @application_checks.has_any_role("Yetkili", "Sheets")
    async def download(
        self,
        interaction: Interaction,
        sheet_name: str = SlashOption(
            choices = {"All (USE WITH CAUTION)": "all", "Data": "data", "Teams": "teams", "Screening": "screening", "Staffreg": "staffreg", "Staff": "staff"},
        ),
    ):
        dataNames = ["data", "teams", "screening", "staffreg", "staff"]
        if sheet_name == "all":
            await interaction.response.defer()
            for i in dataNames:
                filepath = Path(f"{i}.csv")
                worksheet = sh.worksheet(f"{i}_raw")
                df = pd.DataFrame(worksheet.get_all_records(head=1))
                with open(filepath, "w") as f:
                    df.to_csv(filepath, header=True, index=False)
            em = nextcord.Embed(color=0x00FF00, title="**Success!** :white_check_mark:", description=f"**All** of the sheets have been downloaded successfully.")
        else:
            await interaction.response.defer()
            filepath = Path(f"{sheet_name}.csv")
            worksheet = sh.worksheet(f"{sheet_name}_raw")
            df = pd.DataFrame(worksheet.get_all_records(head=1))
            with open(filepath, "w") as f:
                df.to_csv(filepath, header=True, index=False)
            em = nextcord.Embed(color=0x00FF00, title="**Success!** :white_check_mark:", description=f"{sheet_name} has been downloaded successfully.")
        await interaction.followup.send(embed=em, ephemeral=True)

def setup(client):
    client.add_cog(Sheets(client))