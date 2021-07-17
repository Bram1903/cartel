import discord
from discord.ext import commands
from discord import Embed


class Invites(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Help module has successfully been initialized.')

    @commands.group(name='help', invoke_without_command=True)
    async def help(self, ctx):
        await ctx.send("Base command")

    @help.command(name='info')
    async def info_subcommand(self, ctx):
        await ctx.send("Info commands")


def setup(client):
    client.add_cog(Invites(client))
