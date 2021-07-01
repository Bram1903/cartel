from discord.ext import commands
from discord import Embed


class Slowmode(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Slowmode module has successfully been initialized.')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, amount):
        await ctx.message.delete()
        await ctx.channel.edit(slowmode_delay=int(amount))
        SlowEmbed = Embed(title="CartePvP | Moderation",
                          description="Slowmode has been activated",
                          colour=0xAE0808)
        SlowEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        SlowEmbed.add_field(name="Delayed by", value=f"{ctx.author}", inline=True)
        SlowEmbed.add_field(name="Delay", value=f"{int(amount)} seconds", inline=True)
        await ctx.send(embed=SlowEmbed)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def unslow(self, ctx):
        await ctx.message.delete()
        await ctx.channel.edit(slowmode_delay=0)
        UnSlowEmbed = Embed(title="CartePvP | Moderation",
                          description="Slowmode has been deactivated",
                          colour=0xAE0808)
        UnSlowEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        UnSlowEmbed.add_field(name="Disabled by", value=f"{ctx.author}", inline=True)
        UnSlowEmbed.add_field(name="Delay", value="Disabled", inline=True)
        await ctx.send(embed=UnSlowEmbed)


def setup(client):
    client.add_cog(Slowmode(client))
