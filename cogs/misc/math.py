import discord
from discord import app_commands, Interaction, Embed, Object
from discord.ext import commands

class Math(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="add")
    async def add(self, interaction: Interaction, num1: int, num2: int):
        """
            Adds two numbers together.
        """
        await interaction.response.send_message(f"The result is {num1 + num2}")

    @app_commands.command(name="sub")
    async def sub(self, interaction: Interaction, num1: int, num2: int):
        """
            substracts two numbers together.
        """
        await interaction.response.send_message(f"The result is {num1 - num2}")

    @app_commands.command(name="mul")
    async def mul(self, interaction: Interaction, num1: int, num2: int):
        """
            Multiplies two numbers together.
        """
        await interaction.response.send_message(f"The result is {num1 * num2}")

    @app_commands.command(name="div")
    async def div(self, interaction: Interaction, num1: int, num2: int):
        """
            Divides two numbers together.
        """
        await interaction.response.send_message(f"The result is {num1 / num2}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Math(bot))