import discord
import requests
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
    async def link(self, ctx, *, token):
        payload = {'token': token, 'userId': ctx.author}
        r = requests.post(configured_ip, data=payload)

    @commands.command()
    async def test(self, ctx, *, token):
        payload = {'token': token, 'userId': ctx.author}
        Status = Embed(title="CartelPvP | Linking",
                       description=f"Trying to link you accounts",
                       colour=0xAE0808)

        Status.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        Status.add_field(name="User", value=f"{ctx.author}", inline=True)
        Status.add_field(name="Token", value=f"{token}", inline=True)
        await ctx.send(embed=Status)


def setup(client):
    client.add_cog(link(client))
