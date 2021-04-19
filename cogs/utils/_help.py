import discord
import json
import os

with open('config.json') as f:
    config_arg = json.load(f)["command_prefix"]


TITLE_UFD = "**Ultimate frame data**"
DESCRIPTION_COMMAND_UFD = f"""
                    Get all characters name with -l option (show links)
                    {config_arg}ufd list [search] -l
                    """

TITLE_POLL = "**Create a poll**"
DESCRIPTION_COMMAND_POLL = f"""
                        Create a simple poll.
                        {config_arg}poll Kenshuri is a troll?

                        For advanced polls use the folowing syntax:
                        {config_arg}poll {{title}} [Option1] [Option2] [Option 3] ...

                        Note: options are limited at 21.
                        """




class HelperCommand:
    def __init__(self):
        pass

    def help(self, title, description_command):
        e = discord.Embed(title=title,
                          description=description_command)
        return e

