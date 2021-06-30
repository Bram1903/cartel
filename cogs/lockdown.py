import discord
from discord.ext import commands
from discord import Embed

class Lockdown(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Lockdown module has succesfully been initialized.')


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        role = ctx.guild.default_role

        if role not in channel.overwrites:
            overwrites = {
                role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
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