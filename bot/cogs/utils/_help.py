import json
import discord


with open('config.json', 'r', encoding='utf-8') as f:
    config_arg = json.load(f)["command_prefix"]


REF_COLOR = {'dice': '#8B0000'}

TITLE_DICE = "**Roll a random dice**"
DESCRIPTION_COMMAND_DICE = f"""
                        Roll one six sided die.
                        ```{config_arg}d 1d6```
                        Roll two four sided die.
                        ```{config_arg}d 2d4```
                        Roll one -101 to 150 sided die.
                        ```{config_arg}d 1d[-101:150]```
                        Add a one six sided die and a eight \
                            sided die (all display).
                        ```{config_arg}d 1d6 + 1d8 -v```
                        Minus a one six sided die and a eight sided \
                            die (only output).
                        ```{config_arg}d 1d6 - 1d8```
                        Add 6 at a one sided die.
                        ```{config_arg}d 1d6 + 6```
                        """


TITLE_UFD = "**Ultimate frame data**"
DESCRIPTION_COMMAND_UFD = f"""
                    Get all characters name with -l option (show links)
                    {config_arg}ufd list [search] -l
                    """

TITLE_POLL = "**Create a poll**"
DESCRIPTION_COMMAND_POLL = f"""
                        Create a simple poll.
                        ```{config_arg}poll Kenshuri is a troll?```
                        For advanced polls use the folowing syntax:
                        ```{config_arg}poll {{title}} [Option1] \
                            [Option2] [Option 3] ...```
                        *Note: options are limited at 21.*
                        """


class HelperCommand:
    def __init__(self):
        pass

    def help(self, title, description_command):
        embed_m = discord.Embed(title=title,
                                description=description_command)
        return embed_m
