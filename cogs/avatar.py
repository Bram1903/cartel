import time

import discord
from discord.ext import commands


class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.5)
        print('Avatar module has successfully been initialized.')

    @commands.command(aliases=["av", "pfp"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.message.author

        message = discord.Embed(title=str(member), color=0xAE0808)
        message.set_image(url=member.avatar_url)

        await ctx.send(embed=message)


def setup(client):
    client.add_cog(Avatar(client))
