from discord import Embed
from discord.ext import commands
import psutil


class Usage(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Usage module has successfully been initialized.')

    @commands.command()
    async def usage(self, ctx):
        cpu = psutil.cpu_percent()
        memoryUsed = psutil.virtual_memory().percent
        memoryAvailable = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        usage = Embed(title="CartelPvP | System",
                      description="System usage",
                      colour=0xAE0808)
        usage.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        usage.add_field(name="CPU usage", value=f"{cpu}%", inline=False)
        usage.add_field(name="Memory usage %", value=f"{memoryUsed}%", inline=False)
        usage.add_field(name="Memory available", value=f"{memoryAvailable}%", inline=False)
        await ctx.send(embed=usage)


def setup(client):
    client.add_cog(Usage(client))
