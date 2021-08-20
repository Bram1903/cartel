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
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
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
        if ctx.author.id not in admins:
            channel = self.client.get_channel(int(botChannel))
            if ctx.channel == channel:
                await ctx.send(embed=em)
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
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Whois(client))  # Other part of setting up the cog.
