import json
from asyncio import sleep

from discord import Embed
from discord.ext import commands
from discord.utils import get

with open("config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        admins = value['admins']
        role_media_admin = value['media-admin']


class Invites(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Help module has successfully been initialized.')

    @commands.group(name='help', invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        help = Embed(title="CartelPvP | Help",
                     colour=0xAE0808)
        help.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        help.add_field(name="Sub commands", value="```Info         | ?help info\n"
                                                  "Support      | ?help support\n" 
                                                  "Ticket       | ?help ticket\n"
                                                  "Media        | ?help media\n"
                                                  "Moderation   | ?help moderation\n"
                                                  "System       | ?help system```")
        await ctx.send(embed=help)

    @help.command(name='info')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info_subcommand(self, ctx):
        info = Embed(title="CartelPvP | Help",
                     colour=0xAE0808)
        info.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        info.add_field(name="Info commands", value="```Avatar     | ?avatar (user)\n"
                                                   "Invites    | ?invites\n"
                                                   "Latency    | ?ping\n"
                                                   "Userinfo   | ?ui (user)\n"
                                                   "Serverinfo | ?si```")
        await ctx.send(embed=info)

    @help.command(name='support')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def support_subcommand(self, ctx):
        info = Embed(title="CartelPvP | Help",
                     colour=0xAE0808)
        info.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        info.add_field(name="Support commands", value="```Appeal   | ?appeal\n"
                                                      "Report   | ?report```")
        await ctx.send(embed=info)

    @help.command(name='ticket')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ticket_subcommand(self, ctx):
        ticket = Embed(title="CartelPvP | Help",
                       colour=0xAE0808)
        ticket.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        ticket.add_field(name="Ticket commands (ticket channels only)",
                         value="```Close  | ?close (reason)\n"
                               "Appeal | ?createappeal (staff only)```")
        await ctx.send(embed=ticket)

    @help.command(name='media')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def media_subcommand(self, ctx):
        media_role_id = (int(role_media_admin))
        role = get(ctx.guild.roles, id=media_role_id)
        if role not in ctx.author.roles:
            await ctx.message.delete()
            no_perm = Embed(colour=0xAE0808)
            no_perm.set_author(name='You are not a media administrator.',
                               icon_url='https://i.imgur.com/sFhjp83.png')
            msg = await ctx.channel.send(embed=no_perm)
            await sleep(4.7)
            await msg.delete()
            return
        info = Embed(title="CartelPvP | Help",
                     colour=0xAE0808)
        info.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        info.add_field(name="Media commands", value="```Grant     | ?grant (user) <rank>\n"
                                                    "Revoke    | ?revoke (user) <rank>```")
        await ctx.send(embed=info)

    @help.command(name='moderation')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def moderation_subcommand(self, ctx):
        permission = ctx.author.guild_permissions.manage_messages
        if not permission:
            await ctx.message.delete()
            no_perm = Embed(colour=0xAE0808)
            no_perm.set_author(name='You are not a staff member.',
                               icon_url='https://i.imgur.com/sFhjp83.png')
            msg = await ctx.channel.send(embed=no_perm)
            await sleep(4.7)
            await msg.delete()
            return
        moderation = Embed(title="CartelPvP | Help",
                           colour=0xAE0808)
        moderation.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        moderation.add_field(name="Moderation commands",
                             value="```Ban       | ?ban (user (reason)\n"
                                   "Kick      | ?kick (user) (reason)\n"
                                   "Mute      | ?mute (user) (reason)\n"
                                   "Unmute    | ?unmute (user)\n"
                                   "Lockdown  | ?lockdown (channel_id)\n"
                                   "Purge     | ?purge (amount)\n"
                                   "Slowmode  | ?slowmode (time)\n"
                                   "Unslow    | ?unslow\n"
                                   "Snipe     | ?snipe```")
        await ctx.send(embed=moderation)

    @help.command(name='system')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def system_subcommand(self, ctx):
        if ctx.author.id not in admins:
            await ctx.message.delete()
            no_perm = Embed(colour=0xAE0808)
            no_perm.set_author(name='You are not a system administrator.',
                               icon_url='https://i.imgur.com/sFhjp83.png')
            msg = await ctx.channel.send(embed=no_perm)
            await sleep(4.7)
            await msg.delete()
            return
        moderation = Embed(title="CartelPvP | Help",
                           colour=0xAE0808)
        moderation.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        moderation.add_field(name="System commands",
                             value="```Module list    | ?system list\n"
                                   "Unload module  | ?system unload (module)\n"
                                   "Load module    | ?system load (module)\n"
                                   "Reload module  | ?system reload (module)\n"
                                   "Reload all     | ?system reloadall\n"
                                   "Command logs   | ?system logs\n"
                                   "System info    | ?system info```")
        await ctx.send(embed=moderation)


def setup(client):
    client.add_cog(Invites(client))
