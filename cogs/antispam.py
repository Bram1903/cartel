import datetime
import json

import discord
from discord import Embed
from discord.ext import commands

import datetime
import time

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']


class antispam(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('antispam has successfully been initialized.')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        time_window_milliseconds = 5000
        max_msg_per_window = 5
        author_msg_times = {}

        author_id = ctx.author.id
        # Get current epoch time in milliseconds
        curr_time = datetime.datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
            author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
            msg_time for msg_time in author_msg_times[author_id]
            if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
            author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.

        if len(author_msg_times[author_id]) > max_msg_per_window:
            await ctx.send("Stop Spamming")


def setup(client):
    client.add_cog(antispam(client))
