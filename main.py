import discord
from bot import Ramoloss
import sys
import json
import os

with open('config.json') as config_file:
    config = json.load(config_file)

extensions = (
    'cogs.dice',
    'cogs.john',
    'cogs.poll',
    'cogs.ufd'
)

token = os.environ["DISCORD_TOKEN"]
bot = Ramoloss(config=config, token=token, extensions=extensions)
bot.run()