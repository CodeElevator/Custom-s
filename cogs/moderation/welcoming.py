import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View
import sqlite3
from easy_pil import load_image_async, Font, Editor

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
        if result is None:
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
        if result is None:
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
    
    @commands.Cog.listener()
    async def on_member_join(self, member :  discord.Member):
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        ch = cur.execute(f"SELECT ch_id FROM welcome WHERE guild_id = {member.guild.id}")
        result = ch.fetchone()
        if result is None:
            return
        msg = cur.execute(f"SELECT msg FROM welcome WHERE guild_id = {member.guild.id}")
        res = msg.fetchone()
        member_list = len(list(member.guild.members))
        mention = member.mention
        guild = member.guild.name
        generated = str(res[0]).format(member_list=member_list, mention=mention, server=guild)
        channel = self.bot.get_channel(result[0])
        img = cur.execute(f"SELECT img FROM welcome WHERE guild_id = {member.guild.id}")
        result2 = img.fetchone()
        if result2 is None:
            return
        bg = Editor(str(result2[0]))
        profile_picture = await load_image_async(member.avatar.url)
        pp_circle = Editor(profile_picture).resize((150,150)).circle_image()
        poppins = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=20, variant="light")
        bg.paste(pp_circle, (325,90))
        bg.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)
        bg.text((400, 260), f"WELCOME TO {guild}", color="white", font=poppins, align="center")
        bg.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")
        file = discord.File(fp=bg.image_bytes, filename="welcome.jpg")
        await channel.send(generated, file=file)

    welcoming = app_commands.Group(name="welcome", description="Setups welcoming", guild_only=True, nsfw=False)

    @welcoming.command(name="channel")
    async def channel(self, interaction : discord.Interaction, channel : discord.TextChannel):
        """
        Setups Welcome message.

        Args:
            interaction (discord.Interaction): The interaction that invokes this coroutine
            channel (discord.TextChannel): The channel where welcome message will be sent.
        """
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT ch_id FROM welcome WHERE guild_id = {interaction.guild_id}")
        result = cur.fetchone()
        if result is None:
            cur.execute("INSERT INTO welcome(guild_id, ch_id) VALUES(?,?)", (interaction.guild_id, channel.id))
            await interaction.response.send_message(f"Channel has been set to {channel.mention}")
            db.commit()
        else:
            cur.execute("UPDATE welcome SET ch_id = ? WHERE guild_id = ?", (channel.id, interaction.guild_id))
            await interaction.response.send_message(f"Channel has been updated to {channel.mention}")
            db.commit()

    @welcoming.command(name="message")
    async def message(self, interaction : discord.Interaction, message : str):
        """
        Setups Welcome message.

        Args:
            interaction (discord.Interaction): The interaction that invokes this coroutine
            message (str): Ex: Welcome {mention} to {server} ! You are the {member_list} member!
        """
        db = sqlite3.connect("DB.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT msg FROM welcome WHERE guild_id = {interaction.guild_id}")
        result = cur.fetchone()
        if result is None:
            cur.execute("INSERT INTO welcome(guild_id, msg) VALUES(?,?)", (message, interaction.guild_id))
            db.commit()
            await interaction.response.send_message(f"Message has been set!")
            
        else:
            cur.execute("UPDATE welcome SET msg = ? WHERE guild_id = ?", (message, interaction.guild_id))
            db.commit()
            await interaction.response.send_message(f"Message has been updated!")
            
    
    @welcoming.command(name="image")
    async def image(self, interaction : discord.Interaction):
        """
        Setups Welcome image (optional).

        Args:
            interaction (discord.Interaction): The interaction that invokes this coroutine
        """
        view = ConfirmThinguy()
        await interaction.response.send_message("Wich image do you prefer?", files=[discord.File("pic1.jpg"), discord.File("pic2.jpg")], view=view)
    

async def setup(bot):
    await bot.add_cog(Welcoming(bot))