import discord
from discord.ext import commands
from discord import Embed


class Whois(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Whois module has successfully been initialized.')

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        if not member:  # if member is not mentioned
            member = ctx.message.author  # set member as the author
        roles = [role for role in member.roles]

        whoisEmbed = Embed(title=str(member),
                           timestamp=ctx.message.created_at,
                           colour=0xAE0808)

        whoisEmbed.set_thumbnail(url=member.avatar_url)
        whoisEmbed.set_footer(text=f"Requested by {ctx.author}")
        whoisEmbed.add_field(name="Display Name:", value=member.display_name)
        whoisEmbed.add_field(name="ID:", value=member.id)
        whoisEmbed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, "
                                                                                          "%I:%M %p UTC"))
        whoisEmbed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        whoisEmbed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
        whoisEmbed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=whoisEmbed)


def setup(client):
    client.add_cog(Whois(client))
