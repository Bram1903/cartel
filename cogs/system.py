import json
import os
import platform
from asyncio import sleep

import discord
import psutil
from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


class System(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('System module has successfully been initialized.')

    @commands.group(name='system', invoke_without_command=True)
    async def system(self, ctx):
        pass

    @system.command(name='load')
    async def load_subcommand(self, ctx, extension=None):
        if ctx.author.id in admins:
            if not extension:
                return await ctx.send("You must provide a module.")
            try:
                self.client.load_extension(f'cogs.{extension}')
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
    async def unload_subcommand(self, ctx, extension=None):
        if ctx.author.id in admins:
            if not extension:
                return await ctx.send("You must provide a module")
            if extension == 'system':
                channel_embed = Embed(colour=0xAE0808)
                channel_embed.set_author(name=f'You cannot unload the main system.',
                                         icon_url='https://i.imgur.com/SR9wWm9.png')
                msg = await ctx.send(embed=channel_embed)
                await ctx.message.delete()
                await sleep(4.7)
                await msg.delete()
                return
            try:
                self.client.unload_extension(f'cogs.{extension}')
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
    async def reload_subcommand(self, ctx, extension=None):
        if ctx.author.id in admins:
            if not extension:
                return await ctx.send("You must provide a module")
            if extension == 'system':
                channel_embed = Embed(colour=0xAE0808)
                channel_embed.set_author(name=f'You cannot reload the main system.',
                                         icon_url='https://i.imgur.com/SR9wWm9.png')
                msg = await ctx.send(embed=channel_embed)
                await ctx.message.delete()
                await sleep(4.7)
                await msg.delete()
                return
            try:
                self.client.unload_extension(f'cogs.{extension}')
                self.client.load_extension(f'cogs.{extension}')
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
    async def reloadall_subcommand(self, ctx):
        if ctx.author.id in admins:
            loadedModules = ""
            failedModules = ""
            for file in os.listdir("./cogs"):
                if file.endswith('.py') and not file.startswith("system"):
                    name = file[:-3]
                    try:
                        self.client.reload_extension(f"cogs.{name}")
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
    async def list_subcommand(self, ctx):
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
    async def logs_subcommand(self, ctx):
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
    async def info_subcommand(self, ctx):
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


def setup(client):
    client.add_cog(System(client))
