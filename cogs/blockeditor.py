import json
from asyncio import sleep

from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


class blockeditor(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Blocking editor has successfully been initialized.')

    @commands.group(name='blocker', invoke_without_command=True)
    async def blocker(self, ctx):
        pass

    @blocker.command(name='add')
    async def add_subcommand(self, ctx, word=None, extension="maliciousblocker"):
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if ctx.author.id not in admins:
            NoPerm = Embed(colour=0xAE0808)
            NoPerm.set_author(name='You are not a system administrator.',
                              icon_url='https://i.imgur.com/SR9wWm9.png')
            msg = await ctx.send(embed=NoPerm)
            await ctx.message.delete()
            await sleep(4.7)
            await msg.delete()
            return
        if not word:
            await ctx.reply("You must provide a word.", mention_author=False)
            return
        with open('blacklist.json', 'r+') as f:
            words = json.load(f)
            if word in words:
                channel_embed = Embed(colour=0xAE0808)
                channel_embed.set_author(name=f'{word} is already blocked.',
                                         icon_url='https://i.imgur.com/SR9wWm9.png')
                await ctx.reply(embed=channel_embed, mention_author=False)
                return
            words.append(word)
            f.seek(0)
            json.dump(words, f)
            f.truncate()
            self.client.unload_extension(f'cogs.{extension}')
            self.client.load_extension(f'cogs.{extension}')
            channel_embed = Embed(colour=0xAE0808, )
            channel_embed.set_author(name=f'{word} has been blacklisted.',
                                     icon_url='https://i.imgur.com/SR9wWm9.png', )
            await ctx.reply(embed=channel_embed, mention_author=False)

    @blocker.command(name='remove')
    async def remove_subcommand(self, ctx, word=None, extension="maliciousblocker"):
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if ctx.author.id not in admins:
            NoPerm = Embed(colour=0xAE0808)
            NoPerm.set_author(name='You are not a system administrator.',
                              icon_url='https://i.imgur.com/SR9wWm9.png')
            msg = await ctx.send(embed=NoPerm)
            await ctx.message.delete()
            await sleep(4.7)
            await msg.delete()
            return
        if not word:
            await ctx.reply("You must provide a word.", mention_author=False)
            return
        with open('blacklist.json', 'r+') as f:
            words = json.load(f)
            try:
                index_of_word: int = words.index(word)
            except ValueError:
                channel_embed = Embed(colour=0xAE0808)
                channel_embed.set_author(name=f'{word} is not blacklisted.',
                                         icon_url='https://i.imgur.com/SR9wWm9.png')
                await ctx.reply(embed=channel_embed, mention_author=False)
            else:
                del words[index_of_word]
                with open("blacklist.json", "w+") as write_file:
                    write_file.write(json.dumps(words))
                self.client.unload_extension(f'cogs.{extension}')
                self.client.load_extension(f'cogs.{extension}')
                channel_embed = Embed(colour=0x57F287)
                channel_embed.set_author(name=f'{word} is unblacklisted.',
                                         icon_url='https://i.imgur.com/SR9wWm9.png')
                await ctx.reply(embed=channel_embed, mention_author=False)


def setup(client):
    client.add_cog(blockeditor(client))
