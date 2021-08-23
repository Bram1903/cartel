import json
from asyncio import sleep

import discord
from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        botChannel = value['bot-commands']
        admins = value['admins']


class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Avatar module has successfully been initialized.')

    @commands.command(aliases=["av", "pfp"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member = None):
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if not member:
            member = ctx.message.author

        em = Embed(title=str(member), color=0xAE0808)
        em.set_image(url=member.avatar_url)
        if ctx.author.id not in admins:
            channel = self.client.get_channel(int(botChannel))
            if ctx.channel == channel:
                await ctx.reply(embed=em, mention_author=False)
            else:
                channel_embed = Embed(colour=0xAE0808)
                channel_embed.set_author(name=f'Wrong channel',
                                         icon_url='https://i.imgur.com/SR9wWm9.png')
                channel_embed.add_field(name="Channel", value=channel.mention)
                msg = await ctx.send(embed=channel_embed)
                await ctx.message.delete()
                await sleep(4.7)
                await msg.delete()
        else:
            await ctx.reply(embed=em, mention_author=False)


def setup(client):
    client.add_cog(Avatar(client))
