import discord
from discord.ext import commands
from discord import app_commands

class Infos(commands.Cog):
    """
    Infos commands
    """
    def __init__(self, bot):
        self.bot = bot

    

async def setup(bot):
    await bot.add_cog(Infos(bot))