import json

import discord
from discord.ext import commands

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        announce_id = value['announcements_id']


class Announcement(commands.Cog):
    def __init__(self, clientValue):
        self.client = clientValue

    @commands.Cog.listener()
    async def on_ready(self):
        print('Announcement module has successfully been initialized.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def announcetitle(self, ctx, *, title):
        global annctitle
        annctitle = title
        await ctx.send("Announcement Title Set!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def announcemessage(self, ctx, *, message):
        global anncmessage
        anncmessage = message
        await ctx.send("Announcement Message Set!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def announce(self, ctx):
        channel = self.client.get_channel(int(announce_id))
        embedVar = discord.Embed(title=f"**{annctitle}**", description=f"{anncmessage}",
                                 color=0xAE0808)
        await channel.send(embed=embedVar)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def serverannounce(self, ctx):
        for channel in ctx.guild.text_channels:
            embedVar = discord.Embed(title=f"**{annctitle}**", description=f"{anncmessage}",
                                     color=0xAE0808)
            await channel.send(embed=embedVar)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def previewannounce(self, ctx):
        embedVar = discord.Embed(title=f"**{annctitle}**", description=f"{anncmessage}",
                                 colour=0xAE0808)
        await ctx.send(embed=embedVar)


def setup(client):
    client.add_cog(Announcement(client))
