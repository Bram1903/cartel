from asyncio import sleep

import discord
from discord import Embed
from discord.ext import commands


class fileblocker(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fileblocker has successfully been initialized.')

    @commands.Cog.listener()
    async def on_message(self, message):
        permission = discord.Permissions(manage_messages=True)
        if not permission:
            for file in message.attachments:
                if file.filename.endswith((".exe", ".dll")):
                    await message.delete()
                    NoPerm = Embed(colour=0xAE0808)
                    NoPerm.set_author(name='You are not allowed to send that file type.',
                                      icon_url='https://i.imgur.com/uoq4zFS.png')
                    msg = await message.channel.send(embed=NoPerm)
                    await sleep(4.7)
                    await msg.delete()
        else:
            return


def setup(client):
    client.add_cog(fileblocker(client))
