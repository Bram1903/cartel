import discord
from discord import Embed
from discord.ext import commands


# This prevents staff members from being punished
class Sinner(commands.Converter):  # Creates the class
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages  # Given permission in this cage manage messages.
        if not permission:  # Checks if the member doesn't have manage messages permissions.
            return argument  # When the member doesn't have the permission it will go on with the argument (command).
        else:  # Else if the member does have manage messages as permission it will give a return.
            await ctx.send("You cannot punish other staff members.")  # Sends a message in the channel of the command
            # given.
            raise commands.BadArgument(  # Raises an error otherwise the console gets flood and mister pizza in your ass
                # gets angry
                "You cannot punish other staff members")


class Redeemed(commands.Converter):  # Creates the class
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)  # Basically the given command.
        muted = discord.utils.get(ctx.guild.roles, name="Muted")  # Defines the muted role.
        if muted in argument.roles:  # Checks for the muted role.
            return argument  # Goes back to the argument (command)
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
    else:
        await user.add_roles(role)


class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mute module has successfully been initialized.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, user: Sinner, reason=None):
        await ctx.message.delete()
        await mute(ctx, user, reason or "Not specified")
        MutedDM = Embed(title="CartelPvP | Moderation",
                        description=f"You have been muted in CartelPvP",
                        colour=0xAE0808)
        MutedDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        MutedDM.add_field(name="Muted by", value=f"{ctx.author}", inline=True)
        MutedDM.add_field(name="Reason", value=f"{reason}", inline=True)
        MutedEmbed = Embed(title="CartelPvP | Moderation",
                           description=f"{user} has been muted in CartelPvP",
                           colour=0xAE0808)
        MutedEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        MutedEmbed.add_field(name="Muted by", value=f"{ctx.author}", inline=True)
        MutedEmbed.add_field(name="Reason", value=f"{reason}", inline=True)
        if user:
            try:
                await user.send(embed=MutedDM)
            except discord.Forbidden:
                pass
            await ctx.send(embed=MutedEmbed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, user: Redeemed):
        await ctx.message.delete()
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        UnmutedEmbed = Embed(title="CartelPvP | Moderation",
                           description=f"{user} has been unmuted in CartelPvP",
                           colour=0xAE0808)
        UnmutedEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        UnmutedEmbed.add_field(name="Unmuted by", value=f"{ctx.author}", inline=True)
        UnmutedEmbed.add_field(name="Reason", value="Expired", inline=True)
        UnmutedDM = Embed(title="CartelPvP | Moderation",
                             description="You have been unmuted in CartelPvP",
                             colour=0xAE0808)
        UnmutedDM.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
        UnmutedDM.add_field(name="Unmuted by", value=f"{ctx.author}", inline=True)
        UnmutedDM.add_field(name="Reason", value="Expired", inline=True)
        if user:
            try:
                await user.send(embed=UnmutedDM)
            except discord.Forbidden:
                pass
            await ctx.send(embed=UnmutedEmbed)


def setup(client):
    client.add_cog(Mute(client))
