import discord
from discord.ext import commands
from discord import Embed
import json

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        configured_ip = value['configured_ip']


class link(commands.Cog):
    def __init__(self, clientValue):
        self.client = clientValue

    @commands.Cog.listener()
    async def on_ready(self):
        print('Linking module has successfully been initialized.')

    @commands.command()
    async def test(self, ctx, *, token=None):
        if not token:
            return await ctx.send("You must enter a token.")
        payload = {'token': token, 'userId': ctx.author}
        Status = Embed(colour=0xAE0808)
        Status.add_field(name="CartelPvP | Linking", value="Successfully linked your account to SearchForMe",
                         inline=False)
        await ctx.send(embed=Status)


def setup(client):
    client.add_cog(link(client))
