from discord.ext import commands
from discord import Embed


class Purge(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Purge module has successfully been initialized.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)
        purgeEmbed = Embed(title="CartelPvP | Moderation",
                           description="This chat has been purged",
                           colour=0xAE0808)
        purgeEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        purgeEmbed.add_field(name="Purged by", value=f"{ctx.author}", inline=True)
        purgeEmbed.add_field(name="Amount", value=f"{limit}", inline=True)
        await ctx.send(embed=purgeEmbed)
        

def setup(client):
    client.add_cog(Purge(client))
