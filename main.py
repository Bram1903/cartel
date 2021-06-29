from asyncio import sleep
import os
from dotenv import load_dotenv
load_dotenv()
import discord
import traceback
import sys
from discord.ext import commands
from discord import Activity, ActivityType, Embed, PermissionOverwrite
from discord.ext.commands import Bot, MissingPermissions, CommandNotFound, has_permissions, cooldown, BucketType, \
    CommandOnCooldown, check, CheckFailure

load_dotenv()

client = Bot(command_prefix="?",
             help_command=None,
             case_insensitive=True,
             max_messages=100,
             activity=Activity(type=ActivityType.watching,
                               name=f"over Cartel."))


@client.command()
@has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    moduleLoaded = Embed(title=f"Module {extension} has succesfully been loaded.",
                    colour=0x36393F)
    await ctx.send(embed=moduleLoaded)

@client.command()
@has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    moduleUnloaded = Embed(title=f"Module {extension} has succesfully been unloaded.",
                    colour=0x36393F)
    await ctx.send(embed=moduleUnloaded)

@client.command()
@has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    moduleReloaded = Embed(title=f"Module {extension} has succesfully been reloaded.",
                    colour=0x36393F)
    await ctx.send(embed=moduleReloaded)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)