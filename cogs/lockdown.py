import json

import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        lockdown_mute_role = value['verified_role_id']  # Gets the specific data


class Lockdown(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Lockdown module has successfully been initialized.')

    @commands.command()
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
                await ctx.message.delete()  # Removes that executed command, and says the current channel is
                # under lockdown.
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
            embed2 = Embed(title="This channel is now under lockdown.",
                           colour=0xAE0808)
            await channel.send(embed=embed2)
        else:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = True
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have removed {channel.mention} from lockdown.")
            else:
                await ctx.message.delete()
            embed3 = Embed(title="This channel is no longer under lockdown.",
                           colour=0xAE0808)
            await channel.send(embed=embed3)


def setup(client):
    client.add_cog(Lockdown(client))
