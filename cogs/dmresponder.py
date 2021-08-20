import datetime
import json

import discord
from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


class dmresponder(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('DM responder has successfully been initialized.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if message.author.id in users:
                return
        if not message.guild:
            try:
                embed = Embed(colour=0xAE0808)
                embed.set_author(name=f"I do not respond to DM's.",
                                 icon_url='https://i.imgur.com/sFhjp83.png')
                embed.add_field(name="Help", value="If you need help you can create a ticket in the server.",
                                inline=False)
                await message.channel.send(embed=embed)
            except discord.forbidden:
                pass
            try:
                timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
                embed = Embed(description=f"User ID: {message.author.id}", colour=0xE67E22)
                embed.set_author(name='Bot DM',
                                 icon_url='https://i.imgur.com/sFhjp83.png')
                embed.add_field(name="Message by", value=message.author.mention,
                                inline=False)
                embed.add_field(name="Content", value=message.content,
                                inline=False)
                embed.set_footer(text=f"Message by {message.author.name} send on • {timestamp}"
                                 , icon_url=message.author.avatar_url)
                channel = self.client.get_channel(int(logging_channel))
                await channel.send(embed=embed)
            except:
                pass
        else:
            pass


def setup(client):
    client.add_cog(dmresponder(client))
