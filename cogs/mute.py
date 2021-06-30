import discord
from discord.ext import commands
from discord import Embed, member


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


class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted in argument.roles:
            return argument
        else:
            raise commands.BadArgument("The user was not muted.")


async def mute(ctx, user, reason):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        try:
            muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted, send_messages=False,
                                              read_message_history=True,
                                              read_messages=True)
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make a muted role")
        await user.add_roles(muted)
        MutedDM = Embed(title="CartelPvP | Moderation",
                       description=f"You have been muted in CartelPvP",
                       colour=0xAE0808)
        MutedDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        MutedDM.add_field(name="Banned by", value=f"{ctx.author}", inline=True)
        MutedDM.add_field(name="Reason", value=f"{reason}", inline=True)
        if user:
            try:
                await user.send(embed=MutedDM)
            except discord.Forbidden:
                pass
        await ctx.send(embed=MutedDM)
    else:
        await user.add_roles(role)
        MutedEmbed = Embed(title="CartelPvP | Moderation",
                        description=f"You have been muted in CartelPvP",
                        colour=0xAE0808)
        MutedEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        MutedEmbed.add_field(name="Muted by", value=f"{ctx.author}", inline=True)
        MutedEmbed.add_field(name="Reason", value=f"{reason}", inline=True)
        await ctx.send(embed=MutedEmbed)


class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mute module has successfully been initialized.')

    @commands.command()
    async def mute(self, ctx, user: Sinner, reason=None):
        await mute(ctx, user, reason or "Not specified")

    @commands.command()
    async def unmute(self, ctx, user: Redeemed):
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        UnmutedEmbed = Embed(title="CartelPvP | Moderation",
                           description=f"{user} has been unmuted in CartelPvP",
                           colour=0xAE0808)
        UnmutedEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        UnmutedEmbed.add_field(name="Unmuted by", value=f"{ctx.author}", inline=True)
        UnmutedEmbed.add_field(name="Reason", value="Expired", inline=True)
        await ctx.send(embed=UnmutedEmbed)


def setup(client):
    client.add_cog(Mute(client))
