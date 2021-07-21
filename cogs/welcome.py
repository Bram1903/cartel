from discord import Embed
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client  # Set up parts of the cog.

    @commands.Cog.listener()
    async def on_ready(self):
        print('Welcome module has successfully been initialized.')  # Basic on_ready
        # event, but designed to work in a cog.

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcomeChannel = await self.client.fetch_channel(867422970791985183)
        welcome = Embed(title="CartelPvP | Welcome",
                        description=f"Welcome to the server {member.name}!",
                        colour=0xAE0808)
        welcome.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        await welcomeChannel.send(embed=welcome)


def setup(client):
    client.add_cog(Welcome(client))  # Other part of setting up the cog.
