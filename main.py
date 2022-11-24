from discord import Intents, Interaction, Embed
from discord.ext import commands
from dotenv import load_dotenv
import traceback
import sqlite3
import discord
import logging
import os
import discordSuperUtils
import aiosqlite

logger = logging.getLogger("Custom_s")
logging.basicConfig(level=logging.NOTSET, filename="custom-s.log")
load_dotenv('./.env')
TOKEN =  os.getenv("TOKEN")

class Custom_s(commands.Bot):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents,command_prefix="$")
    
        self.inital_extensions = [
            "cogs.fun.memes",
            "cogs.bot_uh_things.infos",
            "cogs.moderation.moderation",
        ]
    
    async def on_guild_join(self, guild: discord.Guild):
        logger.info(f"Guild joined: {guild.name}\n\tID: {guild.id}")
        print(f"Guild joined: {guild.name}\n\tID: {guild.id}")

    async def on_guild_remove(self, guild: discord.Guild):
        logger.info(f"Guild left: {guild.name}\n\tID: {guild.id}")
        print(f"Guild left: {guild.name}\n\tID: {guild.id}")

    async def on_ready(self):
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
ReactionManager = discordSuperUtils.ReactionManager(client)

@ReactionManager.event()
async def on_reaction_event(guild, channel, message, member, emoji):
    """This event will be run if there isn't a role to add to the member."""

    if ...:
        print("Created ticket.")

@client.event
async def on_ready():
    database = discordSuperUtils.DatabaseManager.connect(await aiosqlite.connect("DB.sqlite"))
    await ReactionManager.connect_to_database(database, ["reaction_roles"])
    print("Test - But the bot is ready!")

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

@client.hybrid_command()
async def reaction(
    ctx : commands.Context, message, emoji: str, remove_on_reaction, role: discord.Role = None
):
    """
    Does a reaction role.

    Args:
        message (Any): The message ID of the role reaction.
        emoji (str): The emoji of the reaction.
        remove_on_reaction (int): Between 0 and 1, if it's 1, it will remove the reaction  after giving the role.
        role (discord.Role): The role of the reaction.
    """
    message = await ctx.channel.fetch_message(message)

    await ReactionManager.create_reaction(
        ctx.guild, message, role, emoji, remove_on_reaction
    )
    await ctx.defer(ephemeral=True)
    await ctx.send("Added your role!")

@client.tree.context_menu(name="Infos")
async def uinfo(interaction : Interaction, member : discord.Member):
    em = discord.Embed(
        color=discord.Colour.random(),
        title=f"Infos of {member}"
    )
    em.set_author(name=interaction.user)
    em.set_thumbnail(url=interaction.user.avatar.url)
    roles = []
    b = ','.join(roles)
    em.add_field(name="ID: ", value=member.id)
    em.add_field(name="Name: ", value=member.display_name)
    em.add_field(name="Bot: ", value="🧑" if not member.bot else "🤖")
    em.add_field(name=f"Roles: ({len(roles)}", value=b, inline=False)
    em.add_field(name="Top Role: ", value=member.top_role.mention, inline=False)
    em.add_field(name="Account Creation Date: ", value=member.created_at)
    em.add_field(name="Server Joined At: ", value=member.joined_at)
    await interaction.response.send_message(embed=em)

client.run(TOKEN)
