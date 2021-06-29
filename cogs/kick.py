from asyncio import sleep
import os
import discord
import traceback
import sys
from discord import Activity, ActivityType, Embed, PermissionOverwrite
from discord.ext.commands import Bot, MissingPermissions, CommandNotFound, has_permissions, cooldown, BucketType, \
    CommandOnCooldown, check, CheckFailure
from discord.ext import commands

class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kick is ready!')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked.")
        

def setup (client):
    client.add_cog(Kick(client))