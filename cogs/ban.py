import discord
from discord import Embed
from discord.ext import commands
import datetime
import json


with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


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


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ban module has successfully been initialized.')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Sinner = None, reason="Not specified"):
        if not user:
            return await ctx.send("You must specify a user")
        mod = ctx.author
        userDM = Embed(title="CartelPvP | Moderation",
                       description=f"You have been banned from CartelPvP",
                       colour=0xAE0808)
        userDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        userDM.add_field(name="Banned by", value=f"{ctx.author}", inline=True)
        userDM.add_field(name="Reason", value=f"{reason}", inline=True)

        timestamp = datetime.datetime.utcnow()
        embed = Embed(description=f"Member ID: {user.id}", colour=0xAE0808)
        embed.set_author(name='Member banned',
                         icon_url='https://i.imgur.com/SR9wWm9.png')
        embed.add_field(name="Banned", value=f"{user.mention}",
                        inline=False)
        embed.add_field(name="Banned by", value=f"{ctx.author.mention}",
                        inline=False)
        embed.add_field(name="Reason", value=f"{reason}",
                        inline=False)
        embed.set_footer(text=f"Banned on {timestamp}"
                         , icon_url=user.avatar_url)
        channel_embed = Embed(colour=0xAE0808)
        channel_embed.set_author(name=f'{user.display_name} has been banned.',
                           icon_url='https://i.imgur.com/SR9wWm9.png')
        if user:
            try:
                logs = self.client.get_channel(int(logging_channel))
                await ctx.channel.send(embed=channel_embed)
                await user.send(embed=userDM)
                await logs.send(embed=embed)
            except discord.Forbidden:
                pass
        try:
            await user.ban(reason=reason)
        except discord.Forbidden:
            return await ctx.send("Are you trying to ban someone higher than the bot")


def setup(client):
    client.add_cog(Ban(client))
