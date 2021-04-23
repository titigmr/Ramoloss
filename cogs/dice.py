import discord
from discord.ext import commands
import numpy as np
import re

from cogs.utils import HelperCommand, TITLE_DICE, DESCRIPTION_COMMAND_DICE


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
            await ctx.channel.send(embed=self.help(title=TITLE_DICE, description_command=DESCRIPTION_COMMAND_DICE))
            return

        values = []
        if ('+' in args) or ('-' in args):
            calculation = True
            if '-v' not in args:
                verbose = False

        for l in args:
            if 'd' in l:
                try:
                    size, high = l.split('d')
                except ValueError as  error:
                    # This really feels wrong, there has to be a better way but i guess we'll be refactoring
                    if (error.args[0] == "not enough values to unpack (expected 2, got 1)"):
                        size = 1
                        high = l.split('d')
                    else:
                        await ctx.send("Bad request, please use $d help.")
                if (int(size) > 1) and (calculation):
                    await ctx.send('Calculation with more than one dice'
                                   'is not currently supported.')
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
