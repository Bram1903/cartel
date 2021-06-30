import discord
from discord.ext import commands
from discord import Embed


class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kick module has succesfully been initialized.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Not specified"):
        userdm = Embed(title="CartelPvP | Moderation",
                       description=f"You have been kicked from CartelPvP",
                       colour=0xAE0808)

        userdm.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        userdm.add_field(name="Kicked by", value=f"{ctx.author}", inline=True)
        userdm.add_field(name="Reason", value=f"{reason}", inline=True)

        if member:
            try:
                await member.send(embed=userdm)
            except discord.Forbidden:
                pass

        await member.kick(reason=reason)
        embedkick = Embed(title="CartelPvP | Moderation",
                          description=f"{member} has been kicked from CartelPvP.",
                          colour=0xAE0808)
        embedkick.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        embedkick.add_field(name="Kicked by", value=f"{ctx.author}", inline=True)
        embedkick.add_field(name="Reason", value=f"{reason}", inline=True)
        await ctx.send(embed=embedkick)


def setup(client):
    client.add_cog(Kick(client))
