import discord
from discord.ui import Modal, TextInput, RoleSelect
from discord import app_commands
from discord.ext import commands
import sqlite3
import traceback


class RoleReact(commands.Cog):
    """
    Reaction roles.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = self.bot.get_user(payload.user_id)
        emoji = str(self.bot.get_emoji(payload.emoji))
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        result = cur.execute("SELECT role FROM rolereact WHERE msg_id = ? AND emoji = ?",(str(message), emoji))
        r = result.fetchall()
        for entry in r:
            message_id = payload.message_id
            if message_id == entry[1]:
                guild = self.bot.get_guild(payload.guild_id)
            if str(payload.emoji) == entry[2]:
                role = discord.utils.get(guild.roles, id=entry[0])
                await member.add_roles(role)
                await message.remove_reaction(member, emoji)



    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def rolereact(
        self,
        interaction : discord.Interaction,
        channel : discord.TextChannel,
        role : discord.Role,
        message_id : str,
        emoji : str):
        """
        Setups reaction roles.

        Args:
            interaction (discord.Interaction): The interaction that invokes this coroutine 
            channel (discord.TextChannel): The channel where the message is.
            role (discord.Role): The role to add/remove.
            message_id (str): The ID of the message of the author.
            emoji (str): The emoji to add (structure: <:emoji_name:emoji_id>).
        """

        db = sqlite3.connect('DB.sqlite')
        cur = db.cursor()
        cur.execute("""
            INSERT INTO rolereact(role, msg_id, emoji) VALUES(?,?,?)
        """, (role.id, int(message_id), emoji))
        db.commit()
        message = await channel.fetch_message(int(message_id))
        await message.add_reaction(str(emoji))
        await interaction.response.send_message("Everything is setup!")


async def setup(bot):
    await bot.add_cog(RoleReact(bot))