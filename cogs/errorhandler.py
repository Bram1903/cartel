import sys
import traceback

import discord
from discord.ext import commands
from asyncio import sleep


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
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        if isinstance(error, commands.MissingPermissions):
            # generic error handler for commands from guilds without permissions
            perms = str(error.missing_perms)[1:][:-1].title().replace("_", " ").replace("'", "")
            try:
                await ctx.message.delete()
                embed = discord.Embed(
                    description=f"You are missing the following permissions: \n"
                                f"`{perms}`",
                    colour=0xAE0808,
                )
                embed.set_author(name='Error | Permissions', icon_url='https://i.imgur.com/sFhjp83.png')
                msg = await ctx.send(embed=embed)
                await sleep(4.7)
                await msg.delete()
                return
            except:
                return await ctx.send(f"You are missing the following permissions:\n"
                                      f"`{perms}`\n"
                                      f"As this error is not in an embed, please enable the `embed links` permission, "
                                      f"or else I cannot continue.")
        if isinstance(error, commands.CommandOnCooldown):
            try:
                em = discord.Embed(color=0xAE0808)
                em.set_author(name=f'You can use this command again in {round(error.retry_after, 2)}s'
                              , icon_url='https://i.imgur.com/SR9wWm9.png')
                await ctx.send(embed=em, delete_after=10)
            except:
                return await ctx.send(f"You are on cooldown.\n"
                                      f"`You can use this again in {round(error.retry_after, 2)}s`\n"
                                      f"As this error is not in an embed, please enable the `embed links` permission, "
                                      f"or else I cannot continue.")


def setup(client):
    client.add_cog(CommandErrorHandler(client))
