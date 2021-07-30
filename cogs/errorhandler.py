import sys
import traceback

import discord
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Error handler has successfully been initialized.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        if isinstance(error, commands.MissingPermissions):
            # generic error handler for commands from guilds without permissions
            perms = str(error.missing_perms)[1:][:-1].title().replace("_", " ").replace("'", "")
            try:
                embed = discord.Embed(
                    description=f"You are missing the following permissions: \n"
                                f"`{perms}`",
                    colour=discord.Colour.red(),
                )
                embed.set_author(name='Error | Permissions', icon_url='https://i.imgur.com/sFhjp83.png')
                return await ctx.send(embed=embed)
            except:
                return await ctx.send(f"You are missing the following permissions:\n"
                                      f"`{perms}`\n"
                                      f"As this error is not in an embed, please enable the `embed links` permission, "
                                      f"or else I cannot continue.")


def setup(client):
    client.add_cog(CommandErrorHandler(client))
