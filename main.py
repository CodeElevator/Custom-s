from discord import Intents, Interaction, Embed
from discord.ext import commands
from dotenv import load_dotenv
import traceback
import sqlite3
import discord
import logging
import os

logger = logging.getLogger("Custom_s")
logging.basicConfig(level=logging.NOTSET, filename="custom-s.log")
load_dotenv('./.env')
TOKEN =  os.getenv("TOKEN")

class Custom_s(commands.Bot):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents,command_prefix="$")
    
        self.inital_extensions = [
            "cogs.fun.memes",
            "cogs.moderation.moderation",
            "cogs.moderation.reactionroles"
        ]
    
    async def on_guild_join(self, guild: discord.Guild):
        logger.info(f"Guild joined: {guild.name}\n\tID: {guild.id}")
        print(f"Guild joined: {guild.name}\n\tID: {guild.id}")

    async def on_guild_remove(self, guild: discord.Guild):
        logger.info(f"Guild left: {guild.name}\n\tID: {guild.id}")
        print(f"Guild left: {guild.name}\n\tID: {guild.id}")

    async def on_ready(self):
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS rolereact(
                    role INTEGER,
                    msg_id INTEGER,
                    emoji TEXT
                )
            """
        )
        db.commit()
        print("\n".join([
            f"Logged in as {self.user} (ID: {self.user.id})\n",
            f"Use this URL to invite {self.user}:",
            f"https://discord.com/api/oauth2/authorize?client_id={self.user.id}&scope=applications.commands%20bot"
        ]))


    async def setup_hook(self) -> None:
        for ext in self.inital_extensions:
            await self.load_extension(ext)
        await self.tree.sync(guild=None)

intents = Intents.all()
intents.messages = True

client = Custom_s(intents=intents)

class Feedback(discord.ui.Modal, title='Feedback'):

    feedback = discord.ui.TextInput(
        label='What is your feedback?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=True,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {interaction.user}!', ephemeral=True)
        channel = client.get_channel(1041940166270521424)
        await channel.send(embed = Embed(
            title=f"Feedback from: {str(interaction.user)}",
            description= self.feedback.value,
        ))

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)

@client.tree.command()
async def feedback(interaction: Interaction):
    """Submit feedback"""
    logger.info("heya, someone did a feedback")
    await interaction.response.send_modal(Feedback())

client.run(TOKEN)