import discord
from discord.ext import commands
from discord import Embed
import sys
from discord import Activity, ActivityType, Embed, PermissionOverwrite
from discord.ext.commands import Bot, has_permissions, cooldown, BucketType, \
    check
from asyncio import sleep
import os
from dotenv import load_dotenv
import json


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ticket module has successfully been initialized.')


def setup(client):
    client.add_cog(Ticket(client))
