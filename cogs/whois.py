import discord
from discord import Embed
from discord.ext import commands


# Imports


class Whois(commands.Cog):
    def __init__(self, client):
        self.client = client  # Set up parts of the cog.

    @commands.Cog.listener()
    async def on_ready(self):
        print('Whois module has successfully been initialized.')  # Basic on_ready event, but designed to work in a cog.

    @commands.command(aliases=['ui', 'userinfo'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def whois(self, ctx, user: discord.Member = None):
        if not user:  # Checks if a member is given.
            user = ctx.message.author  # If member is not given set the ctx.author as member.
        em = Embed(color=0xAE0808)
        em.set_author(name='User Info', icon_url='https://i.imgur.com/FgkMDGn.png')
        em.set_thumbnail(url=ctx.author.avatar_url)
        fields = [("ID", f"`{user.id}`", False),
                  ("Bot", user.bot, True),
                  ("Top Role", user.top_role.mention, True),
                  ("Status", str(user.status).title(), True),
                  ("Created At", user.created_at.strftime("%d/%m/%Y | %H:%M:%S"), True),
                  ("Joined At", user.joined_at.strftime("%d/%m/%Y | %H:%M:%S"), True)]

        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Whois(client))  # Other part of setting up the cog.
