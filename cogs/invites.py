import json
from asyncio import sleep

import discord
from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        botChannel = value['bot-commands']
        admins = value['admins']


class Invites(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Invite module has successfully been initialized.')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invites(self, ctx, user: discord.Member = None):
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if not user:  # Checks if a member is given.
            user = ctx.message.author  # If member is not given set the ctx.author as member.
        total_invites = 0
        for i in await ctx.guild.invites():
            if i.inviter == user:
                total_invites += i.uses
        if ctx.author.id not in admins:
            channel = self.client.get_channel(int(botChannel))
            if ctx.channel == channel:
                await ctx.send(
                    f"{user} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")
            else:
                channel_embed = Embed(colour=0xAE0808)
                channel_embed.set_author(name=f'Wrong channel',
                                         icon_url='https://i.imgur.com/SR9wWm9.png')
                channel_embed.add_field(name="Channel", value=channel.mention)
                msg = await ctx.send(embed=channel_embed)
                await ctx.message.delete()
                await sleep(4.7)
                await msg.delete()
        else:
            await ctx.send(
                f"{user} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")


def setup(client):
    client.add_cog(Invites(client))
