import json
import time
from asyncio import sleep

from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        botChannel = value['bot-commands']
        admins = value['admins']


class Latency(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Latency module has successfully been initialized.')

    @commands.command(aliases=['ping'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def latency(self, ctx):
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if ctx.author.id not in admins:
            channel = self.client.get_channel(int(botChannel))
            if ctx.channel == channel:
                before = time.monotonic()
                before_ws = int(round(self.client.latency * 1000, 1))
                message = await ctx.send("Pinging...")
                ping = (time.monotonic() - before) * 1000
                PingEmbed = Embed(title="CartelPvP | Info",
                                  description=f"<a:speedtest:868948303218352178> **Websocket**: {before_ws}ms\n"
                                              f"<a:loading:868948800201453569> **Rest**: {int(ping)}ms\n",
                                  colour=0xAE0808)
                PingEmbed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
                PingEmbed.set_footer(text=f"Requested by: {ctx.author}")
                await message.edit(content="", embed=PingEmbed)
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
            before = time.monotonic()
            before_ws = int(round(self.client.latency * 1000, 1))
            message = await ctx.send("Pinging...")
            ping = (time.monotonic() - before) * 1000
            PingEmbed = Embed(title="CartelPvP | Info",
                              description=f"<a:speedtest:868948303218352178> **Websocket**: {before_ws}ms\n"
                                          f"<a:loading:868948800201453569> **Rest**: {int(ping)}ms\n",
                              colour=0xAE0808)
            PingEmbed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
            PingEmbed.set_footer(text=f"Requested by: {ctx.author}")
            await message.edit(content="", embed=PingEmbed)


def setup(client):
    client.add_cog(Latency(client))
