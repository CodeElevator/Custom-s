import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import logging
import datetime
from typing import Optional

# Warns setup

class ConfirmVerannWantsToDoThis(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.blurple)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Ok, I\'ll still report it to lenom!', ephemeral=True)
        logs = logging.getLogger("Custom_s")
        logs.warning("VERANN WARNED SOMEONE!!!!!!!!!!!!!!!!!!!!!!")
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelled', ephemeral=True)
        self.value = False
        self.stop()

async def add_warn(interaction : discord.Interaction, user : discord.Member, reason : str, guild):
    db = sqlite3.connect("DB.sqlite")
    cur = db.cursor()

    if interaction.user.id == 661230793028403202:
        view = ConfirmVerannWantsToDoThis()
        await interaction.response.send_message("It seems that you are Verann, are you SURE you wanna do this?", view=view)

    cur.execute("""
        INSERT INTO warn(
            user,
            reason,
            time,
            guild
        ) VALUES (?,?,?,?)
    """, (user.id, reason, datetime.datetime.now(), guild))
    db.commit()

async def remove_warn(interaction : discord.Interaction, user : discord.Member, guild):
    db = sqlite3.connect("DB.sqlite")
    cur = db.cursor()
    cur.execute(
        """
            SELECT reason FROM warn WHERE user = ? AND guild = ?
        """, (user.id, guild)
    )
    db.commit()
    data = cur.fetchone()
    if data:
        cur.execute(
            """
                DELETE FROM warn WHERE user = ? AND guild = ?
            """, (user.id, guild)
        )
        db.commit()
        await interaction.response.send_message("ALL the warns have been removed!")
    else:
        await interaction.response.send_message("This user doesn't have any warns.")

class Moderation(commands.Cog):
    """
    Moderation commands.
    Commands:
        /warn: warns a user.
        /resetwarns: resets ALL the warns from a member on the server.
        /warns: shows the warn of a user.
        /announcement: makes an announcement.
    """
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="warn", description="Warns a user.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction : discord.Interaction, user : discord.Member, reason : str = "No reasons...At all..."):
        await add_warn(interaction, user, reason, interaction.guild_id)
        await interaction.response.send_message(f"Warned {user} for: {reason}")

    @warn.error
    async def warn_er(self, interaction : discord.Interaction, error):
        await interaction.response.send_message("You need to be able to kick members to execute this command.", ephemeral=True)
    
    @app_commands.command(name="resetwarns", description="Removes ALL the warns from a user.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def resetwarns(self, interaction : discord.Interaction, user : discord.Member):
        await remove_warn(interaction, user, interaction.guild_id)
    
    @resetwarns.error
    async def rswarn_er(self, interaction : discord.Interaction, error):
        await interaction.response.send_message("You need to be able to kick members to execute this command.", ephemeral=True)

    @app_commands.command(name="warns", description="Shows all the warns of a user.")
    async def warns(self, interaction : discord.Interaction, user : discord.Member):
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        cur.execute(
            """
                SELECT * FROM warn WHERE user = ? AND guild = ?
            """, (user.id, interaction.guild_id)
        )
        data = cur.fetchall()
        embed = discord.Embed(
            title=f"Warns for {user}",
            colour = 0x36393F,
            timestamp=datetime.now()
        )
        for i in data:
            embed.add_field(name="Warn reason:", value=i[1])
            embed.add_field(name="Time:", value=i[2])
        
        await interaction.response.send_message(embed=embed)

    
    @app_commands.command(name="announcement")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def _announcement(
        self, 
        interaction : discord.Interaction,
        channel : discord.TextChannel,
        title : str,
        description : str,
        color : Optional[int],
        ping : Optional[discord.Role]):
        """
        Sends an announcement, with an embed wich has the color of your choice
  
        Args: 
            interaction (discord.Interaction): The interaction that invokes this coroutine 
            channel (discord.TextChannel): The channel where we want to send this announcement 
            title (str): The title of the announcement (limit: 256 characters)
            description (str): The description of the announcement (limit: 4096 characters)
            color: The color of the embed
            ping (discord.Role): The role you want to ping
        """
        embed = discord.Embed(
            title = title,
            description = description,
            color=color if color is not None else 0x000000
        )
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        channel = interaction.guild.get_channel(channel.id)
        await channel.send("Ping: " + ping.mention if ping is not None else "No pings.", embed=embed)
        await interaction.response.send_message("Announcement send!", ephemeral=True)


async def setup(bot : commands.Bot):
    await bot.add_cog(Moderation(bot))