import datetime
import json
import os
import time
from asyncio import sleep

import discord
from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


class fileblocker(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.5)
        print('Fileblocker has successfully been initialized.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        else:
            permission = message.author.guild_permissions.manage_messages
            if not permission:
                for file in message.attachments:
                    if file.filename.endswith((".exe", ".bat", ".vb", ".jar")):
                        for attachment in message.attachments:
                            await attachment.save(attachment.filename)
                        no_perm = Embed(colour=0xAE0808)
                        no_perm.set_author(name='You are not allowed to send that file type.',
                                           icon_url='https://i.imgur.com/uoq4zFS.png')
                        msg = await message.channel.send(embed=no_perm)
                        timestamp = datetime.datetime.utcnow()
                        embed_logs = Embed(description=f"User ID: {message.author.id}", colour=0xE67E22)
                        embed_logs.set_author(name='File Removed',
                                              icon_url='https://i.imgur.com/uoq4zFS.png'),
                        embed_logs.add_field(name="User", value=f"{message.author.mention}",
                                             inline=False)
                        embed_logs.add_field(name="Channel", value=f"{message.channel.mention}",
                                             inline=False)
                        embed_logs.set_footer(text=f"Removed on {timestamp}"
                                              , icon_url=message.author.avatar_url)
                        await message.delete()
                        logs = self.client.get_channel(int(logging_channel))
                        await logs.send(embed=embed_logs)
                        file = discord.File(attachment.filename)
                        await logs.send(file=file)
                        os.remove(attachment.filename)
                        await sleep(4.7)
                        await msg.delete()
            else:
                return


def setup(client):
    client.add_cog(fileblocker(client))
