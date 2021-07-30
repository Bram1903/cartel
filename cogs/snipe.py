import discord
from discord import Embed
from discord.ext import commands


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
    @commands.has_permissions(manage_messages=True)
    async def snipe(self, ctx: commands.Context):
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_msg.author
        content = self.last_msg.content

        SnipeEmbed = Embed(title="CartelPvP | Moderation",
                           description=content,
                           colour=0xAE0808)
        SnipeEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        SnipeEmbed.add_field(name="**Sniped by**", value=f"{ctx.author}", inline=True)
        SnipeEmbed.add_field(name="**Sniped**", value=f"{author}", inline=True)
        await ctx.send(embed=SnipeEmbed)


def setup(client):
    client.add_cog(Snipe(client))
