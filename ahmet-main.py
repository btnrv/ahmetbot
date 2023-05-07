import nextcord
from nextcord import AllowedMentions, Interaction, SlashOption, ChannelType, ApplicationCheckFailure
from nextcord.ext import commands, tasks
import os
from dotenv import load_dotenv
import aiosqlite
from cooldowns import CallableOnCooldown

load_dotenv()
TOKEN = os.getenv("TOKEN")
client = commands.Bot(intents=nextcord.Intents.all(), owner_ids=[482232269038288916, 581745397182234626])

@client.event
async def on_ready():
    print("Bot hazır")
    print("-----------------")
    await client.change_presence(activity=nextcord.Game(name='asdfg'))
    client.db = await aiosqlite.connect("giveaway.db")

@client.event
async def on_application_command_error(inter: nextcord.Interaction, error):
    error = getattr(error, "original", error)
    if isinstance(error, CallableOnCooldown):
        em = nextcord.Embed(color=0xff0000, title="**Fazla hızlısın!** :x:", description=f"{error.retry_after} saniye sonra tekrar dene.")
        await inter.send(embed=em, ephemeral=True)
    elif isinstance(error, ApplicationCheckFailure):
        em = nextcord.Embed(color=0xff0000, title="**Error!** :x:", description=f"No permissions.")
        await inter.send(embed=em, ephemeral=True)
    else:
        raise error

for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        client.load_extension(f"cogs.{fn[:-3]}")
    else:
        pass

@client.slash_command(
    name="cog"
)
@commands.is_owner()
async def cog(interaction:nextcord.Interaction):
    pass
@cog.subcommand()
async def load(interaction: nextcord.Interaction, extension: str):
    client.load_extension(f"cogs.{extension}")
    await interaction.send("cog yüklendi!")
@cog.subcommand()
async def unload(interaction: nextcord.Interaction, extension: str):
    client.unload_extension(f"cogs.{extension}")
    await interaction.send("cog durduruldu!")
@cog.subcommand()
async def reload(interaction: nextcord.Interaction, extension: str):
    client.reload_extension(f"cogs.{extension}")
    await interaction.send("cog yeniden yüklendi!")

client.run(TOKEN)