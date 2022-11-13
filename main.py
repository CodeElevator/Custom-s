from discord import app_commands, Intents, Client, Interaction
from dotenv import load_dotenv
import os

load_dotenv('./.env')
TOKEN =  os.getenv("TOKEN")

class Custom_s(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def on_ready(self):
        print("\n".join([
            f"Logged in as {client.user} (ID: {client.user.id})",
            "",
            f"Use this URL to invite {client.user} to your server:",
            f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot"
        ]))

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=None)

intents = Intents.all()
intents.messages = True

client = Custom_s(intents=intents)

@client.tree.command()
async def hello(interaction: Interaction):
    """ Says hello or something """
    print(f"> {interaction.user} used the command.")
    await interaction.response.send_message(
        f"Hi **{interaction.user}**, thank you for saying hello to me."
    )


client.run(TOKEN)