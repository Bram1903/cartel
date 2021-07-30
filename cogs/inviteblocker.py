from asyncio import sleep

import discord
from discord import Embed
from discord.ext import commands


class inviteblocker(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fileblocker has successfully been initialized.')

    @commands.Cog.listener()
    async def on_message(self, message):
        permission = message.author.guild_permissions.manage_messages
        if not permission:
            if message.content.startswith('https://discord.gg'):
                await message.delete()
                no_perm = Embed(colour=0xAE0808)
                no_perm.set_author(name='You are not allowed to send invite links.',
                                   icon_url='https://i.imgur.com/l2tL2kc.png')
                msg = await message.channel.send(embed=no_perm)
                await sleep(4.7)
                await msg.delete()
        else:
            return


def setup(client):
    client.add_cog(inviteblocker(client))
