import discord
import requests
from discord.ext import commands
from discord import Embed
import json

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        configured_ip = value['configured_ip']


class Link(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Linking module has successfully been initialized.')

    @commands.command()
    async def link(self, ctx, *, token):
        payload = {'token': token, 'userId': ctx.author.id}
        r = requests.post(configured_ip, json=payload)
        if r.status_code == 200:
            embed = Embed(colour=0x38ff6d)
            embed.add_field(name="CartelPvP | Linking", value="Successfully linked your account to " + r.text + ".",
                            inline=False)
            await ctx.send(embed=embed)
        else:
            embed = Embed(colour=0xAE0808)
            embed.add_field(name="CartelPvP | Linking", value="Failed to find that token.",
                            inline=False)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Link(client))
