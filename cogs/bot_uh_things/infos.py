import discord
from discord.ext import commands
from discord import app_commands
from discord_timestamps import format_timestamp
import platform
import distro
import time
import psutil

def uptime():
	return round((time.time() - psutil.boot_time()) / 60, 2)


class Infos(commands.Cog):
    """
    Infos commands
    """
    def __init__(self, bot):
        self.bot = bot
    
    async def _userinfo(self, interaction : discord.Interaction, user : discord.Member):
        em = discord.Embed(
            color=discord.Colour.random(),
            title=f"Infos of {user}"
        )
        em.set_author(name=interaction.user)
        em.set_thumbnail(url=interaction.user.avatar.url)
        roles = []
        for role in user.roles:
            if role.name != "@everyone":
                roles.append(role.mention)
        b = ','.join(roles)
        em.add_field(name="ID: ", value=user.id)
        em.add_field(name="Name: ", value=user.display_name)
        em.add_field(name="Bot: ", value="🧑" if not user.bot else "🤖")
        em.add_field(name=f"Roles: ({len(roles)}", value=b, inline=False)
        em.add_field(name="Top Role: ", value=user.top_role.mention, inline=False)
        em.add_field(name="Account Creation Date: ", value=format_timestamp(user.created_at.timestamp()))
        em.add_field(name="Server Joined At: ", value=format_timestamp(user.joined_at.timestamp()))
        await interaction.response.send_message(embed=em)


    @app_commands.command(name="botinfo", description="Bot infos!")
    async def _botinfo(self, interaction : discord.Interaction):
        em = discord.Embed(
            color=discord.Colour.gold(),
            title="Infos of the bot",
        )
        em.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        em.description = self.bot.description
        memoryused = round(psutil.virtual_memory().used / 1000000000, 2)
        memory = f"{memoryused}GB"
        em.add_field(name="Servers", value=len(self.bot.guilds))
        em.add_field(name="Online Users", value=str(len({m.id for m in self.bot.get_all_members() if m.status is not discord.Status.offline})))
        em.add_field(name='Total Amount Of Users', value=len(self.bot.users))
        em.add_field(name="Library", value=f"Discord.py {discord.__version__}")
        em.add_field(name="Python Version:", value=platform.python_version())
        em.add_field(name="Operating System:", value=distro.id() if distro.id() != "" else "Windows (Bot In Development)")
        em.add_field(name="Kernel Version:", value=platform.platform(), inline=False)
        em.add_field(name="RAM Used:", value=memory, inline=False)
        em.add_field(name="Uptime:", value=f"{uptime()} minutes.", inline=False)
        em.add_field(name="Bot Latency", value=f"{self.bot.ws.latency * 1000:.0f} ms")
        em.add_field(name="Invite", value=f"In my profile")
        em.add_field(name='GitHub', value='[Click here](https://github.com/CodeElevator/Custom-s)')

        em.set_footer(text="Custom's - Made with discord.py")
        await interaction.response.send_message(embed=em)
    
    @app_commands.command(name="userinfo")
    async def _uinfo(self, interaction : discord.Interaction, member : discord.Member = None):
        if member is None:
            member = interaction.user
        await self._userinfo(interaction, member)

async def setup(bot):
    await bot.add_cog(Infos(bot))