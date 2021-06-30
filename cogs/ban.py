import discord
from discord.ext import commands
from discord import Embed


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ban module has succesfully been initialized.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        userdm = Embed(title="CartelPvP | Moderation",
                       description=f"You have been banned from CartelPvP",
                       colour=0xAE0808)

        userdm.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        userdm.add_field(name="Banned by", value=f"{ctx.author}", inline=True)
        userdm.add_field(name="Reason", value=f"{reason}", inline=True)

        if member:
            try:
                await member.send(embed=userdm)
            except discord.Forbidden:
                pass
        
        await member.ban(reason=reason)
        embedban = Embed(title="CartelPvP | Moderation",
                        description=f"{member} has been banned from CartelPvP.",
                        colour=0xAE0808)
        embedban.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        embedban.add_field(name="Banned by", value=f"{ctx.author}", inline=True)
        embedban.add_field(name="Reason", value=f"{reason}", inline=True)
        await ctx.send(embed=embedban)


def setup(client):
    client.add_cog(Ban(client))
