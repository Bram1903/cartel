import os
import sys

import discord
from discord import Activity, ActivityType
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    pass

client = Bot(command_prefix=">",
             help_command=None,
             case_insensitive=True,
             max_messages=100,
             activity=Activity(type=ActivityType.watching,
                               name=f"over Cartel."),
             intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Main system is operational.")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
