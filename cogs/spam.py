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
        spamList = [404342118878937099, 726533388751863858, 155027196530917376, 832572222597496842, 832370449744658453, 531201462869557261, 333405321034989568, 590980471865868323, 268432928600621058, 328463751562919936, 852634365346447360, 537016490432528384, 289477325441990678, 356234221825818627, 343149618797740034, 534448452059529216]
        em = nextcord.Embed(color=0x4ebc7f, title="**:warning: :bangbang: :warning: ÇOK ÖNEMLİ DUYURU :warning: :bangbang: :warning:**", description="Eğer bu mesajı görüyorsanız **osu!türkiye Open 2023** \nturnuvası için **qualifier odanızı ACİLEN belirlemeniz** gerekmekte.\n[Buraya](https://ptb.discord.com/channels/1097961220960682056/1113179401551622194/1121506594186854450) tıklayarak detayları görebilirsiniz.\n Halen **kayıt olamayanlar için** oda süreleri **1 gün** daha uzatıldı.")
        em.set_image(url="https://cdn.discordapp.com/attachments/1099985651987910686/1103020297579409498/agunga.png")
        em.set_footer(text="Qualifier odaları için son tarih: 26 Haziran Pazartesi 18:00")
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
        for id in [1105948421187186758, 1098884763223330916, 1099985542348808223, 1098884990365859970, 1100184587419783278]:
            roleList.append(interaction.guild.get_role(id))
        givenrole = interaction.guild.get_role(1145387240072163370)
        for rol in roleList:
            i = 1
            for dude in rol.members:
                print(f"dude {i}")
                i += 1
                await dude.add_roles(givenrole)
        await interaction.followup.send("başarılı!")

def setup(client):
    client.add_cog(Spam(client))