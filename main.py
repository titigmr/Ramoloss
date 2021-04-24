import json
import os
from bot import Ramoloss


with open('config.json') as config_file:
    config = json.load(config_file)

token = os.environ["DISCORD_TOKEN"]
bot = Ramoloss(config=config, token=token)
bot.run()
