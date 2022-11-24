import discord
from discord.ext import commands
from discord import app_commands

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
        em.add_field(name="Account Creation Date: ", value=user.created_at)
        em.add_field(name="Server Joined At: ", value=user.joined_at)
        await interaction.response.send_message(embed=em)


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
    
    @app_commands.command(name="userinfo")
    async def _uinfo(self, interaction : discord.Interaction, member : discord.Member = None):
        if member is None:
            member = interaction.user
        await self._userinfo(interaction, member)

async def setup(bot):
    await bot.add_cog(Infos(bot))