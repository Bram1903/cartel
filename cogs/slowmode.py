import datetime
import json
from asyncio import sleep

from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        lockdown_mute_role = value['verified_role_id']  # Gets the specific data
        logging_channel = value['logging_channel']


# imports


class Slowmode(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Slowmode module has successfully been initialized.')

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)  # Permission check
    async def slowmode(self, ctx, amount=None):
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if not amount:  # Checks if an amount is given.
            await ctx.message.delete()
            return await ctx.send("You must enter an amount.")  # Says to give an amount.
        await ctx.channel.edit(slowmode_delay=int(amount))  # Applies slow chat counter with the given amount.
        channel_embed = Embed(colour=0xAE0808)
        channel_embed.set_author(name=f'Slowmode activated.',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=channel_embed)
        timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
        embed = Embed(description=f"Channel ID: {ctx.channel.id}", colour=0xAE0808)
        embed.set_author(name='Slowmode Activated',
                         icon_url='https://i.imgur.com/SR9wWm9.png')
        embed.add_field(name="Activated by", value=f"{ctx.author.mention}",
                        inline=False)
        embed.add_field(name="Amount", value=f"{amount}s",
                        inline=False)
        embed.add_field(name="Channel", value=f"{ctx.channel.mention}",
                        inline=False)
        embed.set_footer(text=f"Activated on {timestamp}"
                         , icon_url=ctx.author.avatar_url)
        logs = self.client.get_channel(int(logging_channel))
        await logs.send(embed=embed)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)  # Permission check
    async def unslow(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)  # Sets the slowmode to 0 which means off.
        channel_embed = Embed(colour=0xAE0808)
        channel_embed.set_author(name=f'Slowmode deactivated.',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=channel_embed)
        timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
        embed = Embed(description=f"Channel ID: {ctx.channel.id}", colour=0x57F287)
        embed.set_author(name='Slowmode Deactivated',
                         icon_url='https://i.imgur.com/SR9wWm9.png')
        embed.add_field(name="Deactivated by", value=f"{ctx.author.mention}",
                        inline=False)
        embed.add_field(name="Channel", value=f"{ctx.channel.mention}",
                        inline=False)
        embed.set_footer(text=f"Deactivated on {timestamp}"
                         , icon_url=ctx.author.avatar_url)
        logs = self.client.get_channel(int(logging_channel))
        await logs.send(embed=embed)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()


def setup(client):
    client.add_cog(Slowmode(client))
