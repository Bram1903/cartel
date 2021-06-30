import discord
from discord.ext import commands
from discord import Embed


class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kick module has successfully been initialized.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Not specified"):
        await ctx.message.delete()
        dmUser = Embed(title="CartelPvP | Moderation",
                       description=f"You have been kicked from CartelPvP",
                       colour=0xAE0808)

        dmUser.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        dmUser.add_field(name="Kicked by", value=f"{ctx.author}", inline=True)
        dmUser.add_field(name="Reason", value=f"{reason}", inline=True)

        if member:
            try:
                await member.send(embed=dmUser)
            except discord.Forbidden:
                pass

        await member.kick(reason=reason)
        embedKick = Embed(title="CartelPvP | Moderation",
                          description=f"{member} has been kicked from CartelPvP.",
                          colour=0xAE0808)
        embedKick.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        embedKick.add_field(name="Kicked by", value=f"{ctx.author}", inline=True)
        embedKick.add_field(name="Reason", value=f"{reason}", inline=True)
        await ctx.send(embed=embedKick)


def setup(client):
    client.add_cog(Kick(client))
