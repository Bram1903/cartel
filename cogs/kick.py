import discord
from discord.ext import commands

class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kick is ready!')

    @commands.command()
    async def pong(self, ctx):
        await ctx.send('Ping!')




def setup (client):
    client.add_cog(Kick(client))



