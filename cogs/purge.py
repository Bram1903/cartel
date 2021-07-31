from discord import Embed
from discord.ext import commands
import datetime
import json
from asyncio import sleep

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


class Purge(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Purge module has successfully been initialized.')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)  # Checks for the permission.
    async def purge(self, ctx, limit: int = None):
        if not limit:  # Checks if a limit is given.
            await ctx.message.delete()
            msg = await ctx.send("You must specify an amount.")
            await sleep(4.7)
            await msg.delete()
            return
        timestamp = datetime.datetime.utcnow()
        embed = Embed(description=f"Member ID: {ctx.author.id}", colour=0xAE0808)
        embed.set_author(name='Chat Purged',
                         icon_url='https://i.imgur.com/uoq4zFS.png')
        embed.add_field(name="Purged by", value=f"{ctx.author.mention}",
                        inline=False)
        embed.add_field(name="Amount", value=f"{limit}",
                        inline=False)
        embed.add_field(name="Channel", value=f"{ctx.channel.mention}",
                        inline=False)
        embed.set_footer(text=f"Purged on {timestamp}"
                         , icon_url=ctx.author.avatar_url)

        channel_embed = Embed(colour=0xAE0808)
        channel_embed.set_author(name=f'This chat has been purged.',
                                 icon_url='https://i.imgur.com/uoq4zFS.png')
        try:
            logs = self.client.get_channel(int(logging_channel))
            await ctx.channel.purge(limit=limit)  # Starts purging the channel with the given limit.
            await ctx.channel.send(embed=channel_embed)
            await logs.send(embed=embed)
        except:
            pass


def setup(client):
    client.add_cog(Purge(client))
