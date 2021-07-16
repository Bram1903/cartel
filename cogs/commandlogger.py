import time

import discord
from discord.ext import commands
from datetime import datetime
from discord import Embed


class CommandLogger(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Command logger has successfully been initialized.')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            fileName = "commandlogger.txt"
            with open(fileName, "a") as file:
                milliseconds = int(time.time() * 1000)
                file.write(f"{milliseconds} § discord_main § {ctx.channel.id} ({ctx.channel}), "
                           f"{ctx.author.id} ({ctx.author}) {ctx.message.content}\n")
        except Exception as e:
            print(e)


def setup(client):
    client.add_cog(CommandLogger(client))
