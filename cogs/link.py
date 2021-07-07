import discord
from discord.ext import commands
from discord import Embed
import json

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        test = 'test'


class link(commands.Cog):
    def __init__(self, clientValue):
        self.client = clientValue

    @commands.Cog.listener()
    async def on_ready(self):
        print('Linking module has successfully been initialized.')

    @commands.command()
    async def link(self, ctx, *, token):
        await ctx.send("test")


def setup(client):
    client.add_cog(link(client))
