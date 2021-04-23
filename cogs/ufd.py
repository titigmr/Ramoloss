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
        self.ref_atk = ufd.REF_ATK


    @commands.cooldown(5, 30, commands.BucketType.user)
    @commands.command(name='ufd')
    async def ufd(self, ctx, command=None, *args):

        if 'help' in command or command is None:
            await ctx.channel.send(embed=self.help(
                title=TITLE_UFD, description_command=DESCRIPTION_COMMAND_UFD))
            return

        if command == 'list':
            if len(args) == 0:
                type_command = 'char'
            else:
                type_command = args[0]

            if type_command == 'char':
                selection=None
                if args is not None and len(args) >= 2:
                    selection = args[1]
                list_char = self.show_list(ctx=ctx, selection=selection)
                em = self.show_wrap_message(list_to_out=list_char,
                                            title='Liste des personnages')
                for m in em:
                    await ctx.send(embed=m)

            elif type_command == 'moves':
                list_moves = [f"**{ref}** ({move.title()})" for ref, move in REF_ATK.items()]
                em = self.show_wrap_message(list_to_out=list_moves, title='Liste des mouvements')
                for m in em:
                    await ctx.send(embed=m)

            elif type_command == 'index':
                pass

            else:
                await ctx.channel.send("Unrecognezied command: make sure you're choosing between {'char', 'moves', 'index'}")
                return

        else:
            if args is None:
                args='all'
            else:
                if len(args) == 1:
                    options=re.findall('[a-z]+', args[0])
                elif len(args) >= 1:
                    arguments="".join(args)
                    try:
                        options=self.find_options(message=arguments, options=[])
                    except:
                        return "Please make sure you are using the format '$ufd character [Move1] [Move2] [Move3]'"
                else:
                    options='all'

                try:
                    char=UltimateFD(character=command, moves=options,
                                      get_hitbox=True, args_stats=None)
                except (ValueError, KeyError) as f:
                    await ctx.send(f'{f}')
                    return

                for move, statistics in char.stats.items():
                    hb=None
                    embed=discord.Embed(
                        title=f"**{char.char.title().replace('_', ' ')} – {move.title()}**",
                        color=0x03f8fc, url=self.url + char.char)
                    for stats, amount in statistics.items():
                        if stats == 'hitbox':
                            hb=amount
                        else:
                            amount_c=str(f"""```css\n{amount}```""")
                            embed.add_field(name=f'**{stats.title()}**',
                                            value=amount_c,
                                            inline=True)

                    await ctx.send(embed=embed)
                    if hb is not None:
                        await ctx.send(hb)

    def show_list(self, ctx, selection):
        all_characters=self.get_all_characters(self.url[:-1])
        if selection is None:
            selection=''

        names=[name for name in all_characters if selection in name]
        return names

    def show_wrap_message(self, list_to_out, title, wrap_at=1000):
        output="\n".join(list_to_out)
        send_messages=TextWrapper(wrap_at,
                                    break_long_words=False,
                                    replace_whitespace=False).wrap(output)

        return [discord.Embed(title=title, description=m) for m in send_messages]


    @ufd.error
    async def ufd_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

def setup(bot):
    bot.add_cog(UFD(bot))
