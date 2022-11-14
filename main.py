from discord import app_commands, Intents, Interaction, Embed, Object
from discord.ext import commands
from dotenv import load_dotenv
import traceback
import discord
import os

load_dotenv('./.env')
TOKEN =  os.getenv("TOKEN")

class Custom_s(commands.Bot):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents,command_prefix="$")
    
        self.inital_extensions = [
            "cogs.misc.math",
        ]
    
    async def on_ready(self):
        print("\n".join([
            f"Logged in as {client.user} (ID: {client.user.id})\n",
            f"Use this URL to invite {client.user} to your server:",
            f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot"
        ]))


    async def setup_hook(self) -> None:
        for ext in self.inital_extensions:
            await self.load_extension(ext)
        await self.tree.sync(guild=None)

intents = Intents.all()
intents.messages = True

client = Custom_s(intents=intents)


class Feedback(discord.ui.Modal, title='Feedback'):

    name = discord.ui.TextInput(
        label="Can you tell us your username?",
        style=discord.TextStyle.short,
        required=True,
        placeholder="Your username here..."
    )

    feedback = discord.ui.TextInput(
        label='What is your feedback?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=True,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {interaction.user}!', ephemeral=True)
        channel = client.get_channel(938844696971718743)
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
    await interaction.response.send_modal(Feedback())

client.run(TOKEN)