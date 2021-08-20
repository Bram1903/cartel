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
class Sinner(commands.Converter):  # Creates the class
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages  # Given permission in this cage manage messages.
        if not permission:  # Checks if the member doesn't have manage messages permissions.
            return argument  # When the member doesn't have the permission it will go on with the argument (command).
        else:  # Else if the member does have manage messages as permission it will give a return.
            await ctx.send("You cannot punish other staff members.")  # Sends a message in the channel of the command
            # given.
            raise commands.BadArgument(  # Raises an error otherwise the console gets flood and mister pizza in your ass
                # gets angry
                "You cannot punish other staff members")


class Redeemed(commands.Converter):  # Creates the class
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)  # Basically the given command.
        muted = discord.utils.get(ctx.guild.roles, name="Muted")  # Defines the muted role.
        if muted in argument.roles:  # Checks for the muted role.
            return argument  # Goes back to the argument (command)
        else:
            raise commands.BadArgument("The user was not muted.")


async def mute(ctx, user):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        try:
            muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
            for channel in ctx.guild.channels:  # For loop to get all channels within the guild.
                await channel.set_permissions(muted, send_messages=False,
                                              read_message_history=True,
                                              read_messages=True)
        except discord.Forbidden:  # Basic discord handler for not having the permission.
            return await ctx.send("I have no permissions to make a muted role")
        await user.add_roles(muted)
    else:
        await user.add_roles(role)


class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mute module has successfully been initialized.')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: Sinner = None, *, reason=None):
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
        MutedDM = Embed(title="CartelPvP | Moderation",
                        description=f"You have been muted in CartelPvP",
                        colour=0xAE0808)
        MutedDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        MutedDM.add_field(name="**Muted by**", value=f"{ctx.author}", inline=True)
        MutedDM.add_field(name="**Reason**", value=f"{reason}", inline=True)

        timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
        embed = Embed(description=f"Member ID: {user.id}", colour=0xAE0808)
        embed.set_author(name='Member Muted',
                         icon_url='https://i.imgur.com/SR9wWm9.png')
        embed.add_field(name="Muted", value=f"{user.mention}",
                        inline=False)
        embed.add_field(name="Muted by", value=f"{ctx.author.mention}",
                        inline=False)
        embed.add_field(name="Reason", value=f"{reason}",
                        inline=False)
        embed.set_footer(text=f"Muted on {timestamp}"
                         , icon_url=user.avatar_url)
        channel_embed = Embed(colour=0xAE0808)
        channel_embed.set_author(name=f'{user.display_name} has been muted.',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
        if user:
            await mute(ctx, user, reason)
        else:
            return
        try:
            await user.send(embed=MutedDM)
        except discord.Forbidden:
            pass
        try:
            logs = self.client.get_channel(int(logging_channel))
            msg = await ctx.channel.send(embed=channel_embed)
            await logs.send(embed=embed)
            await ctx.message.delete()
            await sleep(4.7)
            await msg.delete()
        except discord.Forbidden:
            return await ctx.send("Are you trying to kick someone higher than the bot")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: Redeemed = None, *, reason=None):
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
        MutedDM = Embed(title="CartelPvP | Moderation",
                        description=f"You have been unmuted in CartelPvP",
                        colour=0xAE0808)
        MutedDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        MutedDM.add_field(name="Unmuted by", value=f"{ctx.author}", inline=True)
        MutedDM.add_field(name="Reason", value=f"{reason}", inline=True)

        timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
        embed = Embed(description=f"Member ID: {user.id}", colour=0x57F287)
        embed.set_author(name='Member Unmuted',
                         icon_url='https://i.imgur.com/SR9wWm9.png')
        embed.add_field(name="Unmuted", value=f"{user.mention}",
                        inline=False)
        embed.add_field(name="Unmuted by", value=f"{ctx.author.mention}",
                        inline=False)
        embed.add_field(name="Reason", value=f"{reason}",
                        inline=False)
        embed.set_footer(text=f"Unmuted on {timestamp}"
                         , icon_url=user.avatar_url)
        channel_embed = Embed(colour=0xAE0808)
        channel_embed.set_author(name=f'{user.display_name} has been unmuted.',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
        if user:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        else:
            return
        try:
            await user.send(embed=MutedDM)
        except discord.Forbidden:
            pass
        try:
            logs = self.client.get_channel(int(logging_channel))
            msg = await ctx.channel.send(embed=channel_embed)
            await logs.send(embed=embed)
            await ctx.message.delete()
            await sleep(4.7)
            await msg.delete()
        except discord.Forbidden:
            return await ctx.send("Are you trying to unmute someone higher than the bot")


def setup(client):
    client.add_cog(Mute(client))
