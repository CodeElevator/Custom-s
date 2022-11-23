from typing import Literal, Optional, Union
import discord
from discord.ui import View, button, Button
from discord import app_commands, ButtonStyle, Emoji, PartialEmoji
from discord.ext import commands
import sqlite3
import traceback

class Role(View):
    def __init__(self, *, timeout: Optional[float] = 5):
        super().__init__(timeout=timeout)

    db = sqlite3.connect('DB.sqlite')
    cur = db.cursor()
    r = cur.execute("SELECT * FROM rolereact")

    result = r.fetchall()
    for res in result:
        res = res
    if res[3] == "blurple":
        btnstyle = ButtonStyle.primary
    elif res[3] == "green":
        btnstyle = ButtonStyle.success
    elif res[3] == "grey":
        btnstyle = ButtonStyle.secondary
    elif res[3] == "red":
        btnstyle = ButtonStyle.danger
    
    label = res[2]
    btnemote = res[4]
    
    @button(label=label, style=btnstyle, emoji=btnemote)
    async def rolebtn(self, interaction : discord.Interaction, button : discord.Button):
        user = interaction.user
        db = sqlite3.connect('DB.sqlite')
        cur = db.cursor()
        r = cur.execute("SELECT * FROM rolereact")

        result = r.fetchall()
        for res in result:
            res = res
        if res[0] in [i.id for i in user.roles]:
            role = user.guild.get_role(res[0])
            await user.remove_roles(res[0], reason="Reaction roles")
            await interaction.response.send_message(f"Successfully removed role <@&{res[0]}>", ephemeral=True)
        else:
            role = user.guild.get_role(res[0])
            await user.add_roles(role, reason="Reaction roles")
            await interaction.response.send_message(f"Successfully added role <@&{res[0]}>", ephemeral=True)


class RoleReact(commands.Cog):
    """
    Reaction roles.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def rolereact(
        self,
        interaction : discord.Interaction,
        role : discord.Role,
        message : str,
        button : str,
        color : Literal['blurple', 'green', 'grey', 'red'],
        emoji : str):
        """
        Setups reaction roles.

        Args:
            interaction (discord.Interaction): The interaction that invokes this coroutine 
            role (discord.Role): The role to add/remove.
            message (str): The text of the message.
            button (str): The text of the button.
            color (Literal): The color of the button.
            emoji (str): The emoji of the button (structure: <:emoji_name:emoji_id>).
        """

        db = sqlite3.connect('DB.sqlite')
        cur = db.cursor()
        r = cur.execute("SELECT * FROM rolereact")

        cur.execute("INSERT INTO rolereact(role, txt, btn_txt, btn_color, emoji) VALUES(?,?,?,?,?)", (role.id, message, button, color, emoji))
        db.commit()
        view = Role()
        await interaction.response.send_message(message, view=view)


async def setup(bot):
    await bot.add_cog(RoleReact(bot))