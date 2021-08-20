import json
import os
from asyncio import sleep

import discord
from discord import Embed
from discord import PermissionOverwrite
from discord.ext import commands
from discord.ext.commands import has_permissions, cooldown, BucketType, \
    check

with open("config.json") as configFile:
    data = json.load(configFile)
    for value in data["server_details"]:
        ticket_logs = value['ticket_logs_id']
        TICKET_CATEGORY_ID = value['ticket_category_id']
        TICKET_CHANNEL_ID = value['ticket_channel_id']
        admins = value['admins']

#  Adjust to your likings, but ONLY use lowercase even if the role in the server has Uppercase!
GENERIC_ELEVATED_ROLES = ("cold support", "head-admin", "senior-admin", "admin", "manager")
ROLES1 = ("cold support", "manager", "head-admin")
ROLES2 = ("cold support", "trial-mod", "mod", "senior-mod", "support team")
ROLES3 = ("cold support", "head-admin", "senior-admin", "admin", "manager", "support team")
ROLES4 = ("senior-mod", "head-admin", "senior-admin", "admin", "manager")

#  Ticket reactions, (inherit, description, roles)
REACTIONS = {
    "✉️": {"inherit": False, "description": "Player report",
           "roles": ROLES2},
    "🛒": {"inherit": False, "description": "Buycraft issue or question",
           "roles": ROLES1},
    "🚓": {"inherit": False, "description": "Admin support",
           "roles": GENERIC_ELEVATED_ROLES},
    "✍️": {"inherit": False, "description": "Appeal a ban",
           "roles": ROLES4},
    "❓": {"inherit": False, "description": "Other issue/not specified",
          "roles": ROLES3}
}
TICKET_CATEGORY = (int(TICKET_CATEGORY_ID))

OVERWRITE_ALLOW = PermissionOverwrite(read_messages=True, send_messages=True)


def only_tickets():
    async def predicate(ctx):  # AND AND AND!!!
        channel = ctx.channel
        return channel.topic and channel.topic.isdigit() and channel.category and channel.category.id == TICKET_CATEGORY

    return check(predicate)


def has_too_many_tickets(query, category_channels) -> bool:  # This is sort of how VOID checks for duplicate tickets
    return any(channel.topic and query in channel.topic for channel in category_channels)


async def recreate_reactions(message):
    for reaction in REACTIONS:
        await message.add_reaction(reaction)


async def handle_reaction_overflow(message):
    if len(message.reactions) != 5:
        await message.clear_reactions()
        await recreate_reactions(message)

    elif any(reaction.count > 2 for reaction in message.reactions):
        await recreate_reactions(message)


class ticket(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ticket module has successfully been initialized.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if "ADD" not in payload.event_type or payload.emoji.name not in REACTIONS:
            return

        guild = self.client.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        author = payload.member

        TICKET_CHANNEL = (int(TICKET_CHANNEL_ID))
        if channel.id != TICKET_CHANNEL or not author or author.bot:
            return

        ticket_category = None
        for category in guild.categories:
            if category.id == TICKET_CATEGORY:
                ticket_category = category

        if not ticket_category:
            return print("Unable to find ticket category")

        if has_too_many_tickets(str(author.id), ticket_category.text_channels):
            return

        metadata = REACTIONS.get(payload.emoji.name)  # I guess you could use this to validate line 48 too
        if metadata['inherit']:
            await self.create_ticket(guild, author, ticket_category, 0xAE0808, metadata['description'], True)
        else:
            await self.create_ticket(guild, author, ticket_category, 0xAE0808, metadata['description'], False,
                                     metadata['roles'])

        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, author)
        await handle_reaction_overflow(message)

    async def create_ticket(self, guild, author, category, colour, message, inherit_overwrites=False, roles=None):
        guild_roles = guild.roles

        ticket_created = Embed(title=f"{author} has created a new ticket",
                               description="Please state your issue and do not ping staff\nUse ?close (reason) "
                                           "to close the ticket",
                               colour=colour)

        if inherit_overwrites:
            overwrites = category.overwrites
        else:
            overwrites = {}
            roles_to_add = [role for role in guild_roles if role.name.lower() in roles]
            overwrites.update({role: OVERWRITE_ALLOW for role in roles_to_add})

        overwrites[guild.default_role] = PermissionOverwrite(read_messages=False)
        overwrites[author] = OVERWRITE_ALLOW
        overwrites[self.client.user] = OVERWRITE_ALLOW

        ticket_created.add_field(name="Ticket category", value=message)
        ticket_created.set_thumbnail(url=author.avatar_url)

        ticket = await guild.create_text_channel(f"ticket-{author.name}",
                                                 category=category,
                                                 topic=author.id, overwrites=overwrites)
        await ticket.send(f"{author.mention} Staff will be with you shortly", embed=ticket_created)
        if message == "Appeal a ban":
            ticket_appeal = Embed(title="CartelPvP | Appeals",
                                  colour=0xAE0808)

            ticket_appeal.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/807568994202025996/854995835154202644/lg-1.png")
            ticket_appeal.add_field(name="Use the following format",
                                    value="Once you fill out your appeal using the following format please"
                                          " be patient while we look into your punishment.",
                                    inline=False)
            ticket_appeal.add_field(name="• IGN", value="Your in-game username.", inline=False)
            ticket_appeal.add_field(name="• Ban Reason", value="The reason you got banned.", inline=False)
            ticket_appeal.add_field(name="• Guilty", value="Do you plead guilty?", inline=False)
            ticket_appeal.add_field(name="• Ban date", value="When did you get banned?", inline=False)
            ticket_appeal.add_field(name="• Unban reason", value="Why should we unban you?", inline=False)
            ticket_appeal.set_footer(text="CartelPvP | Appeals")
            await ticket.send(embed=ticket_appeal)

    @commands.command()
    @has_permissions(mention_everyone=True)  # Good enough, I mean, what Admin can't mention everyone
    async def setup(self, ctx):
        ticket_panel = Embed(title="Cartel | Tickets", description="Please open a ticket depending on your issue",
                             colour=0xAE0808)  # We bri'ish use colour, init
        ticket_panel.add_field(name="Options", value="✉️ | Report a player for abuse\n"
                                                     "🛒 | Buycraft support\n"
                                                     "🚓 | Admin-only support\n"
                                                     "✍️ | Appeal a ban\n"
                                                     "❓  | Other / unspecified support")
        ticket_panel.set_image(
            url="https://cdn.discordapp.com/attachments/785967499153113089/855027002721173524/create_a_ticket.png")
        ticket_panel.set_footer(text="CartelPvP Ticket System")
        message = await ctx.send(embed=ticket_panel)
        await recreate_reactions(message)

    @commands.command()
    @cooldown(1, 5, BucketType.channel)  # Used in VOID; prevents 2 people closing ticket at once
    @only_tickets()  # This check/line is important. Do not change otherwise members might end up deleting channels
    async def close(self, ctx, *, reason=None):
        if not reason:
            return await ctx.send("You must specify a reason.")
        ticket_closing = Embed(title="Closing this ticket in 5 seconds",
                               description="You can now forget this ticket ever existed",
                               colour=0xAE0808)
        await ctx.send(embed=ticket_closing)
        await sleep(4.7)

        fileName = f"{ctx.channel.name}.txt"
        with open(fileName, "w") as file:
            async for msg in ctx.channel.history(limit=None):
                file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n")

        await ctx.channel.delete(reason=f"Closed by {ctx.author}, reason: {reason}")
        channel = ctx.channel
        user = await self.client.fetch_user(channel.topic)
        ticket_dm = Embed(title=f"CartelPvP | Tickets",
                          description="Your ticket in CartelPvP has been closed.",
                          colour=0xAE0808)

        ticket_dm.set_thumbnail(url=user.avatar_url)
        ticket_dm.add_field(name="Closed by", value=f"{ctx.author.display_name}", inline=True)
        ticket_dm.add_field(name="Reason", value=f"{reason}", inline=True)
        if user:
            try:
                await user.send(embed=ticket_dm)
            except discord.Forbidden:
                pass

        ticket_staff = Embed(title=f"CartelPvP | Tickets",
                             description=f"{user} his ticket has been closed.",
                             colour=0xAE0808)

        ticket_staff.set_thumbnail(url=ctx.author.avatar_url)
        ticket_staff.add_field(name="Closed by", value=f"{ctx.author.display_name}", inline=True)
        ticket_staff.add_field(name="Reason", value=f"{reason}", inline=True)

        channel = self.client.get_channel(int(ticket_logs))
        await channel.send(embed=ticket_staff)
        file = discord.File(fileName)
        await channel.send(file=file)

        os.remove(fileName)


def setup(client):
    client.add_cog(ticket(client))
