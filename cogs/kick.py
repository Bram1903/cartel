import discord
from discord.ext import commands
from discord import Embed

class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kick module has succesfully been loaded.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason="Not specified"):
        await member.kick(reason=reason)
        embedkick = Embed(title="CartelPvP | Moderation",
                        description="You have been kicked from CartelPvP.",
                        colour=0xAE0808)
        embedkick.set_thumbnail(url=ctx.author.avatar_url)
        embedkick.add_field(name="Kicked by", value=f"{ctx.author}", inline=True)
        embedkick.add_field(name="Reason", value=f"{reason}", inline=True)
        await ctx.send(embed=embedkick)
        

def setup (client):
    client.add_cog(Kick(client))