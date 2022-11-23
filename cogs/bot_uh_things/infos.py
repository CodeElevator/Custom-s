import discord
from discord.ext import commands
from discord import app_commands

class Infos(commands.Cog):
    """
    Infos commands
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="botinfo", description="Bot infos!")
    async def _botinfo(self, interaction : discord.Interaction):
        em = discord.Embed(
            color=discord.Colour.gold(),
            title="Infos of the bot",
        )
        em.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        em.description = 'A simple bot'
        em.add_field(name="Servers", value=len(self.bot.guilds))
        em.add_field(name="Online Users", value=str(len({m.id for m in self.bot.get_all_members() if m.status is not discord.Status.offline})))
        em.add_field(name='Total Amount Of Users', value=len(self.bot.users))
        em.add_field(name="Library", value=f"discord.py {discord.__version__}")
        em.add_field(name="Bot Latency", value=f"{self.bot.ws.latency * 1000:.0f} ms")
        em.add_field(name="Invite", value=f"In my profile")
        em.add_field(name='GitHub', value='[Click here](https://github.com/CodeElevator/Custom-s)')

        em.set_footer(text="Custom's - Made with discord.py")
        await interaction.response.send_message(embed=em)
async def setup(bot):
    await bot.add_cog(Infos(bot))