import discord
from discord.ext import commands


class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Server info has successfully been initialized.')

    @commands.command()
    async def serverinfo(self, ctx):
        server = ctx.message.guild
        channel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

        role_count = len(server.roles)
        emoji_count = len(server.emojis)
        em = discord.Embed(color=0xAE0808)
        em.add_field(name='Name', value=server.name, inline=True)
        em.add_field(name='Owner', value=server.owner, inline=True)
        em.add_field(name='Members', value=server.member_count, inline=True)
        em.add_field(name='Text Channels', value=str(channel_count))
        em.add_field(name='Region', value=server.region, inline=True)
        em.add_field(name='Verification Level', value=str(server.verification_level), inline=True)
        em.add_field(name='Roles', value=str(role_count))
        em.add_field(name='Emotes', value=str(emoji_count), inline=True)
        em.add_field(name='Created At', value=server.created_at.__format__('%A, %d. %B %Y'), inline=True)
        em.set_thumbnail(url=server.icon_url)
        em.set_author(name='Server Info')
        em.set_footer(text='Server ID: %s' % server.id)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(serverinfo(client))
