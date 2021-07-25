import time

from discord import Embed
from discord.ext import commands


class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ping module has successfully been initialized.')

    @commands.command()
    async def ping(self, ctx):
        before = time.monotonic()
        before_ws = int(round(self.client.latency*1000, 1))
        message = await ctx.send("Pinging...")
        ping = (time.monotonic()-before)*1000
        PingEmbed = Embed(title="CartePvP | Info",
                          description=f"<a:speedtest:868948472487870514> **Websocket**: {before_ws}ms\n"
                                      f"<a:loading:868948541714862090> **REST**: {int(ping)}ms\n",
                          colour=0xAE0808)
        PingEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        PingEmbed.set_footer(text=f"Requested by: {ctx.author}")
        await message.edit(content="", embed=PingEmbed)


def setup(client):
    client.add_cog(Ping(client))
