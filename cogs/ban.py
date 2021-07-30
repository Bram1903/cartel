import discord
from discord import Embed
from discord.ext import commands


class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages
        if not permission:
            return argument
        else:
            await ctx.send("You cannot punish other staff members.")
            raise commands.BadArgument(
                "You cannot punish other staff members")


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ban module has successfully been initialized.')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Sinner = None, reason="Not specified"):
        if not user:
            return await ctx.send("You must specify a user")
        userDM = Embed(title="CartelPvP | Moderation",
                       description=f"You have been banned from CartelPvP",
                       colour=0xAE0808)

        userDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        userDM.add_field(name="Banned by", value=f"{ctx.author}", inline=True)
        userDM.add_field(name="Reason", value=f"{reason}", inline=True)
        if user:
            try:
                await user.send(embed=userDM)
            except discord.Forbidden:
                pass
        try:
            await user.ban(reason=reason)
        except discord.Forbidden:
            return await ctx.send("Are you trying to ban someone higher than the bot")
        embedBan = Embed(title="CartelPvP | Moderation",
                         description=f"{user} has been banned from CartelPvP.",
                         colour=0xAE0808)
        embedBan.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        embedBan.add_field(name="**Banned by**", value=f"{ctx.author}", inline=True)
        embedBan.add_field(name="**Reason**", value=f"{reason}", inline=True)
        await ctx.send(embed=embedBan)


def setup(client):
    client.add_cog(Ban(client))
