import json
import socket

import dns.resolver
import whois
from discord import Embed
from discord.ext import commands


def is_registered(domain_name):
    """
    A function that returns a boolean indicating
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)


with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        admins = value['admins']


class Domain(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Domain module has successfully been initialized.')

    @commands.group(name='domain', invoke_without_command=True)
    async def domain(self, ctx):
        pass

    @domain.command(name='ns')
    async def ns_subcommand(self, ctx, domain=None):
        if ctx.author.id not in admins:
            return
        if not domain:
            await ctx.send("You must provide a domain.")
            return
        domain = domain.replace('http://', '')
        domain = domain.replace('www.', '')
        domain = domain.replace('https://', '')
        try:
            message = await ctx.send("Searching...")
            answers = dns.resolver.resolve(f'{domain}', 'NS')
            ns_list = ""
            for server in answers:
                ns_list += f"{server.target}" + "\n"
            ns = Embed(colour=0xAE0808)
            ns.add_field(name="Name Servers", value=f"```\n{ns_list}```")
            ns.set_author(name=f"NS lookup for {domain}")
            await message.edit(content="", embed=ns)
        except Exception as e:
            error = Embed(colour=0xAE0808,
                          description=f"{e}")
            error.set_author(name=f"DNS Lookup Error",
                             icon_url='https://i.imgur.com/SR9wWm9.png')
            error.set_footer(text="We do not support sub domains. Are you sure you provided the right domain?")
            await ctx.send(embed=error)

    @domain.command(name='whois')
    async def whois_subcommand(self, ctx, domain=None):
        if ctx.author.id not in admins:
            return
        if not domain:
            await ctx.send("You must provide a domain.")
            return
        domain = domain.replace('http://', '')
        domain = domain.replace('www.', '')
        domain = domain.replace('https://', '')
        try:
            message = await ctx.send("Searching...")
            answers = dns.resolver.resolve(f'{domain}', 'NS')
            ns_list = ""
            for server in answers:
                ns_list += f"{server.target}" + "\n"
            ip = socket.gethostbyname(domain)
            if is_registered(domain):
                whois_info = whois.whois(domain)
            embed = Embed(colour=0xAE0808)
            embed.set_author(name=f"Whois lookup for {domain}")
            embed.add_field(name="IP", value=f"{ip}", inline=False)
            embed.add_field(name="Registrar", value=f"{whois_info.registrar}", inline=False)
            embed.add_field(name="Whois Server", value=f"{whois_info.whois_server}", inline=False)
            embed.add_field(name="Name Servers", value=f"\n{ns_list}", inline=False)
            await message.edit(content="", embed=embed)
        except Exception as e:
            error = Embed(colour=0xAE0808,
                          description=f"{e}")
            error.set_author(name=f"WHOIS Lookup Error",
                             icon_url='https://i.imgur.com/SR9wWm9.png')
            error.set_footer(text="Are you sure you provided the right domain?")
            await ctx.send(embed=error)


def setup(client):
    client.add_cog(Domain(client))
