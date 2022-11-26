import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View
import sqlite3
import traceback

class ConfirmThinguy(View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label="Image 1", style=discord.ButtonStyle.success)
    async def img1(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT img FROM welcome WHERE guild_id = {interaction.guild_id}")
        result = cur.fetchone()
        if result == "NULL":
            cur.execute("INSERT INTO welcome(guild_id, img) VALUES(?,?)", ("pic1.jpg", interaction.guild_id))
            await interaction.response.send_message(f"Image has been set!")
            db.commit()
        else:
            cur.execute("UPDATE welcome SET img = ? WHERE guild_id = ?", ("pic1.jpg", interaction.guild_id))
            await interaction.response.send_message(f"Image has been updated!")
            db.commit()

    @discord.ui.button(label="Image 2", style=discord.ButtonStyle.primary)
    async def img2(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT img FROM welcome WHERE guild_id = {interaction.guild_id}")
        result = cur.fetchone()
        if result == "NULL":
            cur.execute("INSERT INTO welcome(guild_id, img) VALUES(?,?)", ("pic2.jpg", interaction.guild_id))
            await interaction.response.send_message(f"Image has been set!")
            db.commit()
        else:
            cur.execute("UPDATE welcome SET img = ? WHERE guild_id = ?", ("pic2.jpg", interaction.guild_id))
            await interaction.response.send_message(f"Image has been updated!")
            db.commit()


class Welcoming(commands.Cog):
    """
        Welcoming group cog
    """
    def __init__(self, bot):
        self.bot = bot
    
    welcoming = app_commands.Group(name="welcome", description="Setups welcoming", guild_only=True, nsfw=False)

    @welcoming.command(name="channel")
    async def channel(self, interaction : discord.Interaction, channel : discord.TextChannel):
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT ch_id FROM welcome WHERE guild_id = {interaction.guild_id}")
        result = cur.fetchone()
        if result == "NULL":
            cur.execute("INSERT INTO welcome(guild_id, ch_id) VALUES(?,?)", (interaction.guild_id, channel.id))
            await interaction.response.send_message(f"Channel has been set to {channel.mention}")
            db.commit()
        else:
            cur.execute("UPDATE welcome SET ch_id = ? WHERE guild_id = ?", (channel.id, interaction.guild_id))
            await interaction.response.send_message(f"Channel has been updated to {channel.mention}")
            db.commit()

    @welcoming.command(name="message")
    async def message(self, interaction : discord.Interaction, message : str):
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT msg FROM welcome WHERE guild_id = {interaction.guild_id}")
        result = cur.fetchone()
        if result == "NULL":
            cur.execute("INSERT INTO welcome(guild_id, msg) VALUES(?,?)", (message, interaction.guild_id))
            db.commit()
            await interaction.response.send_message(f"Message has been set!")
            
        else:
            cur.execute("UPDATE welcome SET msg = ? WHERE guild_id = ?", (message, interaction.guild_id))
            db.commit()
            await interaction.response.send_message(f"Message has been updated!")
            
    
    @welcoming.command(name="image")
    async def image(self, interaction : discord.Interaction):
        view = ConfirmThinguy()
        await interaction.response.send_message("Wich image do you prefer?", files=[discord.File("pic1.jpg"), discord.File("pic2.jpg")], view=view)
    

async def setup(bot):
    await bot.add_cog(Welcoming(bot))