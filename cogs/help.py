import discord
from discord.ext import commands
from discord import Embed


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
                                                  "Moderation     | ?help Moderation\n"
                                                  "Administration | ?help Administration\n"
                                                  "System         | ?system help```")
        await ctx.send(embed=help)

    @help.command(name='info')
    async def info_subcommand(self, ctx):
        info = Embed(title="CartelPvP | Help",
                     colour=0xAE0808)
        info.set_thumbnail(url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        info.add_field(name="Info commands", value="```Avatar  | ?avatar (user)\nInvites | ?invites\n"
                                                   "Latency | ?ping\nWhois   | ?whois (user)```")
        await ctx.send(embed=info)

def setup(client):
    client.add_cog(Invites(client))
