import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class Echo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Echo module has successfully been initialized.')

    @commands.command(aliases=['mimic', 'paste', 'say'])
    @has_permissions(administrator=True)
    async def echo(self, ctx, *, sentence=None):
        if not sentence:
            return await ctx.send("You must provide a word or sentence.")
        fileName = "command_logs.txt"
        with open(fileName, "w") as file:
            async for msg in ctx.channel.history(limit=1):
                file.write(f"{msg.created_at} - {msg.author.display_name}: has executed the echo command. Text: {sentence}\n")
        await ctx.send(await commands.clean_content().convert(ctx=ctx, argument=sentence))
        await ctx.message.delete()


def setup(client):
    client.add_cog(Echo(client))
