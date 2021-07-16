import json

import discord
from discord.ext import commands
from discord import Embed

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        welcome_channel = value['welcome_channel_id']


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Welcome module has successfully been initialized.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            channel = self.client.get_channel(int(welcome_channel))
            try:
                WelcomeEmbed = Embed(colour=0xAE0808)
                WelcomeEmbed.set_author(name=member.name, icon_url=member.avatar_url)
                WelcomeEmbed.add_field(name=
                                       "Welcome",
                                       value=f"**Hey,{member.mention}! Welcome to CartelPvP"
                                             f"\nI hope you enjoy your stay here!\nThanks for joining**",
                                       inline=False)
                WelcomeEmbed.set_thumbnail(url=member.avatar_url)
                await channel.send(embed=WelcomeEmbed)
            except Exception as e:
                raise e
        except Exception as e:
            raise e


def setup(client):
    client.add_cog(Welcome(client))
