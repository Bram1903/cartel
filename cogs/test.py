import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption, ButtonStyle, InteractionType


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Test module has successfully been initialized.')
        DiscordComponents(self.client)

    @commands.command()
    async def button(self, ctx):
        test = await ctx.channel.send(
            "_ _",
            components=[
                Button(label="WOW", style=ButtonStyle.blue, emoji="✉"),
            ]
        )
        interaction = await self.client.wait_for("button_click", check=lambda i: i.component.label.startswith("WOW"))
        await interaction.respond(content="Button clicked!")


def setup(client):
    client.add_cog(Test(client))
