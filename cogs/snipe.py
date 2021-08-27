import datetime
import json
from asyncio import sleep

import discord
from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        lockdown_mute_role = value['verified_role_id']  # Gets the specific data
        logging_channel = value['logging_channel']
        admins = value['admins']


class Snipe(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.last_msg = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Snipe module has successfully been initialized.')

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @commands.command(name="snipe")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def snipe(self, ctx: commands.Context):
        author = self.last_msg.author
        content = self.last_msg.content
        channel = self.last_msg.channel
        contentguild = self.last_msg.guild
        guild = ctx.guild
        with open('botblacklist.json', 'r+') as f:
            users = json.load(f)
            if ctx.author.id in users:
                return
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            await ctx.reply("There is no message to snipe!", mention_author=False)
            return
        if contentguild.id != guild.id:
            await ctx.reply("There is no message to snipe!", mention_author=False)
            return
        if self.last_msg.author.id in admins:
            await ctx.message.delete()
            embed = Embed(colour=0xAE0808)
            embed.set_author(name="I'm not allowed to snipe my creator.",
                             icon_url='https://i.imgur.com/sFhjp83.png')
            msg = await ctx.send(embed=embed)
            await sleep(4.7)
            await msg.delete()
            return

        embed = Embed(colour=0xAE0808)
        embed.set_author(name='This snipe has been send to the logs channel.',
                         icon_url='https://i.imgur.com/uoq4zFS.png')
        await ctx.reply(embed=embed, mention_author=False)

        timestamp = datetime.datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")
        embed_logs = Embed(description=f"User ID: {author.id}", colour=0xE67E22)
        embed_logs.set_author(name='Message Sniped',
                              icon_url='https://i.imgur.com/uoq4zFS.png'),
        embed_logs.add_field(name="Sniped", value=f"{author.mention}",
                             inline=False)
        embed_logs.add_field(name="Sniped by", value=f"{ctx.author.mention}",
                             inline=False)
        embed_logs.add_field(name="Content", value=f"{content}",
                             inline=False)
        embed_logs.add_field(name="Channel", value=f"{channel.mention}",
                             inline=False)
        embed_logs.set_footer(text=f"Sniped on {timestamp}"
                              , icon_url=author.avatar_url)
        logs = self.client.get_channel(int(logging_channel))
        await logs.send(embed=embed_logs)


def setup(client):
    client.add_cog(Snipe(client))
