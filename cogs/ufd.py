import re
from utils import UltimateFD, REF_ATK, DEFAULT_STATS, DEFAULT_EXCLUDE_OVERALL_STATS
from textwrap import TextWrapper


import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class UFD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://ultimateframedata.com"

    def get_all_characters(self, url):
        soup = BeautifulSoup(requests.get(url).content, 'lxml')
        characters = {}
        for i in soup.find_all('a'):
            href = i["href"]
            if ('.php' in href) and ('stats' not in href):
                name = href[1:].replace('.php', '')
                url_c = url + href
                characters[name] = url_c
        return characters

    @commands.command(name='ufd')
    async def character(self, ctx, command, *args):


        if command is None or 'help' in command:
            await ctx.channel.send(embed=self.help())
            return

        if command == 'list':
            selection, get_link = self.parse_command_list(args)
            if selection is None and get_link is None:
                await ctx.send('Too much arguments')
                return

            em = self.show_list(ctx=ctx, selection=selection, get_link=get_link)
            for i in em:
                await ctx.send(embed=i)

    def help(self):
        title = "**Ultimate frame data**"
        description_command = """
                                Get all characters name
                                $ufd list [search] -l
                                -l : show links
                                """

        e = discord.Embed(title=title,
                          description=description_command)
        return e

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
