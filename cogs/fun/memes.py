import discord
from discord.ext import commands
from discord import app_commands
import httpx
import json

async def gimme_memes(interaction : discord.Interaction):
    async with httpx.AsyncClient() as req:
        result = await req.get(f"https://meme-api.herokuapp.com/gimme")
        res = result.text
        data = json.loads(res)
        if data['nsfw']:
            await interaction.response.send_message("The meme here is an NSFW meme, please retry.")
        embed = discord.Embed(
            title=data['title'],
            color=discord.Colour.random()
        )
        embed.set_footer(text=f"From: {data['subreddit']}")
        embed.set_image(url=data['url'])
        embed.set_author(name=data['author'], url=data['postLink'])
        await interaction.response.send_message(embed=embed)


class Memes(commands.Cog):
    """
    Meme commands.
    Commands:
        /meme: gives memes (not NSFW)
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="meme")
    async def _meme(self, interaction : discord.Interaction):
        """
        Gives 1 meme.

        Args:
            interaction (discord.Interaction): The interaction that invokes this coroutine .
        """
        await gimme_memes(interaction)

async def setup(bot):
    await bot.add_cog(Memes(bot))