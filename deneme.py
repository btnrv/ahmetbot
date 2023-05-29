import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import asyncio
from ossapi import OssapiAsync
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
api = OssapiAsync(client_id, client_secret)

class deneme(commands.Cog):
    def __init__(self, client):
        self.client=client
    @nextcord.slash_command(
        name="deneme"
    )
    async def deneme(self, interaction: Interaction):
        user = await api.user(interaction.user.display_name)
        print(user.username)
        await interaction.response.send_message("deneme")

def setup(client):
    client.add_cog(deneme(client))
