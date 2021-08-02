import discord
from discord import Embed
from discord.ext import commands
import json


with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        welcome_channel = value['welcome_channel_id']
        logging_channel = value['logging_channel']
        member_role = value['verified_role_id']
        admins = value['admins']


# Imports


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client  # Set up parts of the cog.

    @commands.Cog.listener()
    async def on_ready(self):
        print('Welcome module has successfully been initialized.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = member_role
        await member.add_roles(role)
        welcome_embed = Embed(colour=0x57F287)
        welcome_embed.set_author(name=f'Welcome to the server, {member.display_name}!',
                                 icon_url=member.avatar_url)
        channel = self.client.get_channel(int(welcome_channel))
        await channel.send(embed=welcome_embed)


def setup(client):
    client.add_cog(Welcome(client))
