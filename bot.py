import json
import os
import platform
import sys
from asyncio import sleep

import discord
import psutil
from discord import Activity, ActivityType, Embed, PermissionOverwrite
from discord.ext.commands import Bot, has_permissions, cooldown, BucketType, \
    check
from dotenv import load_dotenv

load_dotenv()

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
# Create a file called config.json in the root of your bot, and put the following details in it:
# {
#   "server_details": [
#     {
#       "announcements_id": "860117203683770399",
#       "ticket_logs_id": "859442000255123476",
#       "ticket_category_id": "859442055867793438",
#       "ticket_channel_id": "859486071871111189",
#       "verified_role_id": "859724691643039774",
#       "configured_ip": "IP_configured",
#       "welcome_channel_id": "859725386576953364",
#       "logging_channel": "865541976950833172",
#       "admins": [574958028651233281, 373556761015353354, 426902176661635082]
#     }
#   ]
# }
else:
    with open("config.json") as configFile:
        data = json.load(configFile)
        for value in data["server_details"]:
            ticket_logs = value['ticket_logs_id']
            TICKET_CATEGORY_ID = value['ticket_category_id']
            TICKET_CHANNEL_ID = value['ticket_channel_id']
            admins = value['admins']

client = Bot(command_prefix=">",
             help_command=None,
             case_insensitive=True,
             max_messages=100,
             activity=Activity(type=ActivityType.watching,
                               name=f"over Cartel."),
             intents=discord.Intents.all())


@client.group(name='system', invoke_without_command=True)
async def system(ctx):
    pass


@system.command(name='load')
async def load_subcommand(ctx, extension=None):
    if ctx.author.id in admins:
        if not extension:
            return await ctx.send("You must provide a module.")
        try:
            client.load_extension(f'cogs.{extension}')
            moduleLoaded = Embed(colour=0x2F3136)
            moduleLoaded.set_author(name=f'Module {extension} has successfully been loaded.',
                                    icon_url='https://i.imgur.com/pkfD5kS.png')
            await ctx.send(embed=moduleLoaded)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        NoPerm = Embed(colour=0xAE0808)
        NoPerm.set_author(name='You are not a system administrator.',
                          icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=NoPerm)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()


@system.command(name='unload')
async def unload_subcommand(ctx, extension=None):
    if ctx.author.id in admins:
        if not extension:
            return await ctx.send("You must provide a module")
        try:
            client.unload_extension(f'cogs.{extension}')
            moduleUnloaded = Embed(colour=0x2F3136)
            moduleUnloaded.set_author(name=f'Module {extension} has successfully been unloaded.',
                                      icon_url='https://i.imgur.com/pkfD5kS.png')
            await ctx.send(embed=moduleUnloaded)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        NoPerm = Embed(colour=0xAE0808)
        NoPerm.set_author(name='You are not a system administrator.',
                          icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=NoPerm)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()


@system.command(name='reload')
async def reload_subcommand(ctx, extension=None):
    if ctx.author.id in admins:
        if not extension:
            return await ctx.send("You must provide a module")
        try:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            moduleReloaded = Embed(colour=0x2F3136)
            moduleReloaded.set_author(name=f'Module {extension} has successfully been reloaded.',
                                      icon_url='https://i.imgur.com/pkfD5kS.png')
            await ctx.send(embed=moduleReloaded)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        NoPerm = Embed(colour=0xAE0808)
        NoPerm.set_author(name='You are not a system administrator.',
                          icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=NoPerm)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()


@system.command(name='reloadall')
async def reloadall_subcommand(ctx):
    if ctx.author.id in admins:
        loadedModules = ""
        failedModules = ""
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    client.reload_extension(f"cogs.{name}")
                    loadedModules += file[:-3] + "\n"
                except:
                    failedModules += file[:-3] + "\n"
        try:
            reload_List = Embed(title="CartelPvP | System",
                                colour=0xAE0808)
            reload_List.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
            reload_List.add_field(name="Reloaded modules", value=f"```\n{loadedModules}```", inline=True)
            reload_List.add_field(name="Failed", value=f"```\n{failedModules}```", inline=True)
            await ctx.send(embed=reload_List)
        except Exception as e:
            print(e)
    else:
        NoPerm = Embed(colour=0xAE0808)
        NoPerm.set_author(name='You are not a system administrator.',
                          icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=NoPerm)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()


# noinspection PyShadowingBuiltins
@system.command(name='list')
async def list_subcommand(ctx):
    if ctx.author.id in admins:
        Module_List = ""
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                Module_List += file[:-3] + "\n"
        module_list = Embed(title="CartelPvP | System",
                            colour=0xAE0808)
        module_list.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        module_list.add_field(name="Module List", value=f"```\n{Module_List}```")
        await ctx.send(embed=module_list)
    else:
        NoPerm = Embed(colour=0xAE0808)
        NoPerm.set_author(name='You are not a system administrator.',
                          icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=NoPerm)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()


@system.command(name='logs')
async def logs_subcommand(ctx):
    if ctx.author.id in admins:
        try:
            await ctx.send("Full logs")
            await ctx.send(file=discord.File(r'./commandlogger.txt'))
        except discord.Forbidden:
            pass
    else:
        NoPerm = Embed(colour=0xAE0808)
        NoPerm.set_author(name='You are not a system administrator.',
                          icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=NoPerm)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()


@system.command(name='info')
async def info_subcommand(ctx):
    if ctx.author.id in admins:
        cpu = psutil.cpu_percent()
        memoryUsed = psutil.virtual_memory().percent
        cores = psutil.cpu_count(logical=False)
        threads = psutil.cpu_count()
        python = platform.python_version()
        text = "This bot is written by Bram#2698"
        usageEmbed = Embed(title="CartelPvP | System",
                           description="System usage",
                           colour=0xAE0808)
        usageEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        usageEmbed.add_field(name="CPU usage", value=f"{cpu}%", inline=True)
        usageEmbed.add_field(name="Memory usage", value=f"{memoryUsed}%", inline=True)
        usageEmbed.add_field(name="Python Version", value=f"{python}", inline=False)
        usageEmbed.add_field(name="discord.py Version", value=discord.__version__, inline=False)
        usageEmbed.add_field(name="Cores", value=f"{cores}", inline=True)
        usageEmbed.add_field(name="Threads", value=f"{threads}", inline=True)
        usageEmbed.set_footer(text=text, icon_url="https://i.imgur.com/28qrLRX.png")
        await ctx.send(embed=usageEmbed)
    else:
        NoPerm = Embed(colour=0xAE0808)
        NoPerm.set_author(name='You are not a system administrator.',
                          icon_url='https://i.imgur.com/SR9wWm9.png')
        msg = await ctx.send(embed=NoPerm)
        await ctx.message.delete()
        await sleep(4.7)
        await msg.delete()


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
