from asyncio import sleep
import os
import discord
from discord.ext import commands
import traceback
import sys
from discord import Activity, ActivityType, Embed, PermissionOverwrite
from discord.ext.commands import Bot, MissingPermissions, CommandNotFound, has_permissions, cooldown, BucketType, \
    CommandOnCooldown, check, CheckFailure

class Ticket(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ticket system is ready!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

def setup (client):
    client.add_cog(Ticket(client))