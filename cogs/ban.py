import discord
from discord.ext import commands
from discord import Embed

class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ban module is ready.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embedban = Embed(title="CartelPvP | Moderation",
                        description="You have been banned from CartelPvP.",
                        colour=0xAE0808)
        embedban.set_thumbnail(url=ctx.author.avatar_url)
        embedban.add_field(name="Banned by", value=f"{ctx.author}", inline=True)
        embedban.add_field(name="Reason", value=f"{reason}", inline=True)
        await ctx.send(embed=embedban)


def setup(client):
    client.add_cog(Ban(client))