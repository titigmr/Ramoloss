import re
from textwrap import TextWrapper
import discord
from discord.ext import commands

from cogs.utils import (
    UltimateFD,
    HelperCommand,
    ParseArgs,
    TITLE_UFD,
    DESCRIPTION_COMMAND_UFD,
    REF_ATK
)


class UFD(commands.Cog, HelperCommand, ParseArgs):
    """Ultimate Frame Data module"""

    def __init__(self, bot):
        super().__init__()
        ufd = UltimateFD(character=None, moves=None)
        self.bot = bot
        self.url = ufd.url
        self.get_all_characters = ufd._get_all_characters
        self.ref_atk = ufd.REF_ATK

    @commands.cooldown(5, 30, commands.BucketType.user)
    @commands.command(name="ufd")
    async def ufd(self, ctx, command=None, *args):

        if command is None or "help" in command:
            help_message = self.help(title=TITLE_UFD, description_command=DESCRIPTION_COMMAND_UFD)
            await ctx.channel.send(embed=help_message)
            return

        if command == "list":
            subcommand = self._select_subcommand(arguments=args)

            # TODO: refactor this using match-case once 3.10 is out & stable
            if subcommand in ("char", 'perso'):
                all_embed_m = self.char_typecommand(arguments=args)
                for embed_m in all_embed_m:
                    await ctx.send(embed=embed_m)

            elif subcommand in ("moves", 'move'):
                all_embed_m = self.moves_typecommand()
                for embed_m in all_embed_m:
                    await ctx.send(embed=embed_m)

            elif subcommand == "index":
                pass

            else:
                await ctx.channel.send((
                    "Unrecognized command: make sure you're choosing"
                    "between 'char', 'move', 'index'"))
                return

        else:
            if args is None:
                args = "all"
            else:
                if len(args) == 1:
                    options = re.findall("[a-z]+", args[0])
                elif len(args) >= 1:
                    arguments = "".join(args)
                    try:
                        options = self.find_options(message=arguments, options=[])
                    except ValueError:
                        return ("Please make sure you are using the format"
                                "'$ufd character [Move1] [Move2] [Move3]'")
                else:
                    options = "all"

                try:
                    char = UltimateFD(
                        character=command,
                        moves=options,
                        get_hitbox=True,
                        args_stats=None,
                    )
                except (ValueError, KeyError) as error:
                    await ctx.send(f"{error}")
                    return

                for move, statistics in char.stats.items():
                    hitbox = None
                    embed = discord.Embed(
                        title=f"**{char.char.title().replace('_', ' ')} – {move.title()}**",
                        color=0x03F8FC,
                        url=self.url + char.char,
                    )
                    for stats, amount in statistics.items():
                        if stats == "hitbox":
                            hitbox = amount
                        else:
                            amount_c = str(f"""```css\n{amount}```""")
                            embed.add_field(
                                name=f"**{stats.title()}**", value=amount_c, inline=True
                            )

                    await ctx.send(embed=embed)
                    if hitbox is not None:
                        await ctx.send(hitbox)

    def show_list(self, selection):
        all_characters = self.get_all_characters(self.url[:-1])
        if selection is None:
            selection = ""

        names = [name for name in all_characters if selection in name]
        return names

    @ufd.error
    async def ufd_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @staticmethod
    def show_wrap_message(list_to_out, title, wrap_at=1000):
        output = "\n".join(list_to_out)
        send_messages = TextWrapper(
            wrap_at, break_long_words=False, replace_whitespace=False
        ).wrap(output)

        return [discord.Embed(title=title, description=m) for m in send_messages]

    @staticmethod
    def _select_subcommand(arguments):
        if len(arguments) == 0:
            return "char"
        return arguments[0]

    def char_typecommand(self, arguments, selection=None):
        if arguments is not None and len(arguments) >= 2:
            selection = arguments[1]
        list_char = self.show_list(selection=selection)

        list_e = self.show_wrap_message(
            list_to_out=list_char,
            title="Liste des personnages")
        return list_e

    def moves_typecommand(self):
        list_moves = [f"**{ref}** ({move.title()})"
                      for ref, move in REF_ATK.items()]
        list_e = self.show_wrap_message(
            list_to_out=list_moves,
            title="Liste des mouvements"
        )
        return list_e


def setup(bot):
    bot.add_cog(UFD(bot))
