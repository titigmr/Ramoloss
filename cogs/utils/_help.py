import discord
import json

with open('../../config.json') as f:
    config_arg = json.load(f)


TITLE_UFD = "**Ultimate frame data**"
DESCRIPTION_COMMAND_UFD = """
                    Get all characters name with -l option (show links)
                    $ufd list [search] -l
                    """


class HelperCommand:
    def __init__(self):
        pass

    def help(self, title, description_command):
        e = discord.Embed(title=title,
                          description=description_command)
        return e

