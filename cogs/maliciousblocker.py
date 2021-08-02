import json
from asyncio import sleep

from discord import Embed
from discord.ext import commands

with open("./config.json") as configFile:  # Opens the file config.json as a config file
    data = json.load(configFile)  # Var data is the value in the json.config file
    for value in data["server_details"]:  # For the data in server_details
        logging_channel = value['logging_channel']  # Gets the specific data
        admins = value['admins']
        TICKET_CATEGORY_ID = value['ticket_category_id']

with open('badwords.txt') as file:
    bad_words = file.read()

TICKET_CATEGORY = (int(TICKET_CATEGORY_ID))


class Maliciousblocker(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Maliciousblocker has successfully been initialized.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.channel.category_id == TICKET_CATEGORY:
            return
        try:
            no_perm = Embed(colour=0xAE0808)
            no_perm.set_author(name=f'Do not send that, {message.author.display_name}.',
                               icon_url='https://i.imgur.com/l2tL2kc.png')
            if any(bad_word in message.content.strip().lower() for bad_word in bad_words):
                await message.delete()
                msg = await message.channel.send(embed=no_perm)
                await sleep(4.7)
                await msg.delete()
        except:
            pass


def setup(client):
    client.add_cog(Maliciousblocker(client))
