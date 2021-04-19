import re
from textwrap import TextWrapper

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

from cogs.utils import (DEFAULT_EXCLUDE_OVERALL_STATS, DEFAULT_STATS, REF_ATK,
                        UltimateFD, HelperCommand)



TITLE = "**Ultimate frame data**"
DESCRIPTION_COMMAND = """
                    Get all characters name with -l option (show links)
                    $ufd list [search] -l
                    """


class UFD(commands.Cog, HelperCommand):
    def __init__(self, bot):
        ufd = UltimateFD(character=None, moves=None)
        self.bot = bot
        self.url = ufd.url
        self.get_all_characters = ufd._get_all_characters

    @commands.command(name='ufd')
    async def character(self, ctx, command, *args):

        if command is None or 'help' in command:
            await ctx.channel.send(embed=self.help(title=TITLE, description_command=DESCRIPTION_COMMAND))
            return

        if command == 'list':
            selection, get_link = self.parse_command_list(args)
            if selection is None and get_link is None:
                await ctx.send('Too much arguments')
                return

            em = self.show_list(
                ctx=ctx, selection=selection, get_link=get_link)
            for i in em:
                await ctx.send(embed=i)

    def parse_command_list(self, args):
        grep = None
        get_link = False
        if len(args) == 1:
            if '-l' in args:
                get_link = True
            grep = args[0]
            if grep == '-l':
                if len(args) == 2:
                    grep = args[1]
                else:
                    grep = None
            if len(args) > 2:
                return None, None
        return grep, get_link

    def show_list(self, ctx, selection, get_link, wrap_at=1000):
        all_characters = self.get_all_characters(self.url)
        if selection is None:
            selection = ''

        if get_link:
            names = [f'{name} : {link}' for name, link in all_characters.items(
            ) if selection in name.split(':')[0]]
        else:
            names = [name for name in all_characters if selection in name]

        output = "\n".join(names)
        send_messages = TextWrapper(wrap_at,
                                    break_long_words=False,
                                    replace_whitespace=False).wrap(output)
        return [discord.Embed(title='Liste des personnages', description=m) for m in send_messages]


def setup(bot):
    bot.add_cog(UFD(bot))
