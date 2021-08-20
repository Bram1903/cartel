import datetime
import json
from asyncio import sleep

import discord
from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


# This prevents staff members from being punished
class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages
        if not permission:
            return argument
        else:
            await ctx.send("You cannot punish other staff members.")
            raise commands.BadArgument(
                "You cannot punish other staff members")


class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kick module has successfully been initialized.')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: Sinner = None, *, reason=None):
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if not user:
            await ctx.message.delete()
            msg = await ctx.send("You must specify a user.")
            await sleep(4.7)
            await msg.delete()
            return
        if not reason:
            await ctx.message.delete()
            msg2 = await ctx.send("You must specify a reason.")
            await sleep(4.7)
            await msg2.delete()
            return
        userDM = Embed(title="CartelPvP | Moderation",
                       description=f"You have been kicked from CartelPvP",
                       colour=0xAE0808)

        userDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        userDM.add_field(name="**Kicked by**", value=f"{ctx.author.display_name}", inline=True)
        userDM.add_field(name="**Reason**", value=f"{reason}", inline=True)

        timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
        embed = Embed(description=f"Member ID: {user.id}", colour=0xAE0808)
        embed.set_author(name='Member Kicked',
                         icon_url='https://i.imgur.com/SR9wWm9.png')
        embed.add_field(name="Kicked", value=f"{user.mention}",
                        inline=False)
        embed.add_field(name="Kicked by", value=f"{ctx.author.mention}",
                        inline=False)
        embed.add_field(name="Reason", value=f"{reason}",
                        inline=False)
        embed.set_footer(text=f"Kicked on {timestamp}"
                         , icon_url=user.avatar_url)
        channel_embed = Embed(colour=0xAE0808)
        channel_embed.set_author(name=f'{user.display_name} has been kicked.',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
        if user:
            try:
                await user.send(embed=userDM)
            except discord.Forbidden:
                pass
        try:
            await user.kick(reason=reason)
            logs = self.client.get_channel(int(logging_channel))
            msg = await ctx.channel.send(embed=channel_embed)
            await logs.send(embed=embed)
            await ctx.message.delete()
            await sleep(4.7)
            await msg.delete()
        except discord.Forbidden:
            return await ctx.send("Are you trying to kick someone higher than the bot")


def setup(client):
    client.add_cog(Kick(client))
