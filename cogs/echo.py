import json

from discord.ext import commands
from discord.ext.commands import has_permissions


class Echo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Echo module has successfully been initialized.')

    @commands.command(aliases=['mimic', 'paste', 'say'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(administrator=True)
    async def echo(self, ctx, *, sentence=None):
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if not sentence:
            return await ctx.reply("You must provide a word or sentence.", mention_author=False)
        await ctx.send(await commands.clean_content().convert(ctx=ctx, argument=sentence))
        await ctx.message.delete()


def setup(client):
    client.add_cog(Echo(client))
