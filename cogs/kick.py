import discord
from discord.ext import commands
from discord import Embed


# This prevents staff members from being punished
class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages
        if not permission:
            return argument
        else:
            raise commands.BadArgument(
                "You cannot punish other staff members")


class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kick module has successfully been initialized.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: Sinner = None, reason="Not specified"):
        await ctx.message.delete()
        if not user:  # checks if there is a user
            return await ctx.send("You must specify a user")
        userDM = Embed(title="CartelPvP | Moderation",
                       description=f"You have been kicked from CartelPvP",
                       colour=0xAE0808)

        userDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        userDM.add_field(name="Kicked by", value=f"{ctx.author}", inline=True)
        userDM.add_field(name="Reason", value=f"{reason}", inline=True)
        if user:
            try:
                await user.send(embed=userDM)
            except discord.Forbidden:
                pass
        try:
            await user.kick(reason=reason)
        except discord.Forbidden:
            return await ctx.send("Are you trying to kick someone higher than the bot")
        embedKick = Embed(title="CartelPvP | Moderation",
                         description=f"{user} has been kicked from CartelPvP.",
                         colour=0xAE0808)
        embedKick.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        embedKick.add_field(name="Kicked by", value=f"{ctx.author}", inline=True)
        embedKick.add_field(name="Reason", value=f"{reason}", inline=True)
        await ctx.send(embed=embedKick)


def setup(client):
    client.add_cog(Kick(client))
