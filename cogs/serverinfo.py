import discord
from discord import Embed
from discord.ext import commands


class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Server info has successfully been initialized.')

    @commands.command(aliases=['si'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx):
        em = discord.Embed(color=0xAE0808)
        em.set_author(name='Server Info', icon_url='https://i.imgur.com/FgkMDGn.png')
        em.set_thumbnail(url=ctx.guild.icon_url)
        statues = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                   len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                   len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                   len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("Guild ID", f"`{ctx.guild.id}`", True),
                  ("Owner", ctx.guild.owner, True),
                  ("Region", str(ctx.guild.region).title(), True),
                  ("Text Channels", len(ctx.guild.text_channels), True),
                  ("Voice Channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Total Members", len(ctx.guild.members), True),
                  ("Statues",
                   f"<:green_circle:876826681871069184> {statues[0]}\n <:orange_circle:876826879108206683> {statues[1]}\n <:red_circle:876827033164996669> {statues[2]}\n <:sleeping:876827253324021801> {statues[3]}",
                   True)]

        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(serverinfo(client))
