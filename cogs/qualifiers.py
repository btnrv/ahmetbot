import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import csv
from ossapi import Ossapi, UserLookupKey, GameMode, RankingType
from ossapi.enums import Statistics
import cooldowns
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
api = Ossapi(client_id, client_secret)

class Qualifiers(commands.Cog):
    def __init__(self, client):
        self.client = client     



def setup(client):
    client.add_cog(Qualifiers(client))