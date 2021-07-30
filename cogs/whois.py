import discord
from discord import Embed
from discord.ext import commands


# Imports


class Whois(commands.Cog):
    def __init__(self, client):
        self.client = client  # Set up parts of the cog.

    @commands.Cog.listener()
    async def on_ready(self):
        print('Whois module has successfully been initialized.')  # Basic on_ready event, but designed to work in a cog.

    @commands.command()
    @commands.guild_only()
    async def whois(self, ctx, member: discord.Member = None):
        if not member:  # Checks if a member is given.
            member = ctx.message.author  # If member is not given set the ctx.author as member.
        roles = [role for role in member.roles]  # Loops through all the roles of the given member.

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
    client.add_cog(Whois(client))  # Other part of setting up the cog.
