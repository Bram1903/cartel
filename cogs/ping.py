from discord.ext import commands
from discord import Embed


class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ping module has successfully been initialized.')

    @commands.command()
    async def ping(self, ctx):
        PingEmbed = Embed(title="CartePvP | Info",
                      description="Ping request",
                      colour=0xAE0808)
        PingEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        PingEmbed.add_field(name="Requested by", value=f"{ctx.author}", inline=True)
        PingEmbed.add_field(name="Ping", value=f"{round(self.client.latency * 1000)}ms", inline=True)
        await ctx.send(embed=PingEmbed)


def setup(client):
    client.add_cog(Ping(client))
