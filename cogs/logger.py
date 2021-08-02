import datetime
import json

from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


class logger(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logger has successfully been initialized.')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.client.user:
            return
        else:
            if message.author.id not in admins:
                try:
                    timestamp = datetime.datetime.utcnow()
                    embed = Embed(description=f"Message ID: {message.id}", colour=0xE67E22)
                    embed.set_author(name='Message Deleted',
                                     icon_url='https://i.imgur.com/Jf565HJ.png')
                    embed.add_field(name="Content", value=message.content,
                                    inline=False)
                    embed.add_field(name="Channel", value=message.channel.mention,
                                    inline=False)
                    embed.set_footer(text=f"Message of {message.author.name} removed • {timestamp}"
                                     , icon_url=message.author.avatar_url)
                    channel = self.client.get_channel(int(logging_channel))
                    await channel.send(embed=embed)
                except:
                    pass
            else:
                pass

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.author == self.client.user:
            return
        else:
            if message_before.author.id not in admins:
                try:
                    timestamp = message_after.edited_at
                    embed = Embed(description=f"Message ID: {message_before.id}", colour=0xE67E22)
                    embed.set_author(name='Message Edited',
                                     icon_url='https://i.imgur.com/PV8yJN6.png')
                    embed.add_field(name="Before", value=message_before.content,
                                    inline=False)
                    embed.add_field(name="After", value=message_after.content,
                                    inline=False)
                    embed.add_field(name="Channel", value=message_before.channel.mention,
                                    inline=False)
                    embed.set_footer(text=f"Edit by {message_before.author.name} • {timestamp}"
                                     , icon_url=message_after.author.avatar_url)
                    channel = self.client.get_channel(int(logging_channel))
                    await channel.send(embed=embed)
                except:
                    pass
            else:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        timestamp = datetime.datetime.utcnow()
        embed = Embed(description=f"Member ID: {member.id}", colour=0x57F287)
        embed.set_author(name='Member Joined',
                         icon_url=member.avatar_url)
        embed.add_field(name="Member", value=member.mention,
                        inline=False)
        embed.set_footer(text=f"Joined on • {timestamp}"
                         , icon_url=member.avatar_url)
        channel = self.client.get_channel(int(logging_channel))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        timestamp = datetime.datetime.utcnow()
        embed = Embed(description=f"Member ID: {member.id}", colour=0xAE0808)
        embed.set_author(name='Member Left',
                         icon_url=member.avatar_url)
        embed.add_field(name="Member", value=member.mention,
                        inline=False)
        embed.set_footer(text=f"Left on • {timestamp}"
                         , icon_url=member.avatar_url)
        channel = self.client.get_channel(int(logging_channel))
        await channel.send(embed=embed)


def setup(client):
    client.add_cog(logger(client))
