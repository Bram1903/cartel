import datetime
import json

import discord
from discord import Embed
from discord.ext import commands
from asyncio import sleep
from discord.utils import get

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        role_media_admin = value['media-admin']
        role_youtuber = value['youtuber']
        role_famous = value['famous']
        role_partner = value['partner']
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


class Media(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Media has successfully been initialized.')

    @commands.command(pass_context=True)
    async def grant(self, ctx, member: discord.Member=None, rank=None):
        media_role_id = (int(role_media_admin))
        role = get(ctx.guild.roles, id=media_role_id)
        await ctx.message.delete()
        if role in ctx.author.roles:
            if not member:
                msg = await ctx.send('You must provide a user.')
                await sleep(4.7)
                await msg.delete()
                return
            if not rank:
                msg = await ctx.send('You must provide a rank.')
                await sleep(4.7)
                await msg.delete()
                return
            if rank.lower() == "youtuber":
                youtuber_id = (int(role_youtuber))
                youtuber = get(ctx.guild.roles, id=youtuber_id)
                try:
                    await member.add_roles(youtuber)
                except:
                    await ctx.send("Couldn't give the rank.")
                nick = f"YouTuber | {member.display_name}"
                try:
                    await member.edit(nick=nick)
                except:
                    await ctx.send("Couldn't change the prefix.")
                embed = Embed(colour=0x57F287)
                embed.set_author(name=f'Granted YouTuber to {member.display_name}.',
                            icon_url='https://i.imgur.com/0Lzd0go.png')
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
            elif rank.lower() == "famous":
                famous_id = (int(role_famous))
                famous = get(ctx.guild.roles, id=famous_id)
                try:
                    await member.add_roles(famous)
                except:
                    await ctx.send("Couldn't give the rank.")
                nick = f"Famous | {member.display_name}"
                try:
                    await member.edit(nick=nick)
                except:
                    await ctx.send("Couldn't change the prefix.")
                embed = Embed(colour=0x57F287)
                embed.set_author(name=f'Granted Famous to {member.display_name}.',
                                 icon_url='https://i.imgur.com/0Lzd0go.png')
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
            elif rank.lower() == "partner":
                partner_id = (int(role_partner))
                partner = get(ctx.guild.roles, id=partner_id)
                try:
                    await member.add_roles(partner)
                except:
                    await ctx.send("Couldn't give the rank.")
                nick = f"Partner | {member.display_name}"
                try:
                    await member.edit(nick=nick)
                except:
                    await ctx.send("Couldn't change the prefix.")
                embed = Embed(colour=0x57F287)
                embed.set_author(name=f'Granted Partner to {member.display_name}.',
                                 icon_url='https://i.imgur.com/0Lzd0go.png')
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
            else:
                embed = Embed(colour=0xAE0808)
                embed.set_author(name='Invalid Rank',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
                embed.add_field(name="Options", value="```\nyoutuber\nfamous```",
                                inline=False)
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
        else:
            await ctx.message.delete()
            no_perm = Embed(colour=0xAE0808)
            no_perm.set_author(name='You are not an media administrator.',
                               icon_url='https://i.imgur.com/sFhjp83.png')
            msg = await ctx.channel.send(embed=no_perm)
            await sleep(4.7)
            await msg.delete()

    @commands.command(pass_context=True)
    async def revoke(self, ctx, member: discord.Member = None, rank=None):
        media_role_id = (int(role_media_admin))
        role = get(ctx.guild.roles, id=media_role_id)
        await ctx.message.delete()
        if role in ctx.author.roles:
            if not member:
                msg = await ctx.send('You must provide a user.')
                await sleep(4.7)
                await msg.delete()
                return
            if not rank:
                msg = await ctx.send('You must provide a rank.')
                await sleep(4.7)
                await msg.delete()
                return
            if rank.lower() == "youtuber":
                youtuber_id = (int(role_youtuber))
                youtuber = get(ctx.guild.roles, id=youtuber_id)
                try:
                    await member.remove_roles(youtuber)
                except:
                    await ctx.send("Couldn't remove the rank.")
                    return
                nick = member.name
                try:
                    await member.edit(nick=nick)
                except:
                    await ctx.send("Couldn't remove the prefix.")
                    return
                embed = Embed(colour=0xAE0808)
                embed.set_author(name=f'Revoked YouTuber from {member.display_name}.',
                                 icon_url='https://i.imgur.com/0Lzd0go.png')
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
            elif rank.lower() == "famous":
                famous_id = (int(role_famous))
                famous = get(ctx.guild.roles, id=famous_id)
                try:
                    await member.remove_roles(famous)
                except:
                    await ctx.send("Couldn't remove the rank.")
                nick = member.name
                try:
                    await member.edit(nick=nick)
                except:
                    await ctx.send("Couldn't remove the prefix.")
                    return
                embed = Embed(colour=0xAE0808)
                embed.set_author(name=f'Revoked Famous from {member.display_name}.',
                                 icon_url='https://i.imgur.com/0Lzd0go.png')
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
            elif rank.lower() == "partner":
                partner_id = (int(role_partner))
                partner = get(ctx.guild.roles, id=partner_id)
                try:
                    await member.remove_roles(partner)
                except:
                    await ctx.send("Couldn't remove the rank.")
                    return
                nick = member.name
                try:
                    await member.edit(nick=nick)
                except:
                    await ctx.send("Couldn't remove the prefix.")
                    return
                embed = Embed(colour=0xAE0808)
                embed.set_author(name=f'Revoked partner from {member.display_name}.',
                                 icon_url='https://i.imgur.com/0Lzd0go.png')
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
            else:
                embed = Embed(colour=0xAE0808)
                embed.set_author(name='Invalid Rank',
                                 icon_url='https://i.imgur.com/SR9wWm9.png')
                embed.add_field(name="Options", value="```\nyoutuber\nfamous```",
                                inline=False)
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
        else:
            await ctx.message.delete()
            no_perm = Embed(colour=0xAE0808)
            no_perm.set_author(name='You are not an media administrator.',
                               icon_url='https://i.imgur.com/sFhjp83.png')
            msg = await ctx.channel.send(embed=no_perm)
            await sleep(4.7)
            await msg.delete()


def setup(client):
    client.add_cog(Media(client))
