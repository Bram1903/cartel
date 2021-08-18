import json

from discord.ext import commands

with open("./config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        botChannel = value['bot-commands']
        admins = value['admins']
        TICKET_CHANNEL_ID = value['ticket_channel_id']
        TICKET_CATEGORY_ID = value['ticket_category_id']

TICKET_CATEGORY = (int(TICKET_CATEGORY_ID))


# Imports


class Listener(commands.Cog):
    def __init__(self, client):
        self.client = client  # Set up parts of the cog.

    @commands.Cog.listener()
    async def on_ready(self):
        print('Listener has successfully been initialized.')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def appeal(self, ctx):
        channel = self.client.get_channel(int(TICKET_CHANNEL_ID))
        await ctx.send(f"If you want to create an appeal you can do it here {channel.mention}.")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def report(self, ctx):
        channel = self.client.get_channel(int(TICKET_CHANNEL_ID))
        await ctx.send(f"If you want to report someone you can do it here {channel.mention}.")


def setup(client):
    client.add_cog(Listener(client))
