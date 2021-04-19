import discord
from bot import Ramoloss
import sys
import json
import os

with open('config.json') as config_file:
    config = json.load(config_file)

token = os.environ["DISCORD_TOKEN"]
bot = Ramoloss(config=config, token=token)
bot.run()