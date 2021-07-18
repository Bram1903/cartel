from discord import Embed
from discord.ext import commands
from discord.ext.commands import has_permissions


class Invites(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Help module has successfully been initialized.')

    @commands.group(name='help', invoke_without_command=True)
    async def help(self, ctx):
        help = Embed(title="CartelPvP | Help",
                     colour=0xAE0808)
        help.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        help.add_field(name="Sub commands", value="```Info           | ?help info\n"
                                                  "Ticket         | ?help ticket\n"
                                                  "Moderation     | ?help moderation\n"
                                                  "System         | ?help system```")
        await ctx.send(embed=help)

    @help.command(name='info')
    async def info_subcommand(self, ctx):
        info = Embed(title="CartelPvP | Help",
                     colour=0xAE0808)
        info.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        info.add_field(name="Info commands", value="```Avatar  | ?avatar (user)\nInvites | ?invites\n"
                                                   "Latency | ?ping\nWhois   | ?whois (user)```")
        await ctx.send(embed=info)

    @help.command(name='ticket')
    async def ticket_subcommand(self, ctx):
        ticket = Embed(title="CartelPvP | Help",
                       colour=0xAE0808)
        ticket.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        ticket.add_field(name="Ticket commands (ticket channels only)", value="```Close  | ?close (reason)\nAppeal | "
                                                                              "?appeal```")
        await ctx.send(embed=ticket)

    @help.command(name='moderation')
    @has_permissions(manage_messages=True)
    async def moderation_subcommand(self, ctx):
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
                                   "Unslow    | ?unslow```")
        await ctx.send(embed=moderation)

    @help.command(name='system')
    @has_permissions(manage_messages=True)
    async def system_subcommand(self, ctx):
        moderation = Embed(title="CartelPvP | Help",
                           colour=0xAE0808)
        moderation.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        moderation.add_field(name="System commands",
                             value="```Module list    | ?system list\n"
                                   "Unload module  | ?system unload (module)\n"
                                   "Load module    | ?system load (module)\n"
                                   "Reload module  | ?system reload (module)\n"
                                   "Command logs   | ?system logs```")
        await ctx.send(embed=moderation)


def setup(client):
    client.add_cog(Invites(client))
