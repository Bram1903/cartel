import datetime
import json

import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        lockdown_mute_role = value['verified_role_id']  # Gets the specific data
        logging_channel = value['logging_channel']


class Lockdown(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Lockdown module has successfully been initialized.')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel  # Channel is or the channel mentioned, or the channel written in.
        role_id = (int(lockdown_mute_role))  # Gets the role which it should change the permissions of.
        role = get(ctx.guild.roles, id=role_id)  # Fetches the role.

        if role not in channel.overwrites:  # Creates the overwrite for the specific role.
            overwrites = {
                role: discord.PermissionOverwrite(send_messages=False)  # Disables send_message for the role.
            }
            await channel.edit(overwrites=overwrites)  # Executes the overwrite
            if ctx.channel != channel:  # When channel is mentioned send this
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                embed1 = Embed(title="This channel is now under lockdown",
                               colour=0xAE0808)
                await channel.send(embed=embed1)
        elif channel.overwrites[role].send_messages is True or \
                channel.overwrites[role].send_messages is None:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = False
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
            embed2 = Embed(title="This channel is now under lockdown.",
                           colour=0xAE0808)
            embed = Embed(description=f"Channel ID: {channel.id}", colour=0xAE0808)
            embed.set_author(name='Channel Lockdown',
                             icon_url='https://i.imgur.com/SR9wWm9.png')
            embed.add_field(name="Lockdown by", value=f"{ctx.author.mention}",
                            inline=False)
            embed.add_field(name="Channel", value=f"{channel.mention}",
                            inline=False)
            embed.set_footer(text=f"Lockdown on {timestamp}"
                             , icon_url=ctx.author.avatar_url)
            logs = self.client.get_channel(int(logging_channel))
            await channel.send(embed=embed2)
            await logs.send(embed=embed)
        else:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = True
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
                embed = Embed(description=f"Channel ID: {channel.id}", colour=0x57F287)
                embed.set_author(name='Channel Lockdown Removed',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
                embed.add_field(name="Lockdown removed by", value=f"{ctx.author.mention}",
                                inline=False)
                embed.add_field(name="Channel", value=f"{channel.mention}",
                                inline=False)
                embed.set_footer(text=f"Lockdown removed on {timestamp}"
                                 , icon_url=ctx.author.avatar_url)
                logs = self.client.get_channel(int(logging_channel))
                await logs.send(embed=embed)
                await ctx.send(f"I have removed {channel.mention} from lockdown.")
            else:
                embed3 = Embed(title="This channel is no longer under lockdown.",
                               colour=0xAE0808)

                timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
                embed = Embed(description=f"Channel ID: {channel.id}", colour=0x57F287)
                embed.set_author(name='Channel Lockdown Removed',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
                embed.add_field(name="Lockdown removed by", value=f"{ctx.author.mention}",
                                inline=False)
                embed.add_field(name="Channel", value=f"{channel.mention}",
                                inline=False)
                embed.set_footer(text=f"Lockdown removed on {timestamp}"
                                 , icon_url=ctx.author.avatar_url)
                logs = self.client.get_channel(int(logging_channel))
                await logs.send(embed=embed)
                await channel.send(embed=embed3)


def setup(client):
    client.add_cog(Lockdown(client))
