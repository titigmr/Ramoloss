from textwrap import TextWrapper
import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError

from cogs.utils import (
    UltimateFD,
    HelperCommand,
    TITLE_UFD,
    DESCRIPTION_COMMAND_UFD,
    REF_ATK
)


class UFD(commands.Cog, HelperCommand):
    """Ultimate Frame Data module"""

    def __init__(self, bot):
        super().__init__()
        ufd = UltimateFD(character=None, moves=None)
        self.bot = bot
        self.url = ufd.url
        self.get_all_characters = ufd.get_all_characters
        self.n_args = None
        self.command = None
        self.args = None

    @commands.cooldown(rate=5, per=30, type=commands.BucketType.user)
    @commands.command(name="ufd")
    async def ufd(self, ctx, command=None, *args):
        """
        Command UFD for get information about moves for a character in
        SSBU i.e "ufd wario nair fair"
        """
        self.n_args = len(args)
        self.command = command
        self.args = iter(args)

        match self.command:
            case None | 'help':
                help_message = self.help(title=TITLE_UFD,
                                        description_command=DESCRIPTION_COMMAND_UFD)
                await ctx.channel.send(embed=help_message)
                return

            case 'list':
                subcommand = self.select_subcommand()

                match subcommand:
                    case "char" | 'chars':
                        all_embed_m = self.select_typecommand(choice='char')
                        for embed_m in all_embed_m:
                            await ctx.channel.send(embed=embed_m)

                    case 'move' | 'moves':
                        all_embed_m = self.select_typecommand(choice='move')
                        for embed_m in all_embed_m:
                            await ctx.channel.send(embed=embed_m)

                    case 'index':
                        pass

                    case _:
                        raise ValueError((
                            "Unrecognized command: make sure you're choosing "
                            "between 'char', 'move', 'index'"))

            case _:
                if not self.n_args:
                    raise ValueError('Must choice a move. Availables moves with "ufd list moves"')

                char = UltimateFD(character=command,
                                    moves=self.args,
                                    get_hitbox=True,
                                    args_stats=None)


                for move, statistics in char.stats.items():
                    embed, hitbox = self.create_stats(move=move, statistics=statistics)
                    await ctx.channel.send(embed=embed)

                    if hitbox is not None:
                        await ctx.channel.send(hitbox)

    @ufd.error
    async def error(self, ctx, error):
        if isinstance(error, (commands.CommandOnCooldown, CommandInvokeError)):
            if isinstance(error, CommandInvokeError):
                error = error.__cause__
            await ctx.send(f'```ERROR: {error.__cause__}```')
        print(error)


    def show_list(self, selection):
        """
        Show list of characters with filter not None
        """
        all_characters = self.get_all_characters(self.url[:-1])
        selection = "" if selection is None else selection
        names = [name for name in all_characters if selection in name]
        return names


    @staticmethod
    def show_wrap_message(list_to_out, title, wrap_at=1000):
        """
        Show embed message in discord channel
        with split at wrap_at (default: 1000 chars)
        """
        output = "\n".join(list_to_out)
        send_messages = TextWrapper(wrap_at,
                                    break_long_words=False,
                                    replace_whitespace=False).wrap(output)
        return [discord.Embed(title=title, description=m) for m in send_messages]


    def select_subcommand(self):
        """
        Select subcommand, default 'char' command
        """
        if self.n_args:
            self.n_args -= 1
            return next(self.args)
        return "char"


    def select_typecommand(self, choice: str ='char', selection=None):
        """
        Select type command
            - if type is 'char' return embed
              list char (with filter if selection is not None)
            - if type is 'move' return embed list moves
        """
        match choice:
            case 'char':
                if self.n_args:
                    selection = next(self.args)
                    print(selection)
                    self.n_args -= 1

                list_out = self.show_list(selection=selection)
                title = "Liste des personnages"
            case 'move':
                list_out = [f"**{ref}** ({move.title()})"
                      for ref, move in REF_ATK.items()]
                title = "Liste des mouvements"

        list_embed = self.show_wrap_message(list_to_out=list_out,
                                            title=title)
        return list_embed


    def create_stats(self, move, statistics, hitbox=None):
        """
        Create stats embed with hitbox if available
        """

        title = f"**{self.command.title().replace('_', ' ')} – {move.title()}**"
        embed = discord.Embed(title=title,
                                color=0x03F8FC,
                                url=self.url + self.command)
        for stats, amount in statistics.items():
            if stats == "hitbox":
                hitbox = amount
            else:
                embed.add_field(name=f"**{stats.title()}**",
                                value=str(f"""```css\n{amount}```"""),
                                inline=True)
        return embed, hitbox

def setup(bot):
    bot.add_cog(UFD(bot))
