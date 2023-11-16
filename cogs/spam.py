import nextcord
from nextcord import Interaction
from nextcord.ext import tasks, commands, application_checks

class Spam(commands.Cog):
    def __init__(self, client):
        self.client=client

    @nextcord.slash_command(
        name = "spam"
    )
    @application_checks.is_owner()
    async def spam(self, interaction: Interaction):
        await interaction.response.defer()
        spamList = [USERIDS]
        em = nextcord.Embed(color=0x4ebc7f, title="TITLE", description="DESC")
        em.set_image(url="IMAGELINK")
        em.set_footer(text="FOOTER")
        for i in spamList:
            member = await interaction.guild.fetch_member(i)
            try:
                await member.send(embed=em)
            except nextcord.errors.Forbidden:
                pass
        await interaction.followup.send("başarılı!")

    @nextcord.slash_command(
        name = "rolver"
    )
    @application_checks.is_owner()
    async def rolver(self, interaction: Interaction):
        await interaction.response.defer()
        roleList = []
        for id in [USERIDS]:
            roleList.append(interaction.guild.get_role(id))
        givenrole = interaction.guild.get_role(ROLEID)
        for rol in roleList:
            i = 1
            for dude in rol.members:
                print(f"dude {i}")
                i += 1
                await dude.add_roles(givenrole)
        await interaction.followup.send("başarılı!")

def setup(client):
    client.add_cog(Spam(client))