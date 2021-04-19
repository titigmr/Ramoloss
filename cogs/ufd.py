import re
from textwrap import TextWrapper

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

from cogs.utils import (
    DEFAULT_EXCLUDE_OVERALL_STATS, DEFAULT_STATS, REF_ATK, UltimateFD, HelperCommand,
    ParseArgs, TITLE_UFD, DESCRIPTION_COMMAND_UFD)


class UFD(commands.Cog, HelperCommand, ParseArgs):
    def __init__(self, bot):
        ufd = UltimateFD(character=None, moves=None)
        self.bot = bot
        self.url = ufd.url
        self.get_all_characters = ufd._get_all_characters

    @commands.command(name='ufd')
    async def character(self, ctx, command=None, *args):

        if command is None or 'help' in command:
            await ctx.channel.send(embed=self.help(
                title=TITLE_UFD, description_command=DESCRIPTION_COMMAND_UFD))
            return

        if command == 'list':
            selection, get_link = self.parse_command_list(args)
            if selection is None and get_link is None:
                await ctx.send('Too much arguments')
                return

            out = self.show_list(ctx=ctx, selection=selection, get_link=get_link)
            em = self.show_wrap(string_to_out=out, title='Liste des personnages')
            for m in em:
                await ctx.send(embed=m)
        else:
            if args is None:
                args = 'all'
            else:
                if len(args) == 1:
                    options = re.findall('[a-z]+', args[0])
                elif len(args) >= 1:
                    args = "".join(args)
                    try:
                        options = self.find_options(message=args, options=[])
                    except:
                        return "Please make sure you are using the format '$ufd character [Move1] [Move2] [Move3]'"
                else:
                    options = 'all'
                print(command, options)
                try:
                    char = UltimateFD(character=command, moves=options,
                                      get_hitbox=True, args_stats=None)
                except (ValueError, KeyError) as f:
                    await ctx.send(f'{f}')
                    return

                for move, statistics in char.stats.items():
                    hb = None
                    embed = discord.Embed(
                        title=f"**{char.char.title().replace('_', ' ')} – {move.title()}**",
                        color=0x03f8fc,
                        url=self.url + char.char)
                    v = ''
                    for stats, amount in statistics.items():
                        if stats == 'hitbox':
                            hb = amount
                        else:
                            amount_c = str(f"""```css\n{amount}```""")
                            embed.add_field(name=f'**{stats.title()}**',
                                    value=amount_c,
                                    inline=True)

                    await ctx.send(embed=embed)
                    if hb is not None:
                        await ctx.send(hb)

    def parse_command_list(self, args):
        grep = None
        get_link = False
        if len(args) >= 1:
            if '-l' in args:
                get_link = True
            grep = args[0]
            if grep == '-l':
                if len(args) >= 2:
                    grep = args[1]
                else:
                    grep = None
            if len(args) >= 3:
                return None, None
        return grep, get_link

    def show_list(self, ctx, selection, get_link):
        # to remove the / at the end
        all_characters = self.get_all_characters(self.url[:-1])
        if selection is None:
            selection = ''

        if get_link:
            names = [f'{name} : {link}' for name, link in all_characters.items(
            ) if selection in name.split(':')[0]]
        else:
            names = [name for name in all_characters if selection in name]
        return names

    def show_wrap(self, string_to_out, title, wrap_at=1000):
        output = "\n".join(string_to_out)
        send_messages = TextWrapper(wrap_at,
                                    break_long_words=False,
                                    replace_whitespace=False).wrap(output)

        return [discord.Embed(title=title, description=m) for m in send_messages]


def setup(bot):
    bot.add_cog(UFD(bot))
