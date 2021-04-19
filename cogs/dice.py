import discord
from discord.ext import commands
import numpy as np
import re

from utils import HelperCommand


TITLE = "**Roll a random dice**"
DESCRIPTION_COMMAND = """
                        Roll one six sided die.
                        $d 1d6

                        Roll two four sided die.
                        $d 2d4

                        Roll one -101 to 150 sided die.
                        $d 1d[-101:150]

                        Add a one six sided die and a eight sided die (all display).
                        $d 1d6 + 1d8 -v

                        Minus a one six sided die and a eight sided die (only output).
                        $d 1d6 - 1d8

                        Add 6 at a one sided die.
                        $d 1d6 + 6
                        """


class Dice(commands.Cog, HelperCommand):
    def __init__(self, bot):
        self.bot = bot

    def _check(self, args):
        roll = re.compile(r'^\d*d\d*$')
        number = re.compile(r'[0-9]*')
        for n, a in enumerate(args):
            if 'd' in a:
                if (not '[' in a) and (']' not in a):
                    if len(roll.findall(a)) < 1:
                        return False
            elif (n % 2) != 0:
                if a not in ["+", '-', '-v']:
                    return False
            elif (n % 2) == 0:
                if len(number.findall(a)) < 1:
                    if a not in ['-v']:
                        return False
            else:
                return False
        return True

    @commands.command(name='d')
    async def d(self, ctx, *args):
        "Roll a random dice (use `$d help` for using examples)"
        calculation = False
        verbose = True

        if not self._check(args):
            await ctx.send("Error in arguments. Make sure you are using the command correctly. For help use: $d help")
            return

        if len(args) < 1 or ('help' in args):
            await ctx.channel.send(embed=self.help(title=TITLE, description_command=DESCRIPTION_COMMAND))
            return

        values = []
        if ('+' in args) or ('-' in args):
            calculation = True
            if '-v' not in args:
                verbose = False

        for l in args:
            if 'd' in l:
                size, high = l.split('d')
                if (int(size) > 1) and (calculation):
                    await ctx.send('Calculation not working with more one dice.')
                    return
                number = self._random_de(size=size, high=high)
                for n in number:
                    values.append(n)
                    if verbose:
                        await ctx.send(f'{str(n)}')
            elif '-v' in l:
                continue
            elif ('+' in l) or ('-' in l):
                values.append(l)
            else:
                try:
                    values.append(int(l))
                except ValueError:
                    return

        if not calculation:
            return

        f = self._operator(values)
        if len(f) == 1:
            await ctx.send(f'{str(f)}')
        else:
            await ctx.send("Error in arguments. Make sure you are using the command correctly. For help use: $d help")

    def _random_de(self, low=1, high=6, size=1):
        if isinstance(high, str):
            if '[' and ']' in high:
                first = high.find('[')
                last = high.find(']')
                high = high[first+1:last]
                low, high = map(int, high.split(':'))
            else:
                high = int(high)
        size = int(size)
        return np.random.randint(low=low, high=high + 1, size=size)

    def _operator(self, values):
        if len(values) < 3:
            return values
        part = values[:3]

        if '+' in part:
            v = part[0] + part[-1]
        elif '-' in part:
            v = part[0] - part[-1]

        new_val = [v] + values[3:]
        return self._operator(new_val)


def setup(bot):
    bot.add_cog(Dice(bot))
